import codecs, re
html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()
text = re.sub(r'<script id="canvas_hijack">.*?</script>\s*', '', text, flags=re.DOTALL)
with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)
print('Canvas hack removed')
