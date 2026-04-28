import codecs

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Add a rule that forces any logo to truncate at icon dimensions 
# since the icon is typically ~30-50px wide and text stretches beyond it.
style_payload = '''
/* Strip logotype text entirely from all logo elements */
.logo { 
    max-width: 45px !important; 
    overflow: hidden !important;
    white-space: nowrap !important;
    text-indent: -9999px !important; /* hide any raw text inside it */
}

/* Also hide raw text siblings if any */
.logo-text, .logo span, .logo text, .title-text, .app-name, #idx-about-appname {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
}

/* If the logo is an SVG the text might be an SVG vector path.
   We can hide paths that go pass x=50, but CSS max-width covers this. */
'''

text = text.replace('</style>\n</head>', style_payload + '\n</style>\n</head>')
text = text.replace('</style></head>', style_payload + '\n</style></head>')

with codecs.open(html_path, 'w', 'utf8') as out:
    out.write(text)
print("Logotype truncation CSS injected successfully.")
