import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<style id="nuclear-hub-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-hub-js.*?">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="dom_dumper_hub">.*?</script>', '', text, flags=re.DOTALL)

# Extremely safe Hub hiding script targeting REAL DOM from dump
style = """<style id="nuclear-hub-style-v6">
/* Hide the entire 'Clouds' section cleanly! We found its real ID '#idx-sidebar-portals' */
section.connect, #idx-sidebar-portals {
    display: none !important; 
    visibility: hidden !important; 
    opacity: 0 !important; 
    height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}

/* Hide specific Cloud icons/buttons just in case */
.btn-clouds, #idx-btn-clouds, [tooltip*="cloud" i], [tooltip*="Cloud" i], .cloud-icon { 
    display: none !important; 
}

/* Hide all Logos */
.logo-text, .title-text, .app-name, #idx-about-appname, span[class*='logo-text'] { 
    display: none !important; 
    width: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
}
</style>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Reverted to Safe Hub V6 (Targeting #idx-sidebar-portals)")
