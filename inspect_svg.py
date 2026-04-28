import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Grab all SVG <symbol> definitions that have "logo" in their ID
matches = re.finditer(r'<symbol[^>]*id=[\'"][^\'"]*logo[^\'"]*[\'"][^>]*>.*?</symbol>', text, re.IGNORECASE)
cnt = 0
for m in matches:
    print('--- SVG SYMBOL:', re.search(r'id=[\'"]([^\'"]+)[\'"]', m.group(0)).group(1))
    # print the first 500 characters of the paths to see if it's huge = contains logotype
    print(m.group(0)[:500])
    cnt += 1

if cnt == 0:
    print("No SVG logo symbols found.")
