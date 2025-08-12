from debug_html.toggle_hostler_status.extract_pzuiactionzzz import extract_pzuiactionzzz

# Usage
with open('step3.html', 'r', encoding='utf-8') as reader:
    html = reader.read()

zzz = extract_pzuiactionzzz(html)
print(zzz)
