import urllib.parse
import re


def extract_pzuiactionzzz(html: str) -> str | None:
    """
    Extracts the pzuiactionzzz value from a PEGA HTML page.
    Handles url-encoded, unicode-escaped, and JS-embedded forms.
    """
    # 1. Find all possible matches, including urlencoded and \u003d
    candidates = []

    # Match plain and unicode-escaped assignment
    for m in re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html):
        # decode url-encoded just in case
        decoded = urllib.parse.unquote(m)
        candidates.append(decoded)

    # If also inside JSON, e.g. pzuiactionzzz=...%3D%3D*
    for m in re.findall(r'"pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)"', html):
        decoded = urllib.parse.unquote(m)
        candidates.append(decoded)

    # Return the longest candidate (sometimes first is truncated)
    if candidates:
        return max(candidates, key=len)
    return None
