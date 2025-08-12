import re
import uuid
from urllib.parse import urlencode, quote

from lxml import html

from backend.modules.colored_logger import setup_logger
from backend.pega.yard_coordinator.session_manager.debug import save_html_to_file

logger = setup_logger(__name__)


class DeleteTask:
    def __init__(self, task_id, session_manager):
        self.pzuiactionzzz = None
        self.pzHarnessID = None
        self.content_id = str(uuid.uuid4())
        self.dynamicContainerID = str(uuid.uuid4())
        self.session = session_manager
        self.task_id = task_id
        self.ajax_track_id = 1
        self.key = f"ESTES-OPS-YARDMGMT-WORK {self.task_id}"
        self.assignment_handle = f"ESTES-OPS-YARDMGMT-WORK%20{self.task_id}"

    @staticmethod
    def extract_action_token(html_text):
        matches = re.findall(r'([A-Za-z0-9+=*/]{330,350})', html_text)
        counter = 0
        for token in matches:
            if 330 <= len(token) <= 350:
                token = token.replace('u003d', '')
                # print(f'counter: {counter}')
                # print(f'token: {token}')
                # counter += 1
                return token
        logger.error('Unable to find pzuiactionzzz for open_task_pzuiactionzzz')
        return None

    @staticmethod
    def extract_pzHarnessID(html_text):
        tree = html.fromstring(html_text)
        pzHarnessID_elements = tree.xpath("//input[@id='pzHarnessID']")
        return pzHarnessID_elements[0].get("value") if pzHarnessID_elements else None

    async def run(self):
        await self.open_task()
        # await self.reload_after_ok()
        await self.open_delete_modal()
        await self.confirm_delete_modal()
        await self.submit_confirm_delete()
        # await self.finish_assignment()
        await self.do_close()
        await self.reload_after_ok()
        await self.load_dashboard()  # this is the visual refresh

    async def open_task(self):
        logger.info("[Step 1] Opening task via openWorkByHandle")
        self.session.async_client.headers.update(
            {
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://ymg.estes-express.com/prweb/app/YardMgmt/<sessionid>*/!STANDARD?pzPostData=...",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://ymg.estes-express.com",
                # Add if present in network traffic:
                "pzBFP": self.session.fingerprint_token,
                "pzCTkn": self.session.csrf_token,
            }
        )
        logger.debug(f'{self.session.async_client.headers}')
        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")

        payload = {
            "pyActivity": "@baseclass.doUIAction",
            "isDCSPA": "true",
            "isSDM": "true",
            "action": "openWorkByHandle",
            "key": self.key,
            "SkipConflictCheck": "false",
            "reload": "false",
            "api": "openWorkByHandle",
            "contentID": self.content_id,
            "dynamicContainerID": self.dynamicContainerID,
            "portalName": "YardCoordinator",
            "portalThreadName": "STANDARD",
            "tabIndex": "1",
            "pzHarnessID": self.session.pzHarnessID,
            "UITemplatingStatus": "Y",
            "inStandardsMode": "true",
            "eventSrcSection": "Data-Portal.PortalNavigation",
        }

        for name in [
            "CompositeGadget", "ControlMenu", "DesktopWrapperInclude", "DeterminePortalTop",
            "DynamicContainerFrameLess", "DynamicLayout", "DynamicLayoutCell", "EvalDOMScripts_Include", "Form",
            "GapIdentifier", "GridInc", "Harness", "HarnessStaticJSEnd", "HarnessStaticJSStart",
            "HarnessStaticScriptsClientValidation", "HarnessStaticScriptsExprCal", "LaunchFlow", "MenuBar",
            "MenuBarOld", "MobileAppNotify", "OperatorPresenceStatusScripts", "PMCPortalStaticScripts",
            "RepeatingDynamicLayout", "SessionUser", "SurveyStaticScripts", "WorkformStyles", "cosmoslocale",
            "menubarInclude", "pxButton", "pxDisplayText", "pxDropdown", "pxDynamicContainer", "pxHarnessContent",
            "pxHeaderCell", "pxHidden", "pxIcon", "pxLayoutContainer", "pxLayoutHeader", "pxLink", "pxMenu",
            "pxNonTemplate", "pxSection", "pxTextInput", "pxVisible", "pxWorkArea", "pxWorkAreaContent",
            "pyDirtyCheckConfirm", "pyWorkFormStandardEnd", "pyWorkFormStandardStart", "pycosmoscustomstyles",
            "pzAppLauncher", "pzDecimalInclude", "pzFrameLessDCScripts", "pzHarnessInlineScriptsEnd",
            "pzHarnessInlineScriptsStart", "pzPegaCompositeGadgetScripts", "pzRuntimeToolsBar",
            "pzpega_ui_harnesscontext", "rdlincludes", "xmlDocumentInclude", "LGBundle", "LayoutGroup",
            "MicroDynamicContainer", "NewActionSection", "PegaSocial", "pxMicroDynamicContainer", "pxTextArea",
            "pxWorkAreaHeader", "pycosmoscustomscripts", "pzMicroDynamicContainerScripts", "pzTextIncludes",
            "pzcosmosuiscripts", "pzpega_control_attachcontent", "pxCheckbox", "pxAutoComplete", "pxRadioButtons",
            "pzAutoCompleteAGIncludes", "Checkbox"
        ]:
            payload[f"$O{name}"] = ""

        res = await self.session.async_client.post(url, data=payload)
        if res.status_code == 303 and "location" in res.headers:
            follow = await self.session.async_client.get(res.headers["location"])
            self.pzHarnessID = self.extract_pzHarnessID(follow.text)
            save_html_to_file(follow.text, 1031, enabled=self.session.debug_html)
        logger.debug(f"[Step 1] openWorkByHandle status={res.status_code}")

    async def open_delete_modal(self):
        logger.info("[Step 2] Opening delete modal (ProcessAction)")
        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": self.ajax_track_id,
            "eventSrcSection": "Data-Portal.PortalNavigation"
        }

        payload = {
            "pyActivity": "ProcessAction",
            "$PpyWorkPage$ppyInternalAssignmentHandle": f"ASSIGN-INTERNAL ESTES-OPS-YARDMGMT-WORK {self.task_id}!PZINTERNALCASEFLOW",
            "HarnessType": "Review",
            "Purpose": "Review",
            "UITemplatingStatus": "Y",
            "NewTaskStatus": "DeleteTask",
            "StreamType": "Rule-HTML-Section",
            "FormError": "NONE",
            "pyCustomError": "pyCaseErrorSection",
            "bExcludeLegacyJS": "true",
            "ModalSection": "pzModalTemplate",
            "IgnoreSectionSubmit": "true",
            "bInvokedFromControl": "true",
            "isModalFlowAction": "true",
            "bIsModal": "true",
            "bIsOverlay": "false",
            "StreamClass": "Rule-HTML-Section",
            "UITemplatingScriptLoad": "true",
            "ActionSection": "pzModalTemplate",
            "pzHarnessID": self.pzHarnessID,
            "inStandardsMode": "true",
            # "pzuiactionzzz": self.session.open_task_pzuiactionzzz,
            "modalStyle": "",
            "BaseReference": "",
            "TaskIndex": "",
            "FieldError": "",
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "HOME",
        }

        for name in [
            "CompositeGadget", "ControlMenu", "DesktopWrapperInclude", "DeterminePortalTop",
            "DynamicContainerFrameLess", "DynamicLayout", "DynamicLayoutCell", "EvalDOMScripts_Include",
            "Form", "GapIdentifier", "GridInc", "Harness", "HarnessStaticJSEnd", "HarnessStaticJSStart",
            "HarnessStaticScriptsClientValidation", "HarnessStaticScriptsExprCal", "LaunchFlow", "MenuBar",
            "MenuBarOld", "MobileAppNotify", "OperatorPresenceStatusScripts", "PMCPortalStaticScripts",
            "RepeatingDynamicLayout", "SessionUser", "SurveyStaticScripts", "WorkformStyles", "cosmoslocale",
            "menubarInclude", "pxButton", "pxDisplayText", "pxDropdown", "pxDynamicContainer", "pxHidden", "pxIcon",
            "pxLayoutContainer", "pxLayoutHeader", "pxLink", "pxMenu", "pxNonTemplate", "pxSection", "pxTextInput",
            "pxVisible", "pyWorkFormStandardEnd", "pyWorkFormStandardStart", "pycosmoscustomstyles", "pzAppLauncher",
            "pzDecimalInclude", "pzFrameLessDCScripts", "pzHarnessInlineScriptsEnd", "pzHarnessInlineScriptsStart",
            "pzPegaCompositeGadgetScripts", "pzRuntimeToolsBar", "pzpega_ui_harnesscontext", "rdlincludes",
            "xmlDocumentInclude", "LayoutGroup", "MicroDynamicContainer", "PegaSocial", "pxMicroDynamicContainer",
            "pxTextArea", "pxWorkArea", "pxWorkAreaContent", "pxWorkAreaHeader", "pyDirtyCheckConfirm",
            "pycosmoscustomscripts", "pzLocalActionScript", "pzMicroDynamicContainerScripts", "pzTextIncludes",
            "pzcosmosuiscripts", "pzpega_control_attachcontent", "pxRadioButtons"
        ]:
            payload[f"$O{name}"] = ""

        res = await self.session.async_client.post(url, params=params, data=payload)
        if res.status_code == 303 and "location" in res.headers:
            follow = await self.session.async_client.get(res.headers["location"])
            self.pzuiactionzzz = self.extract_action_token(html_text=follow.text)
            save_html_to_file(follow.text, 1032, enabled=self.session.debug_html)
            logger.debug(f"[Step 2] Modal loaded status={follow.status_code}")

    async def confirm_delete_modal(self):
        logger.info("[Step 3] Confirming Delete Modal (OK button equivalent)")

        query_params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": str(self.ajax_track_id + 1),
            "eventSrcSection": "Data-Portal.PortalNavigation"
        }

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        url_with_query = f"{url}?{urlencode(query_params)}"

        payload = {
            "pyActivity": "ProcessAction",
            "$PpyWorkPage$ppyInternalAssignmentHandle": f"ASSIGN-INTERNAL ESTES-OPS-YARDMGMT-WORK {self.task_id}!PZINTERNALCASEFLOW",
            "HarnessType": "Review",
            "Purpose": "Review",
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "HOME",
            "UITemplatingStatus": "Y",
            "NewTaskStatus": "DeleteTask",
            "TaskIndex": "",
            "StreamType": "Rule-HTML-Section",
            "FieldError": "",
            "FormError": "NONE",
            "pyCustomError": "pyCaseErrorSection",
            "bExcludeLegacyJS": "true",
            "ModalSection": "pzModalTemplate",
            "modalStyle": "",
            "IgnoreSectionSubmit": "true",
            "bInvokedFromControl": "true",
            "BaseReference": "",
            "isModalFlowAction": "true",
            "bIsModal": "true",
            "bIsOverlay": "false",
            "StreamClass": "Rule-HTML-Section",
            "UITemplatingScriptLoad": "true",
            "ActionSection": "pzModalTemplate",
            "pzHarnessID": self.pzHarnessID,
            "inStandardsMode": "true",
            # "pzuiactionzzz": self.session.open_task_pzuiactionzzz,
            "pzuiactionzzz": self.pzuiactionzzz,
        }

        # Add all empty $O fields like before
        for name in [
            "CompositeGadget", "ControlMenu", "DesktopWrapperInclude", "DeterminePortalTop",
            "DynamicContainerFrameLess", "DynamicLayout", "DynamicLayoutCell", "EvalDOMScripts_Include",
            "Form", "GapIdentifier", "GridInc", "Harness", "HarnessStaticJSEnd", "HarnessStaticJSStart",
            "HarnessStaticScriptsClientValidation", "HarnessStaticScriptsExprCal", "LaunchFlow", "MenuBar",
            "MenuBarOld", "MobileAppNotify", "OperatorPresenceStatusScripts", "PMCPortalStaticScripts",
            "RepeatingDynamicLayout", "SessionUser", "SurveyStaticScripts", "WorkformStyles", "cosmoslocale",
            "menubarInclude", "pxButton", "pxDisplayText", "pxDropdown", "pxDynamicContainer", "pxHidden", "pxIcon",
            "pxLayoutContainer", "pxLayoutHeader", "pxLink", "pxMenu", "pxNonTemplate", "pxSection", "pxTextInput",
            "pxVisible", "pyWorkFormStandardEnd", "pyWorkFormStandardStart", "pycosmoscustomstyles", "pzAppLauncher",
            "pzDecimalInclude", "pzFrameLessDCScripts", "pzHarnessInlineScriptsEnd", "pzHarnessInlineScriptsStart",
            "pzPegaCompositeGadgetScripts", "pzRuntimeToolsBar", "pzpega_ui_harnesscontext", "rdlincludes",
            "xmlDocumentInclude", "LayoutGroup", "MicroDynamicContainer", "PegaSocial", "pxMicroDynamicContainer",
            "pxTextArea", "pxWorkArea", "pxWorkAreaContent", "pxWorkAreaHeader", "pyDirtyCheckConfirm",
            "pycosmoscustomscripts", "pzLocalActionScript", "pzMicroDynamicContainerScripts", "pzTextIncludes",
            "pzcosmosuiscripts", "pzpega_control_attachcontent", "Checkbox", "LGBundle", "OpxHarnessContent",
            "OpxHeaderCell", "ListView_FilterPanel_Btns", "ListView_header", "RepeatingGrid",
            "pxGrid", "pxGridBody", "pxGridDataCell", "pxGridDataRow", "pxGridHeaderCell", "pxGridHeaderRow"
        ]:
            payload[f"$O{name}"] = ""

        res = await self.session.async_client.post(url_with_query, data=payload)
        if res.status_code == 303 and "location" in res.headers:
            follow = await self.session.async_client.get(res.headers["location"])
            self.session.delete_task_pzuiactionzzz = self.extract_action_token(html_text=follow.text)
            save_html_to_file(follow.text, 1033, enabled=self.session.debug_html)
            logger.debug(f"[Step 3] Confirm delete modal status={follow.status_code}")
        else:
            save_html_to_file(res.text, 1033, enabled=self.session.debug_html)
            logger.warning(f"[Step 3] Modal POST failed with status={res.status_code}")

    async def submit_confirm_delete(self):
        logger.info("[Step 3.5] Submitting confirm delete form")

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        params = {
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": str(self.ajax_track_id + 2),
            "eventSrcSection": "Data-Portal.PortalNavigation"
        }

        payload = {
            "pzuiactionzzz": self.pzuiactionzzz,  # Must be the latest value extracted from the modal HTML
            "AssignmentID": self.assignment_handle,  # e.g. "ESTES-OPS-YARDMGMT-WORK%20T-34404601"
            "pzActivityParams": "AssignmentID",
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "HOME",
            "UITemplatingStatus": "N",
            "inStandardsMode": "true",
            "pzHarnessID": self.pzHarnessID,
            "eventSrcSection": "Data-Portal.PortalNavigation",
        }

        # Add all $O... fields as empty strings (these are required by Pega)
        for name in [
            "CompositeGadget", "ControlMenu", "DesktopWrapperInclude", "DeterminePortalTop",
            "DynamicContainerFrameLess", "DynamicLayout", "DynamicLayoutCell", "EvalDOMScripts_Include",
            "Form", "GapIdentifier", "GridInc", "Harness", "HarnessStaticJSEnd", "HarnessStaticJSStart",
            "HarnessStaticScriptsClientValidation", "HarnessStaticScriptsExprCal", "LaunchFlow", "MenuBar",
            "MenuBarOld", "MobileAppNotify", "OperatorPresenceStatusScripts", "PMCPortalStaticScripts",
            "RepeatingDynamicLayout", "SessionUser", "SurveyStaticScripts", "WorkformStyles", "cosmoslocale",
            "menubarInclude", "pxButton", "pxDisplayText", "pxDropdown", "pxDynamicContainer", "pxHarnessContent",
            "pxHeaderCell", "pxHidden", "pxIcon", "pxLayoutContainer", "pxLayoutHeader", "pxLink", "pxMenu",
            "pxNonTemplate", "pxSection", "pxTextInput", "pxVisible", "pxWorkArea", "pxWorkAreaContent",
            "pyDirtyCheckConfirm", "pyWorkFormStandardEnd", "pyWorkFormStandardStart", "pycosmoscustomstyles",
            "pzAppLauncher", "pzDecimalInclude", "pzFrameLessDCScripts", "pzHarnessInlineScriptsEnd",
            "pzHarnessInlineScriptsStart", "pzPegaCompositeGadgetScripts", "pzRuntimeToolsBar",
            "pzpega_ui_harnesscontext", "rdlincludes", "xmlDocumentInclude", "LGBundle", "LayoutGroup",
            "MicroDynamicContainer", "NewActionSection", "PegaSocial", "pxMicroDynamicContainer", "pxTextArea",
            "pxWorkAreaHeader", "pycosmoscustomscripts", "pzMicroDynamicContainerScripts", "pzTextIncludes",
            "pzcosmosuiscripts", "pzpega_control_attachcontent", "pxAutoComplete", "pxRadioButtons",
            "pzAutoCompleteAGIncludes", "pzRadiogroupIncludes", "Checkbox", "ListView_FilterPanel_Btns",
            "ListView_header", "RepeatingGrid", "pxGrid", "pxGridBody", "pxGridDataCell", "pxGridDataRow",
            "pxGridHeaderCell", "pxGridHeaderRow", "OpxHarnessContent", "OpxHeaderCell", "OLGBundle",
            "OLayoutGroup", "OListView_FilterPanel_Btns", "OListView_header", "OMicroDynamicContainer",
            "OPegaSocial", "ORepeatingGrid", "OpxGrid", "OpxGridBody", "OpxGridDataCell", "OpxGridDataRow",
            "OpxGridHeaderCell", "OpxGridHeaderRow", "OpxMicroDynamicContainer", "OpxTextArea", "OpxWorkAreaHeader",
            "Opycosmoscustomscripts", "OpzLocalActionScript", "OpzMicroDynamicContainerScripts", "OpzTextIncludes",
            "Opzcosmosuiscripts", "Opzpega_control_attachcontent"
        ]:
            payload[f"${'O' if not name.startswith('O') else ''}{name}"] = ""

        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": self.session.base_url.replace("!DCSPA_YardCoordinator", "!STANDARD"),
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://ymg.estes-express.com",
            "pzBFP": self.session.fingerprint_token,
            "pzCTkn": self.session.csrf_token,
            # Add cookies via your session manager
        }

        res = await self.session.async_client.post(url, params=params, data=payload, headers=headers)
        logger.debug(f'[Step 3.5] status code: {res.status_code}')
        if res.status_code == 303 and "location" in res.headers:
            redirected = await self.session.async_client.get(res.headers["location"])
            save_html_to_file(redirected.text, 1033.5, enabled=self.session.debug_html)
            logger.debug(f"[Step 3.5] Submit confirm delete redirect status={redirected.status_code}")
        else:
            save_html_to_file(res.text, 1033.5, enabled=self.session.debug_html)
            logger.warning(f"[Step 3.5] Submit confirm delete failed status={res.status_code}")

    async def do_close(self):
        logger.info("[Step 4] Running DoClose to finalize delete flow")

        params = {
            "pyActivity": "DoClose",
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "pyRemCtlExpProp": "true",
            "pzHarnessID": self.pzHarnessID,
            "AJAXTrackID": str(self.ajax_track_id + 2),
            "retainLock": "false",
            "dcCleanup": "true",
            "eventSrcSection": "Data-Portal.PortalNavigation"
        }

        # !STANDARD is used in the Referer
        referer_url = self.session.base_url.replace("!DCSPA_YardCoordinator", "!STANDARD")

        url = self.session.base_url.replace("!STANDARD", "!DCSPA_YardCoordinator")
        headers = {
            "Referer": referer_url
        }

        res = await self.session.async_client.get(url, params=params, headers=headers)
        if res.status_code == 303 and "location" in res.headers:
            redirected = await self.session.async_client.get(res.headers["location"])
            save_html_to_file(redirected.text, 1034, enabled=self.session.debug_html)
            logger.debug(f"[Step 4] DoClose redirect status={redirected.status_code}")
        else:
            save_html_to_file(res.text, 1034, enabled=self.session.debug_html)
            logger.warning(f"[Step 4] DoClose failed with status={res.status_code}")

    async def reload_after_ok(self):
        logger.info("[Step 4] Reloading section to commit deletion")
        url = self.session.base_url

        payload = {
            "pyActivity": "ReloadSection",
            "AJAXTrackID": str(self.ajax_track_id + 3),
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            # "pzuiactionzzz": self.session.open_task_pzuiactionzzz,
            "pzuiactionzzz": self.pzuiactionzzz,
            "dynamicContainerID": self.dynamicContainerID,
            "contentID": self.content_id,
            "pySection": "pzModalTemplate",
            "pyWorkPage": "pyWorkPage",
            "streamClass": "ESTES-OPS-YARDMGMT-WORK-TASK",
            "streamName": "pzModalTemplate",
            "bUseNewThread": "true",
            "ajax": "true",
        }

        res = await self.session.async_client.post(url, data=payload)
        if res.status_code == 303 and "location" in res.headers:
            redirected = await self.session.async_client.get(res.headers["location"])
            save_html_to_file(redirected.text, 1034, enabled=self.session.debug_html)
            logger.debug(f"[Step 4] Reload section status={redirected.status_code}")

    async def finish_assignment(self):
        logger.info("[Step 5] Finishing assignment")
        url = self.session.base_url

        payload = {
            "pyActivity": "FinishAssignment",
            "pzTransactionId": self.session.pzTransactionId,
            "pzFromFrame": "pyWorkPage",
            "pzPrimaryPageName": "pyWorkPage",
            "AJAXTrackID": str(self.ajax_track_id + 4),
            # "pzuiactionzzz": self.session.open_task_pzuiactionzzz,
            "pzuiactionzzz": self.pzuiactionzzz,
            "pyPrimaryPageName": "pyWorkPage",
            "HarnessPurpose": "Review",
            "purpose": "Review",
            "AssignmentID": self.assignment_handle,
        }

        res = await self.session.async_client.post(url, data=payload)
        if res.status_code == 303 and "location" in res.headers:
            redirected = await self.session.async_client.get(res.headers["location"])
            save_html_to_file(redirected.text, 1035, enabled=self.session.debug_html)
            logger.debug(f"[Step 5] FinishAssignment status={redirected.status_code}")

    async def load_dashboard(self):
        logger.info("[Step 6] Reloading dashboard to finalize visual refresh")

        url = self.session.base_url.replace("!DCSPA_YardCoordinator", "!STANDARD")

        payload = {
            "isDCSPA": "true",
            "AJAXTrackID": str(self.ajax_track_id + 5),
            "$PDeclare_pyDisplay$ppyDCDisplayState$ppyActiveDocumentType": "WORK",
            "isURLReady": "true",
            "api": "activate",
            "UITemplatingStatus": "Y",
            "inStandardsMode": "true",
            "pzHarnessID": self.session.pzHarnessID,  # Use the latest harness ID if updated
        }

        # Append all $O... keys as empty string
        payload.update({
            key: "" for key in [
                "$OCompositeGadget", "$OControlMenu", "$ODesktopWrapperInclude", "$ODeterminePortalTop",
                "$ODynamicContainerFrameLess", "$ODynamicLayout", "$ODynamicLayoutCell", "$OEvalDOMScripts_Include",
                "$OGapIdentifier", "$OHarnessStaticJSEnd", "$OHarnessStaticJSStart",
                "$OHarnessStaticScriptsClientValidation", "$OHarnessStaticScriptsExprCal", "$OLaunchFlow",
                "$OMenuBar", "$OMenuBarOld", "$OMobileAppNotify", "$OOperatorPresenceStatusScripts",
                "$OPMCPortalStaticScripts", "$ORepeatingDynamicLayout", "$OSessionUser", "$OSurveyStaticScripts",
                "$OWorkformStyles", "$Ocosmoslocale", "$OmenubarInclude", "$OpxButton", "$OpxDisplayText",
                "$OpxDropdown", "$OpxDynamicContainer", "$OpxHidden", "$OpxIcon", "$OpxLayoutContainer",
                "$OpxLayoutHeader", "$OpxLink", "$OpxMenu", "$OpxNonTemplate", "$OpxSection", "$OpxTextInput",
                "$OpxVisible", "$OpyWorkFormStandardEnd", "$OpyWorkFormStandardStart", "$Opycosmoscustomstyles",
                "$OpzAppLauncher", "$OpzDecimalInclude", "$OpzFrameLessDCScripts", "$OpzHarnessInlineScriptsEnd",
                "$OpzHarnessInlineScriptsStart", "$OpzPegaCompositeGadgetScripts", "$OpzRuntimeToolsBar",
                "$Opzpega_ui_harnesscontext", "$Ordlincludes", "$OxmlDocumentInclude", "$OForm", "$OGridInc",
                "$OHarness", "$OpxHarnessContent", "$OpxHeaderCell", "$OpxWorkArea", "$OpxWorkAreaContent",
                "$OpyDirtyCheckConfirm", "$OCheckbox", "$OLGBundle", "$OLayoutGroup", "$OListView_FilterPanel_Btns",
                "$OListView_header", "$OMicroDynamicContainer", "$OPegaSocial", "$ORepeatingGrid", "$OpxGrid",
                "$OpxGridBody", "$OpxGridDataCell", "$OpxGridDataRow", "$OpxGridHeaderCell", "$OpxGridHeaderRow",
                "$OpxMicroDynamicContainer", "$OpxTextArea", "$OpxWorkAreaHeader", "$Opycosmoscustomscripts",
                "$OpzLocalActionScript", "$OpzMicroDynamicContainerScripts", "$OpzTextIncludes",
                "$Opzcosmosuiscripts", "$Opzpega_control_attachcontent",
            ]
        })

        headers = {
            "Referer": url,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        res = await self.session.async_client.post(url, data=payload, headers=headers)
        save_html_to_file(res.text, 1036, enabled=self.session.debug_html)
        logger.debug(f"[Step 6] Dashboard reload status={res.status_code}")
        if res.status_code == 303 and "location" in res.headers:
            redirected = await self.session.async_client.get(res.headers["location"])
            save_html_to_file(redirected.text, 1036, enabled=self.session.debug_html)
            logger.debug(f"[Step 6] Dashboard redirect status={redirected.status_code}")
        else:
            logger.warning(f"[Step 6] Dashboard reload failed with status={res.status_code}")
