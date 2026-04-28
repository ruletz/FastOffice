import os
import re

app_dir = "c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main"
files_to_check = ['index_loader.html', 'app.js']

for file in files_to_check:
    path = os.path.join(app_dir, file)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"--- Analyzing {file} ---")
    
    # Look for IDs containing 'cloud'
    clouds = re.findall(r'id=["\']([^"\']*cloud[^"\']*)["\']', content, re.IGNORECASE)
    if clouds:
        print(f"Clouds IDs: {set(clouds)}")
        
    # Look for IDs containing 'plugin'
    plugins = re.findall(r'id=["\']([^"\']*plugin[^"\']*)["\']', content, re.IGNORECASE)
    if plugins:
        print(f"Plugin IDs: {set(plugins)}")
        
    # Look for IDs containing 'collab'
    collab = re.findall(r'id=["\']([^"\']*collab[^"\']*)["\']', content, re.IGNORECASE)
    if collab:
        print(f"Collab IDs: {set(collab)}")

    # Look for IDs containing 'protection'
    prot = re.findall(r'id=["\']([^"\']*protect[^"\']*)["\']', content, re.IGNORECASE)
    if prot:
        print(f"Protection IDs: {set(prot)}")

    # Look for IDs containing 'undo'
    undo = re.findall(r'id=["\']([^"\']*undo[^"\']*)["\']', content, re.IGNORECASE)
    if undo:
        print(f"Undo IDs: {set(undo)}")
        
    # Look for IDs containing 'save'
    save = re.findall(r'id=["\']([^"\']*save[^"\']*)["\']', content, re.IGNORECASE)
    if save:
        print(f"Save IDs: {set(save)}")
        
    # Look for IDs containing 'title'
    title = re.findall(r'id=["\']([^"\']*title[^"\']*)["\']', content, re.IGNORECASE)
    if title:
        print(f"Title IDs: {set(title)}")
        
    # Look for IDs containing 'mode' or 'edit'
    mode = re.findall(r'class=["\'][^"\']*(?:mode|edit)[^"\']*["\']', content, re.IGNORECASE)
    if mode:
        print(f"Mode/Edit classes (sample): {list(set(mode))[:5]}")
