import os, shutil, re

app_dir = r'c:\Projects\OnlyOffice\app'

print("=== 1. NUKING PLUGINS & AI ===")
plugins_dir = os.path.join(app_dir, 'editors', 'sdkjs-plugins')
if os.path.exists(plugins_dir):
    shutil.rmtree(plugins_dir)
    print("Deleted sdkjs-plugins")

print("=== 2. NUKING CLOUD PROVIDERS ===")
providers_dir = os.path.join(app_dir, 'editors', 'web-apps', 'apps', 'common', 'main', 'resources', 'img', 'providers')
if os.path.exists(providers_dir):
    shutil.rmtree(providers_dir)
    print("Deleted cloud providers assets")

print("=== 3. NUKING EXTRA LOCALES ===")
# Dictionaries
dict_dir = os.path.join(app_dir, 'dictionaries')
if os.path.exists(dict_dir):
    count = 0
    for item in os.listdir(dict_dir):
        if not (item.startswith('en') or item.startswith('pt')):
            path = os.path.join(dict_dir, item)
            if os.path.isdir(path): shutil.rmtree(path)
            else: os.remove(path)
            count += 1
    print(f"Deleted {count} dictionary folders")

# Web-Apps JSON locales
locales_dir = os.path.join(app_dir, 'editors', 'web-apps')
count = 0
for root, dirs, files in os.walk(locales_dir):
    if root.endswith('locale') or root.endswith('locales'):
        for f in files:
            if f.endswith('.json'):
                name = f.lower()
                if not (name.startswith('en') or name.startswith('pt')):
                    os.remove(os.path.join(root, f))
                    count += 1
print(f"Deleted {count} useless json locales")

print("=== 4. CROPPING ONLYOFFICE TEXT FROM LOGOS ===")
def crop_svg(path):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf8') as f:
        content = f.read()
    
    # We remove the path that draws the letters (which is the very long path without opacity)
    # The letters path typically doesn't have opacity attribute right after it, whereas the icon paths do.
    # Actually, simpler: just change the SVG viewport to width="18" and add viewBox="0 0 18 20"
    content = re.sub(r'width="\d+"', 'width="18"', content)
    if 'viewBox' not in content:
        content = content.replace('<svg ', '<svg viewBox="0 0 18 20" ')
    
    with open(path, 'w', encoding='utf8') as f:
        f.write(content)

logos = [
    os.path.join(app_dir, 'editors', 'web-apps', 'apps', 'common', 'main', 'resources', 'img', 'header', 'header-logo_s.svg'),
    os.path.join(app_dir, 'editors', 'web-apps', 'apps', 'common', 'main', 'resources', 'img', 'header', 'dark-logo_s.svg'),
    os.path.join(app_dir, 'editors', 'web-apps', 'apps', 'common', 'main', 'resources', 'img', 'about', 'logo_s.svg'),
    os.path.join(app_dir, 'editors', 'web-apps', 'apps', 'common', 'main', 'resources', 'img', 'about', 'logo-white_s.svg')
]

for l in logos:
    crop_svg(l)
print("Cropped text from SVG logos")
