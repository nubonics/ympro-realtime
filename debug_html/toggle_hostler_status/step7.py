import re


def extract_html_pzuiactionzzz(html: str) -> str | None:
    """
    Extracts the first pzuiactionzzz value as it appears in the HTML (no decoding).
    If there are multiple, returns the first.
    """
    matches = re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html)
    if matches:
        return matches[0]  # or use matches[n] for nth, or all for a list
    return None


# Usage
with open('step7.html', 'r', encoding='utf-8') as reader:
    html = reader.read()

pzuiactionzzz = 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTczNmU5ZWY5ZDY2MjU5ZDE4YWRjYWFjMzQyNWZjODg4MTAyOGQyMGU5YjNlN2NjN2IzNTcwOWQyNTFlZmNmMDlkN2NjNTk3ZGJhNWZmNDlhNjdmNjRmN2IyZTRlYTZiNmIzYmIyYTM2MGI4NDZjZGM2ZjI2NzMyYWZjYWZhZTkxY2YxNDczYTgxMDk2ZDNlM2NkMTgxZmZjMTNmZjY3MTNkMzRkZDc0N2Y4MjY4NTdhZmRiY2EzMmQ2NjRkMTg4MGI5YzdiYmMzZjE2YTEwMjQyNjQwMGUyYTY1ZTVlMDQ1ODY1MTE5ZTdiODJiOWFmY2VhMzkxNDk3NTU1YTc4NDFmYzFhYTBmYTBmMTZlOTZjYmEwN2QzNGRiOTNlNzYzOTRhZTg2ZWU1YmVkYWI3YWJlNzIzZWJmMmY1ZTY4MGNhZDBlY2I4YjM3OTFlMzZmZjk3NzBhNmI3ODY2YzA1YTYzYTgxZTYzMDcxOTU1NzRiMjY2ZTIzZjMwYzIyMGYzMw%3D%3D*'
zzz = extract_html_pzuiactionzzz(html)
print(zzz)
assert zzz == pzuiactionzzz, f"Expected {pzuiactionzzz}, got {zzz}"
