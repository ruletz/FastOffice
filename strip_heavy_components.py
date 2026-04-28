import os
import shutil

app_dir = 'c:/Projects/OnlyOffice/app'

def safe_remove(path):
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"Removed: {path}")
        except Exception as e:
            print(f"Failed to remove {path}: {e}")

# 1. Remove VLC (massive memory/startup bloat)
safe_remove(os.path.join(app_dir, 'libvlc.dll'))
safe_remove(os.path.join(app_dir, 'libvlccore.dll'))
safe_remove(os.path.join(app_dir, 'plugins')) # VLC plugins!

# 2. Remove Vulkan/SwiftShader which add GPU startup overhead
safe_remove(os.path.join(app_dir, 'vulkan-1.dll'))
safe_remove(os.path.join(app_dir, 'vk_swiftshader.dll'))
safe_remove(os.path.join(app_dir, 'vk_swiftshader_icd.json'))

# 3. Remove Bearer, Update Service
safe_remove(os.path.join(app_dir, 'bearer'))
safe_remove(os.path.join(app_dir, 'updatesvc.exe'))

# 4. Remove heavy PAKs
safe_remove(os.path.join(app_dir, 'chrome_200_percent.pak'))

# 5. Remove spellchecker dictionaries we don't need (extreme optimization)
dicts = os.path.join(app_dir, 'dictionaries')
if os.path.exists(dicts):
    for d in os.listdir(dicts):
        if not (d.startswith('en') or d.startswith('pt')):
            safe_remove(os.path.join(dicts, d))

locs = os.path.join(app_dir, 'locales')
if os.path.exists(locs):
    for d in os.listdir(locs):
        if not (d.startswith('en') or d.startswith('pt')):
            safe_remove(os.path.join(locs, d))

print("Heavy runtime components stripped successfully.")
