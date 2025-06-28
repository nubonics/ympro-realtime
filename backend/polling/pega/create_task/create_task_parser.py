import re
import urllib
import json
from lxml import html
from backend.colored_logger import setup_logger

logger = setup_logger(__name__)


def parse_html(html_content: str):
    try:
        return html.fromstring(html_content)
    except Exception as e:
        logger.error("Failed to parse HTML: %s", e)
        return None


def extract_pzuiactionzzz(html_content: str) -> str | None:
    tree = parse_html(html_content)
    if tree is None:
        return None
    xpath_expr = "//script[contains(text(), '$pxActionString') and contains(text(), 'pzuiactionzzz')]"
    script_elements = tree.xpath(xpath_expr)
    for script in script_elements:
        script_text = script.text_content()
        match = re.search(r'pzuiactionzzz\\u003d([^"]+)', script_text)
        if match:
            return urllib.parse.unquote(match.group(1))
    return None


def get_pzTransactionId(html_content: str) -> str | None:
    tree = parse_html(html_content)
    xpath_expr = "//script[contains(text(), 'pega.ui.jittemplate.addMetadataTree')]"
    script_elements = tree.xpath(xpath_expr)
    if not script_elements:
        return None
    script_text = script_elements[0].text
    if not script_text:
        return None
    match = re.search(r"pzTransactionId=([^&\"\s]+)", script_text)
    return match.group(1) if match else None


def get_PD_pzRenderFeedContext(html_content: str) -> str | None:
    tree = parse_html(html_content)
    xpath_expr = "//input[contains(@name, 'PD_pzRenderFeedContext')]"
    input_elements = tree.xpath(xpath_expr)
    if not input_elements:
        return None
    name_attr = input_elements[0].get("name")
    match = re.search(r"(\$PD_pzRenderFeedContext_[^$]+)", name_attr)
    return match.group(1) if match else None


def get_PD_pzFeedParams(html_content: str) -> str | None:
    tree = parse_html(html_content)
    xpath_expr = "//div[@id='AJAXCT']"
    div_elements = tree.xpath(xpath_expr)
    if not div_elements:
        return None
    data_json = div_elements[0].get("data-json")
    if not data_json:
        return None
    try:
        data = json.loads(data_json)
    except Exception:
        return None
    initial = data.get("Initial", {})
    for key in initial:
        if key.startswith("D_pzFeedParams"):
            return key.replace("D_", "PD_", 1)
    return None
