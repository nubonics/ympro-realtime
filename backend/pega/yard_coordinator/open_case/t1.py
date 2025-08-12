from backend.dev.open_task_extractor_test import get_case_info
from backend.pega.yard_coordinator.open_case.task_fields_extractor import extract_selected_fields

task = {}


with open('../../../../debug_html/step_1003.html', 'r') as reader:
    html1 = reader.read()

with open('../../../../debug_html/step_1000.html', 'r') as reader:
    html2 = reader.read()

x = extract_selected_fields(html1)
y = get_case_info(html2)

print(x)
print(y)
