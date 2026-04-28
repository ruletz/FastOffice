import codecs
import re

app_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/app.js'

with codecs.open(app_path, 'r', 'utf8') as f:
    text = f.read()

# Let's search for "collaboration" to see how the tab is defined.
# Usually it's an array of objects like {id:"collaboration", text:...}
matches = re.finditer(r'.{0,80}id:"collaboration".{0,80}', text)
for i, m in enumerate(matches):
    print(f"Match {i+1}: {m.group(0)}")
    if i > 5: break

print('\n---\n')

matches2 = re.finditer(r'.{0,80}id:"plugins".{0,80}', text)
for i, m in enumerate(matches2):
    print(f"Match {i+1}: {m.group(0)}")
    if i > 5: break

print('\n---\n')

matches3 = re.finditer(r'.{0,80}class="btn-clouds".{0,80}', text)
for i, m in enumerate(matches3):
    print(f"Match {i+1}: {m.group(0)}")
    if i > 5: break

print('\n---\n')

matches4 = re.finditer(r'.{0,80}id:"clouds".{0,80}', text)
for i, m in enumerate(matches4):
    print(f"Match {i+1}: {m.group(0)}")
    if i > 5: break

print('\n---\n')

matches5 = re.finditer(r'.{0,80}Editing".{0,80}', text)
for i, m in enumerate(matches5):
    print(f"Match {i+1}: {m.group(0)}")
    if i > 5: break

