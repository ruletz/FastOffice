import codecs

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Hide text associated with the logo or app name
style_payload = '''
<style>
/* Hide the text next to the main logo/logotype */
#idx-about-appname,
.idx-about-appname,
.logo-text,
.app-name,
#idx-about-version,
.ver-copyright,
.box-copyright,
.title-text,
.logo text,
.logo span,
.logo .text,
.logo-container .text,
#box-ver span:not(.ver-logo) {
    display: none !important;
}

/* Ensure the wrapper collapses if it was reserving space for text */
#idx-about-cut-logo {
    margin-right: 0 !important;
}

/* In the custom title bar, the title might be hidden directly */
.titlebar-title {
    display: none !important;
}
</style>
</head>'''

if '/* Hide the text next to the main logo' not in text:
    text = text.replace('</head>', style_payload)
with codecs.open(html_path, 'w', 'utf8') as out:
    out.write(text)
print("Injected CSS styles successfully.")
