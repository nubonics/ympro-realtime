import re
from lxml import html


def extract_total_pages_lxml(html_text):
    tree = html.fromstring(html_text)
    paginator_elems = tree.xpath('//a[@id="pyGridActivePage"]')
    for elem in paginator_elems:
        aria = elem.attrib.get("aria-label", "")
        m = re.search(r"Page \d+ of (\d+)", aria)
        if m:
            return int(m.group(1))
    all_a = tree.xpath('//a[@aria-label]')
    for elem in all_a:
        aria = elem.attrib.get("aria-label", "")
        m = re.search(r"Page \d+ of (\d+)", aria)
        if m:
            return int(m.group(1))
    return 1


def extract_section_id(html_text, default=None):
    tree = html.fromstring(html_text)
    for div in tree.xpath('//div[@id="RULE_KEY"]'):
        sid = div.attrib.get("containedsectionid")
        if sid:
            return sid
    for inp in tree.xpath('//input[@name="SectionIDList"]'):
        v = inp.attrib.get("value")
        if v:
            return v
    return default


def extract_pagelist_property(html_text, default=None):
    m = re.search(r'PageListProperty=([A-Za-z0-9_\.]+)', html_text)
    if m:
        return m.group(1)
    return default


def build_location_params(base_ref, pzHarnessID):
    location_params = {
        "pyActivity": "pzPrepareAssignment",
        "UITemplatingStatus": "Y",
        "NewTaskStatus": "DisplayUserWorkList",
        "TaskIndex": "",
        "StreamType": "Rule-HTML-Section",
        "FieldError": "",
        "FormError": "",
        "pyCustomError": "",
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
        "rowPage": base_ref,
        "GridAction": "true",
        "BaseThread": "STANDARD",
        "pzHarnessID": pzHarnessID,
    }
    return "&".join(f"{key}={value}" for key, value in location_params.items())


def extract_team_members_pd_key(html_text):
    """
    Extract the team_members_pd_key from PEGA_GRID_CONTENT grid markup.
    This finds patterns like: $PD_TeamMembersByWorkGroup_pa1250782387459524pz$ppxResults$l11$ppySelected
    Returns the first such key found, or None if not found.
    """
    # Use lxml to parse the HTML
    tree = html.fromstring(html_text)
    # Find all input elements with name starting with $PD_TeamMembersByWorkGroup
    input_elems = tree.xpath("//input[starts-with(@name, '$PD_TeamMembersByWorkGroup')]")
    for inp in input_elems:
        name = inp.attrib.get("name", "")
        # Usually want the part up to ...ppySelected (full key used in transfer)
        if name.endswith("$ppySelected"):
            return name
    # Fallback: regex search if lxml fails (for robustness)
    m = re.search(r"\$PD_TeamMembersByWorkGroup[^'\"]+\$ppySelected", html_text)
    if m:
        return m.group(0)
    return None


def extract_context_page(html_text):
    tree = html.fromstring(html_text)
    # Try the BASE_REF attribute first
    div = tree.xpath("//div[@BASE_REF]")
    if div:
        return div[0].attrib.get("BASE_REF")
    # Fallback: try GRID_REF_PAGE
    table = tree.xpath("//table[@GRID_REF_PAGE]")
    if table:
        return table[0].attrib.get("GRID_REF_PAGE")
    return None


def extract_str_index_list(html_text):
    # Find pattern like $ppxResults$l11$ppySelected
    m = re.search(r"\$ppxResults\$(l\d+)\$ppySelected", html_text)
    if m:
        return m.group(1)  # returns 'l11'
    return None


def extract_first_pzuiactionzzz(html_text):
    """
    Extract the first pzuiactionzzz value from a data-click attribute in a button.
    Looks for a pattern like: pzuiactionzzz=... inside a JSON-ish string.
    """
    # Parse the HTML
    tree = html.fromstring(html_text)
    # Find all buttons with a data-click attribute
    buttons = tree.xpath("//button[@data-click]")
    for btn in buttons:
        data_click = btn.attrib.get("data-click", "")
        # Search for pzuiactionzzz=... (not quoted)
        m = re.search(r"pzuiactionzzz=([A-Za-z0-9%=\*]+)", data_click)
        if m:
            return m.group(1)
    # Fallback: regex over the whole HTML (handles data-postvalue-url or anywhere else)
    m = re.search(r"pzuiactionzzz=([A-Za-z0-9%=\*]+)", html_text)
    if m:
        return m.group(1)
    return None
