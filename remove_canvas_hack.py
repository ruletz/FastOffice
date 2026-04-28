import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# remove old hijack completely to restore native straight lines
text = re.sub(r'<script id="canvas_hijack">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="canvas_logger">.*?</script>', '', text, flags=re.DOTALL)

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Canvas hijack removed. Native straight red lines restored.")
