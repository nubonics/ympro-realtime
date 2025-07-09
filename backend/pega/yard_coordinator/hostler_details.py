from .hostler_utils import (
    extract_total_pages_lxml,
    extract_section_id,
    extract_pagelist_property,
    build_location_params,
    extract_team_members_pd_key,
    extract_context_page,
    extract_str_index_list,
    extract_first_pzuiactionzzz,
)
from .session_manager.pega_parser import extract_hostler_view_details
from ...modules.colored_logger import setup_logger
from ...rules.validation import validate_and_store_tasks
import math
import json

logger = setup_logger(__name__)


async def fetch_hostler_details(session_manager, base_ref, page_size=10, step1_grid_action=False):
    all_tasks = []
    if step1_grid_action is False:
        html_step = 30
    elif step1_grid_action:
        html_step = 3000
    else:
        raise ValueError("Invalid step1_grid_action value, must be True or False.")

    # --- Extract checker_id from base_ref or another context ---
    checker_id = None
    # Try to get checker_id from hostler_store using base_ref, or pass checker_id as a param for clarity.

    # --- Get total moves from Redis ---
    total_moves = None
    if checker_id:
        hostler_info = await session_manager.task_store.get_hostler(f"hostler:{checker_id}")
        if hostler_info:
            try:
                hostler_info = json.loads(hostler_info)
                total_moves = hostler_info.get("moves")
            except Exception as e:
                logger.warning(f"Failed to parse hostler_info JSON for {checker_id}: {e}")

    # --- First page ---
    location_params_str = build_location_params(base_ref, session_manager.pzHarnessID)
    data = {
        "pyActivity": "pzRunActionWrapper",
        "rowPage": base_ref,
        "Location": location_params_str,
        "PagesToCopy": base_ref.split(".pxResults")[0],
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
    logger.debug(f'1st fetch_hostler_details response status: {response.status_code}, html_step#: {html_step}')
    if getattr(session_manager, "save_html_to_file", None):
        session_manager.save_html_to_file(response.content, step=html_step,
                                          enabled=getattr(session_manager, "debug_html", False))
    html_step += 1

    hostler_details = extract_hostler_view_details(response.text) or {}
    hostler_name = hostler_details.get("assigned_to", "Unknown")
    tasks = hostler_details.get("tasks", []) or []

    # Try to get checker_id if not set yet
    if checker_id is None and hasattr(session_manager, "hostler_store"):
        checker_id = await session_manager.hostler_store.lookup_checker_id(hostler_name)
        if checker_id:
            hostler_info = await session_manager.task_store.get_hostler(f"hostler:{checker_id}")
            if hostler_info:
                try:
                    hostler_info = json.loads(hostler_info)
                    total_moves = hostler_info.get("moves")
                except Exception as e:
                    logger.warning(f"Failed to parse hostler_info JSON for {checker_id}: {e}")

    # Gather all transfer-relevant fields:
    fetch_worklist_pd_key = hostler_details.get("fetch_worklist_pd_key") or base_ref.split(".pxResults")[0]
    team_members_pd_key = extract_team_members_pd_key(html_text=response.text)
    section_id_list = extract_section_id(response.text, default=getattr(session_manager, "sectionIDList", None))
    pzuiactionzzz = extract_first_pzuiactionzzz(html_text=response.text)
    row_page = base_ref
    context_page = extract_context_page(html_text=response.text)
    strIndexInList = extract_str_index_list(html_text=response.text)
    activity_params = None  # Will be set in the loop

    # --- Add context fields to first page tasks ---
    for t in tasks:
        t["fetch_worklist_pd_key"] = fetch_worklist_pd_key
        t["team_members_pd_key"] = team_members_pd_key
        t["section_id_list"] = section_id_list
        t["pzuiactionzzz"] = pzuiactionzzz
        t["row_page"] = row_page
        t["base_ref"] = base_ref
        t["context_page"] = context_page
        t["strIndexInList"] = strIndexInList
        t["activity_params"] = activity_params
    all_tasks.extend(tasks)

    # --- Calculate total_pages using total_moves from Redis, fallback to 1 if not available ---
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

    # --- Pages 2..N (short-circuit if only one page) ---
    if total_pages > 1:
        for page in range(2, total_pages + 1):
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
                "ReadOnly": "0",
                "Increment": "true",
                "UITemplatingStatus": "N",
                "inStandardsMode": "true",
                "pzHarnessID": session_manager.pzHarnessID,
                "eventSrcSection": "ESTES-OPS-YardMgmt-Work.CaseSummary",
            }
            response = await session_manager.async_client.post(
                session_manager.details_url,
                headers=session_manager.get_standard_headers(),
                data=data,
                params=session_manager.get_standard_params(),
                follow_redirects=True
            )
            if getattr(session_manager, "save_html_to_file", None):
                session_manager.save_html_to_file(response.content, step=html_step,
                                                  enabled=getattr(session_manager, "debug_html", False))
            html_step += 1

            hostler_details = extract_hostler_view_details(response.text) or {}
            tasks = hostler_details.get("tasks", []) or []
            # Enrich each task with context for this page
            for t in tasks:
                t["fetch_worklist_pd_key"] = fetch_worklist_pd_key
                t["team_members_pd_key"] = team_members_pd_key
                t["section_id_list"] = section_id_list
                t["pzuiactionzzz"] = pzuiactionzzz
                t["row_page"] = row_page
                t["base_ref"] = base_ref
                t["context_page"] = context_page
                t["strIndexInList"] = strIndexInList
                t["activity_params"] = activity_params
            all_tasks.extend(tasks)
            # Always update for next page (if needed)
            section_id_list = extract_section_id(response.text, default=section_id_list)
            pagelist_property = extract_pagelist_property(response.text, default=pagelist_property)

    # --- Business validation/deduplication ---
    validated_tasks = await validate_and_store_tasks(all_tasks, session_manager.task_store,
                                                     session_manager=session_manager)
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
    return {
        "id": f"detail_{base_ref}",
        "name": hostler_name,
        "tasks": [task.model_dump() for task in validated_tasks],
        "fetch_worklist_pd_key": fetch_worklist_pd_key,
        "team_members_pd_key": team_members_pd_key,
        "section_id_list": section_id_list,
        "pzuiactionzzz": pzuiactionzzz,
        "row_page": row_page,
        "base_ref": base_ref,
        "context_page": context_page,
        "strIndexInList": strIndexInList,
        "activity_params": activity_params,
    }
