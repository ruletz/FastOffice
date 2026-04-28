import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index_loader.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Add a CSS block to permanently hide the loading mask from rendering
# So the user doesn't arbitrarily stare at a "Loading... 45%" screen when the app is already parsing the DOM.
style = '''<style id="anti-loader">
/* Nuke the loading mask from the face of the earth */
#loading-mask, .loadmask, .preloader, #box-loadmask { 
    display: none !important; 
    opacity: 0 !important; 
    visibility: hidden !important; 
    z-index: -9999 !important; 
    pointer-events: none !important;
}
/* Ensure the body actually scrolls and isn't locked */
body { overflow: auto !important; }
</style>'''

text = re.sub(r'<style id="anti-loader">.*?</style>', '', text, flags=re.DOTALL)
text = text.replace('</head>', style + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Loading mask completely neutralized.")
