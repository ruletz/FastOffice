import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app'
editors = ['documenteditor', 'spreadsheeteditor', 'presentationeditor']

def clean_file(path):
    if not os.path.exists(path):
        return
    with codecs.open(path, 'r', 'utf8') as f:
        text = f.read()

    # REMOVE ALL NUCLEAR STYLES AND SCRIPTS
    text = re.sub(r'<style id="nuclear-style-v\d+">.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script id="nuclear_ui_v\d+">.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style id="nuclear-hub-style-v\d+">.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script id="nuclear-hub-js-v\d+">.*?</script>', '', text, flags=re.DOTALL)
    
    # Remove older styles without IDs
    text = re.sub(r'<style>/\* Make the left tool menu.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style>/\* Hide the text next to the main logo.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style>/\* Also remove the actual panels.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style>/\* Float Save/Undo leftwards.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style>/\* More aggressive cleanup for the Hub.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style>/\* Left branding top logo.*?</style>', '', text, flags=re.DOTALL)

    with codecs.open(path, 'w', 'utf8') as f:
        f.write(text)

# Clean Hub
clean_file(os.path.join(app_dir, 'index.html'))

# Clean Editors
for editor in editors:
    clean_file(os.path.join(app_dir, 'editors', 'web-apps', 'apps', editor, 'main', 'index.html'))
    clean_file(os.path.join(app_dir, 'editors', 'web-apps', 'apps', editor, 'main', 'index_loader.html'))

print("TOTAL CLEANUP COMPLETE: All custom injections removed from Hub and Editors.")
