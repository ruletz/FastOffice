import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Try to find the container around the logo, especially any SVG that contains "logo"
# and the HTML text nodes next to it.
matches = re.finditer(r'<[a-z]+[^>]*class=[\'"][^\'"]*logo[^\'"]*[\'"][^>]*>.*?</[a-z]+>', text, re.IGNORECASE)
for m in matches:
    print("MATCH CONTAINER:")
    print(m.group(0)[:300])
    
print("-" * 50)
m2 = re.search(r'idx-ver-logo', text)
if m2:
    start = max(0, m2.start() - 200)
    end = min(len(text), m2.start() + 500)
    print("CONTEXT AROUND idx-ver-logo:")
    print(text[start:end])
