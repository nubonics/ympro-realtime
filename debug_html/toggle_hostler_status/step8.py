def extract_pzuiactionzzz(html: str) -> str | None:
    import re
    import urllib.parse
    candidates = []
    for m in re.findall(r'pzuiactionzzz[=\\u003d]+([A-Za-z0-9%*]+)', html):
        decoded = urllib.parse.unquote(m)
        candidates.append(decoded)
    if candidates:
        return max(candidates, key=len)
    return None


with open('step8.html', 'r', encoding='utf-8') as reader:
    html = reader.read()

pzuiactionzzz = 'CXt0cn17RENTUEFfWWFyZENvb3JkaW5hdG9yfTczNmU5ZWY5ZDY2MjU5ZDE4YWRjYWFjMzQyNWZjODg4MTAyOGQyMGU5YjNlN2NjN2IzNTcwOWQyNTFlZmNmMDlkN2NjNTk3ZGJhNWZmNDlhNjdmNjRmN2IyZTRlYTZiNmIzYmIyYTM2MGI4NDZjZGM2ZjI2NzMyYWZjYWZhZTkxY2YxNDczYTgxMDk2ZDNlM2NkMTgxZmZjMTNmZjY3MTM1M2YxMGI5OWFiZTg4OTRmYThjNTNmZWVlNWMwYmQ5YzZkN2MyNTFjZjhhMzUxNmRmNmNmYmZiM2E5YzQ2ZTZjNTQzOGNlN2E5MWU5MGExODI0YWM0NzEzZDQyYTE0ZjM4OGE2ZTk1NDIwODM0Nzc4YzA4ODZjZGU3ODYxZDJiZjM4MTlmODFlYmIxMTUxODIwNjI1ZTVjMjFkNWY0OTcyYzhkNmU0NDllMDg5NTBiY2EzZjlmM2Q2MDAxMzkxMTllOTRkYTM2NjBlMzBjMWZkN2I1NWRhZmI2MzY5YzdlNWE1MDg3ZjBiNTM1ZWJiYjY5ZjU0OWE2ODNmMWNlNmZh*'
zzz = extract_pzuiactionzzz(html)
print(zzz)
assert zzz == pzuiactionzzz, f"Expected {pzuiactionzzz}, got {zzz}"