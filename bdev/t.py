from lxml import html

case_id = 'T-34484310'

with open('response2.html', 'r', encoding='utf-8') as reader:
    html_text = reader.read()

tree = html.fromstring(html_text)

found_row_id = None

# Try both direct tr and fallback to iter
rows = tree.xpath("//tr")
if not rows:
    print("No <tr> found with xpath. Trying iter...")
    rows = list(tree.iter("tr"))

for tr in rows:
    # lxml may parse attributes with lower-case, so check for both
    attrs = tr.attrib
    oa_args = attrs.get("OAArgs") or attrs.get("oaargs") or ""
    if case_id in oa_args:
        found_row_id = attrs.get("id")
        print(f"Found grid row id for case_id {case_id}: {found_row_id}")
        break

if not found_row_id:
    print("No matching <tr> found. Dumping all <tr> OAArgs and ids for debug:")
    for tr in rows:
        print(tr.attrib.get("OAArgs"), "|", tr.attrib.get("id"))