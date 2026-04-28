import os

html_path = 'c:/Projects/OnlyOffice/app/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

style = '''<style>
/* Remove bloat tabs from desktop hub */
li[data-id="templates"],
li[data-id="connect"],
li[data-id="plugins"],
li[data-id="help"],
.new-feat-badge {
    display: none !important;
}
/* Also remove the actual panels just in case */
#templates-panel,
#connect-panel,
#plugins-panel {
    display: none !important;
}
</style>'''

if style not in html:
    html = html.replace('</head>', style + '\n</head>')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Hub style injected!')
else:
    print('Already injected')
