import os, shutil, codecs

app = 'c:/Projects/OnlyOffice/app'

# 1. Extreme CSS for Left Panel
index_path = os.path.join(app, 'index.html')
with codecs.open(index_path, 'r', 'utf8') as f:
    text = f.read()

style_payload = '''
<style>
/* Make the left tool menu short (narrow) and icon-only */
.tool-menu { 
    width: 60px !important; 
    min-width: 60px !important; 
    padding: 8px !important; 
    overflow-x: hidden !important; 
}
.tool-menu .menu-item a { 
    padding: 10px !important; 
    justify-content: center !important; 
}
.tool-menu .menu-item span.text { 
    display: none !important; 
}
.tool-menu .icon-box {
    margin-right: 0px !important;
}
.main-column.col-left { 
    max-width: 60px !important; 
    flex: 0 0 60px !important;
    width: 60px !important;
}
</style>
</head>'''
if '<style>\n/* Make the left tool menu' not in text:
    text = text.replace('</head>', style_payload)
with codecs.open(index_path, 'w', 'utf8') as f:
    f.write(text)
print("CSS injected into index.html")

# 2. Authenticodes configs for faster load time
config_content = '''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <runtime>
    <generatePublisherEvidence enabled="false"/>
  </runtime>
</configuration>'''
with open(os.path.join(app, 'desktopeditors.exe.config'), 'w', encoding='utf-8') as f:
    f.write(config_content)
with open(os.path.join(app, 'editors.exe.config'), 'w', encoding='utf-8') as f:
    f.write(config_content)
with open(os.path.join(app, 'converter', 'x2t.exe.config'), 'w', encoding='utf-8') as f:
    f.write(config_content)
print("Authenticode blocks added.")

# 3. Trim Dictionaries and Locales
dicts_path = os.path.join(app, 'dictionaries')
loc_path = os.path.join(app, 'locales')
for folder in [dicts_path, loc_path]:
    if not os.path.exists(folder): continue
    for item in os.listdir(folder):
        # We keep pt_PT/pt-PT, en_US/en-US, en_GB/en-GB
        if item.startswith('en') or item.startswith('pt') or item.lower().endswith('.md'):
            continue
        p = os.path.join(folder, item)
        if os.path.isdir(p): shutil.rmtree(p)
        else: os.remove(p)
print("Dictionaries and Locales trimmed.")

# 4. Remove ALL SDK Plugins to save RAM overhead entirely
plugins_dir = os.path.join(app, 'editors', 'sdkjs-plugins')
if os.path.exists(plugins_dir):
    for f in os.listdir(plugins_dir):
        p = os.path.join(plugins_dir, f)
        if os.path.isdir(p): shutil.rmtree(p)
        else: os.remove(p)
    # create empty dir to prevent crash
    os.makedirs(plugins_dir, exist_ok=True)
print("SDK JS Plugins wiped entirely.")

print("Extreme memory optimization applied successfully!")
