import re
from lxml import html


def extract_pzuiactionzzz(html_text):
    tree = html.fromstring(html_text)
    # 1. data-postvalue-url (for grid selection)
    for el in tree.xpath("//*[contains(@data-postvalue-url, 'pzuiactionzzz=')]"):
        val = el.attrib.get('data-postvalue-url') or ""
        match = re.search(r'pzuiactionzzz=([A-Za-z0-9%*=]+)', val)
        if match:
            return match.group(1), 'postvalue-url'
    # 2. fallback: first found in a button (for modal submit)
    for el in tree.xpath("//button[contains(@data-click, 'pzuiactionzzz=')]"):
        data_click = el.attrib.get('data-click') or ""
        match = re.search(r'pzuiactionzzz=([A-Za-z0-9%*=]+)', data_click)
        if match:
            return match.group(1), 'button'
    return None, None


# Usage:
with open('step_3000.html', 'r') as reader:
    html_text = reader.read()
pzuiactionzzz, source = extract_pzuiactionzzz(html_text)
print(f"{pzuiactionzzz}")
