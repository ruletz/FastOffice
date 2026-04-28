import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

out_str = ""
matches = re.finditer(r'<symbol[^>]*id=[\'"][^\'"]*logo[^\'"]*[\'"][^>]*>.*?</symbol>', text, re.IGNORECASE)
for m in matches:
    name = re.search(r'id=[\'"]([^\'"]+)[\'"]', m.group(0)).group(1)
    if 'logo' in name:
        out_str += f'--- {name} ---\n{m.group(0)}\n\n'

with codecs.open("c:/Projects/OnlyOffice/logo_svg.txt", "w", "utf8") as out:
    out.write(out_str)
print("Extracted SVG to logo_svg.txt")
