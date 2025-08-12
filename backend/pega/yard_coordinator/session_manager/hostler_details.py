import asyncio
import math

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.open_case.open_case import OpenCase
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file
from backend.pega.yard_coordinator.session_manager.pega_parser import (
    extract_hostler_view_details,
    extract_grid_action_fields,
    get_row_page,
    extract_str_index_in_list,
    extract_team_members_pd_key,
)
from backend.rules.validation import validate_and_store_tasks
from .hostler_utils import (
    extract_total_pages_lxml,
    extract_section_id,
    extract_pagelist_property,
    build_location_params,
    extract_context_page,
)

logger = setup_logger(__name__)


def get_field(obj, field, default=None):
    if isinstance(obj, dict):
        return obj.get(field, default)
    return getattr(obj, field, default)


async def enrich_and_store_task(session_manager, task):
    case_id = get_field(task, "case_id")
    if not case_id:
        return task

    # Open the case with OpenCase class, fetch HTML from step 4
    logger.error(f'Opening task via hostler_details.py')
    logger.error(f'Opening TASK: {case_id} to enrich task details.')

    await OpenCase(session_manager=session_manager, case_id=case_id).run()


async def fetch_hostler_details(session_manager, base_ref, page_size=10, step1_grid_action=False):
    all_tasks = []
    html_step = 30 if not step1_grid_action else 3000

    row_page = get_row_page(base_ref)
    logger.debug(f'fetch_hostler_details row_page: {row_page}')

    checker_id = None
    total_moves = None
    hostler_info = None

    # --- Get total moves from Redis ---
    if checker_id:
        hostler_info = await session_manager.hostler_store.get_hostler(checker_id)
        if hostler_info:
            total_moves = get_field(hostler_info, "moves")

    location_params_str = build_location_params(base_ref, session_manager.pzHarnessID)
    data = {
        "pyActivity": "pzRunActionWrapper",
        "rowPage": row_page,
        "Location": location_params_str,
        "PagesToCopy": row_page,
        "pzHarnessID": session_manager.pzHarnessID,
        "UITemplatingStatus": "N",
        "inStandardsMode": "true",
        "eventSrcSection": "Data-Portal.TeamMembersGrid",
        "pzActivity": "pzPerformGridAction",
        "skipReturnResponse": "true",
        "pySubAction": "runAct",
    }
    response = await session_manager.async_client.post(
        session_manager.details_url,
        headers=session_manager.get_standard_headers(),
        data=data,
        params=session_manager.get_standard_params(),
        follow_redirects=True
    )
    raw_html = response.text
    logger.debug(f'1st fetch_hostler_details response status: {response.status_code}, html_step#: {html_step}')
    save_html_to_file(response.content, step=html_step, enabled=session_manager.debug_html)
    html_step += 1

    hostler_details = extract_hostler_view_details(response.text) or {}
    hostler_name = get_field(hostler_details, "assigned_to", "Unknown")
    tasks = get_field(hostler_details, "tasks", []) or []

    if checker_id is None and hasattr(session_manager, "hostler_store"):
        checker_id = await session_manager.hostler_store.lookup_checker_id(hostler_name)
        if checker_id:
            hostler_info = await session_manager.hostler_store.get_hostler(checker_id)
            if hostler_info:
                total_moves = get_field(hostler_info, "moves")

    grid_fields = extract_grid_action_fields(response.text)
    selected_row_id = get_field(grid_fields, "selected_row_id")
    pyPropertyTarget = get_field(grid_fields, "pyPropertyTarget")
    base_ref_step2 = get_field(grid_fields, "base_ref")
    context_page = get_field(grid_fields, "context_page")
    pzuiactionzzz = get_field(grid_fields, "pzuiactionzzz")
    pzHarnessID = get_field(grid_fields, "pzHarnessID")

    section_id_list = extract_section_id(response.text, default=getattr(session_manager, "sectionIDList", None))
    strIndexInList = extract_str_index_in_list(response.text) or None
    team_members_pd_key = extract_team_members_pd_key(response.text) or None
    context_page_extracted = extract_context_page(response.text) or context_page

    activity_params = None

    # --- Add context fields to first page tasks ---
    for t in tasks:
        if isinstance(t, dict):
            t["selected_row_id"] = selected_row_id
            t["pyPropertyTarget"] = pyPropertyTarget
            t["base_ref"] = base_ref_step2
            t["context_page"] = context_page_extracted
            t["pzuiactionzzz"] = pzuiactionzzz
            t["pzHarnessID"] = pzHarnessID
            t["section_id_list"] = section_id_list
            t["strIndexInList"] = strIndexInList
            t["team_members_pd_key"] = team_members_pd_key
            t["activity_params"] = activity_params
        else:
            t.selected_row_id = selected_row_id
            t.pyPropertyTarget = pyPropertyTarget
            t.base_ref = base_ref_step2
            t.context_page = context_page_extracted
            t.pzuiactionzzz = pzuiactionzzz
            t.pzHarnessID = pzHarnessID
            t.section_id_list = section_id_list
            t.strIndexInList = strIndexInList
            t.team_members_pd_key = team_members_pd_key
            t.activity_params = activity_params
    all_tasks.extend(tasks)

    # --- Calculate total_pages ---
    if total_moves is not None and page_size:
        total_pages = math.ceil(total_moves / page_size)
        logger.debug(f"Total moves from Redis: {total_moves}, calculated total_pages: {total_pages}")
    else:
        total_pages = extract_total_pages_lxml(response.text)
        if not total_pages or total_pages < 1:
            logger.warning("Could not determine total_pages from Redis or HTML, defaulting to 1 page.")
            total_pages = 1
        else:
            logger.debug(f"Fallback total_pages from HTML: {total_pages}")

    pagelist_property = extract_pagelist_property(response.text,
                                                  default=session_manager.get_pagelist_property(hostler_details))
    logger.debug(f'Total pages: {total_pages}, page size: {page_size}, pagelist_property: {pagelist_property}')

    # --- Pages 2..N in parallel ---
    if total_pages > 1:
        requests = []
        for page in range(2, total_pages + 1):
            row_page = get_row_page(base_ref, page_index=page)
            start_index = (page - 1) * page_size + 1
            prev_start_index = (page - 2) * page_size + 1
            activity_params = (
                f"gridAction=PAGINATE"
                f"&gridActivity=pzGridSortPaginate"
                f"&PageListProperty={pagelist_property}"
                f"&ClassName=Assign-Worklist"
                f"&BaseReference={base_ref}"
                f"&startIndex={start_index}"
                f"&currentPageIndex={page}"
                f"&pyPageMode=Numeric"
                f"&pyPageSize={page_size}"
                f"&isReportDef=false"
                f"&prevStartIndex={prev_start_index}"
            )
            data = {
                "pyActivity": "ReloadSection",
                "SectionIDList": section_id_list,
                "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "HOME",
                "ActivityParams": activity_params,
                "BaseReference": base_ref,
                "rowPage": row_page,
                "ReadOnly": "0",
                "Increment": "true",
                "UITemplatingStatus": "N",
                "inStandardsMode": "true",
                "pzHarnessID": session_manager.pzHarnessID,
                "eventSrcSection": "ESTES-OPS-YardMgmt-Work.CaseSummary",
            }
            requests.append(session_manager.async_client.post(
                session_manager.details_url,
                headers=session_manager.get_standard_headers(),
                data=data,
                params=session_manager.get_standard_params(),
                follow_redirects=True
            ))
        responses = await asyncio.gather(*requests)

        for response in responses:
            save_html_to_file(response.content, step=html_step, enabled=session_manager.debug_html)
            html_step += 1
            hostler_details = extract_hostler_view_details(response.text) or {}
            tasks = get_field(hostler_details, "tasks", []) or []
            strIndexInList = extract_str_index_in_list(response.text) or None
            team_members_pd_key = extract_team_members_pd_key(response.text) or team_members_pd_key
            context_page_extracted = extract_context_page(response.text) or context_page
            for t in tasks:
                if isinstance(t, dict):
                    t["selected_row_id"] = selected_row_id
                    t["pyPropertyTarget"] = pyPropertyTarget
                    t["base_ref"] = base_ref_step2
                    t["context_page"] = context_page_extracted
                    t["pzuiactionzzz"] = pzuiactionzzz
                    t["pzHarnessID"] = pzHarnessID
                    t["section_id_list"] = section_id_list
                    t["strIndexInList"] = strIndexInList
                    t["team_members_pd_key"] = team_members_pd_key
                    t["activity_params"] = activity_params
                else:
                    t.selected_row_id = selected_row_id
                    t.pyPropertyTarget = pyPropertyTarget
                    t.base_ref = base_ref_step2
                    t.context_page = context_page_extracted
                    t.pzuiactionzzz = pzuiactionzzz
                    t.pzHarnessID = pzHarnessID
                    t.section_id_list = section_id_list
                    t.strIndexInList = strIndexInList
                    t.team_members_pd_key = team_members_pd_key
                    t.activity_params = activity_params
            all_tasks.extend(tasks)
            section_id_list = extract_section_id(response.text, default=section_id_list)
            pagelist_property = extract_pagelist_property(response.text, default=pagelist_property)

    # --- Validate/dedupe ---
    validated_tasks = await validate_and_store_tasks(
        all_tasks, session_manager.task_store, session_manager=session_manager
    )

    # --- Always enrich all tasks concurrently ---
    tasks_to_enrich = validated_tasks
    logger.error(f'Tasks to enrich: {[get_field(t, "case_id") for t in tasks_to_enrich]}')
    logger.error(f'Enriching {len(tasks_to_enrich)} tasks')

    if tasks_to_enrich:
        await asyncio.gather(
            *(enrich_and_store_task(session_manager, t) for t in tasks_to_enrich)
        )

    # --- Hostler upsert ---
    checker_id = await session_manager.hostler_store.lookup_checker_id(hostler_name)
    if not checker_id and getattr(session_manager, "logger", None):
        session_manager.logger.warning(
            f"Could not find checker_id for hostler '{hostler_name}', skipping hostler upsert.")
    elif checker_id:
        await session_manager.hostler_store.upsert_hostler({
            "name": hostler_name,
            "checker_id": checker_id,
            "moves": len(validated_tasks),
        })

    # --- Return all transfer-related fields along with tasks ---
    result = {
        "id": f"detail_{base_ref}",
        "name": hostler_name,
        "tasks": [
            t.model_dump() if hasattr(t, "model_dump") else t for t in validated_tasks
        ],
        "selected_row_id": selected_row_id,
        "pyPropertyTarget": pyPropertyTarget,
        "base_ref": base_ref_step2,
        "context_page": context_page_extracted,
        "pzuiactionzzz": pzuiactionzzz,
        "pzHarnessID": pzHarnessID,
        "section_id_list": section_id_list,
        "strIndexInList": strIndexInList,
        "team_members_pd_key": team_members_pd_key,
        "activity_params": activity_params,
    }
    if step1_grid_action:
        result["raw_html"] = response.text

    logger.info(f"Hostler {hostler_name} extracted tasks: {result['tasks']}")
    return result
