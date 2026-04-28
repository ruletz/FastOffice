import os

html_path = 'c:/Projects/OnlyOffice/app/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

style = '''<style>
/* More aggressive cleanup for the Hub */
.nav-item[data-id="templates"],
.nav-item[data-id="connect"],
.nav-item[data-id="plugins"],
.nav-item[data-id="about"],
.nav-item[data-id="help"] {
    display: none !important;
}

/* Hide the logo from the hub too for a super clean look */
.logo { display: none !important; }

/* The left panel container for those tabs */
.col-left { 
    background-color: var(--background-normal);
    border-right: none !important;
}
/* Reduce padding around the login area if it's there */
#area-login {
    padding-top: 10px;
}
</style>'''

if '/* More aggressive cleanup' not in html:
    html = html.replace('</head>', style + '\n</head>')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Aggressive Hub style injected!')
else:
    print('Already injected')
