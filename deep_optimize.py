import os
import shutil
import codecs

app_dir = 'c:/Projects/OnlyOffice/app'

def safe_remove(path):
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"  Removed: {os.path.basename(path)}")
            return True
        except Exception as e:
            print(f"  FAIL: {os.path.basename(path)}: {e}")
    return False

saved_mb = 0

# ============================================================
# 1. CONVERTER: Remove unused format DLLs
#    x2t loads these dynamically, if the DLL is missing it just
#    skips that format. So we can safely remove formats we never use.
# ============================================================
print("=== Removing unused converter format DLLs ===")
converter_remove = [
    'DjVuFile.dll',       # DjVu reader ~0.6MB
    'EpubFile.dll',       # EPUB ~0.1MB
    'Fb2File.dll',        # Fiction Book ~0.8MB
    'HWPFile.dll',        # Korean Hangul ~1.1MB
    'HtmlFile2.dll',      # HTML import ~1.6MB
    'IWorkFile.dll',      # Apple iWork ~2.8MB
    'OFDFile.dll',        # Open Fixed Document ~0.2MB
    'XpsFile.dll',        # XPS ~0.2MB
    'StarMathConverter.dll', # StarMath ~0.2MB
    'ooxmlsignature.dll', # Digital signatures ~1.7MB
    'icudtl_extra.dat',   # Extra ICU data ~1.7MB
    'kernel_network.dll', # Network kernel ~0.1MB
]
for f in converter_remove:
    p = os.path.join(app_dir, 'converter', f)
    if os.path.exists(p):
        saved_mb += os.path.getsize(p) / 1024 / 1024
        safe_remove(p)

# ============================================================
# 2. CONVERTER TEMPLATES: Keep only en-US, en-GB, pt-PT, pt-BR, default
# ============================================================
print("\n=== Trimming converter templates ===")
templates_dir = os.path.join(app_dir, 'converter', 'empty')
if os.path.exists(templates_dir):
    keep_templates = {'en-US', 'en-GB', 'pt-PT', 'pt-BR', 'default'}
    for d in os.listdir(templates_dir):
        if d not in keep_templates:
            p = os.path.join(templates_dir, d)
            if os.path.isdir(p):
                for f in os.listdir(p):
                    saved_mb += os.path.getsize(os.path.join(p, f)) / 1024 / 1024
                safe_remove(p)

# ============================================================
# 3. Qt IMAGE PLUGINS: Keep only jpeg, svg, ico (needed for UI icons)
# ============================================================
print("\n=== Trimming Qt image plugins ===")
imgformats = os.path.join(app_dir, 'imageformats')
keep_img = {'qjpeg.dll', 'qsvg.dll', 'qico.dll'}
if os.path.exists(imgformats):
    for f in os.listdir(imgformats):
        if f not in keep_img:
            p = os.path.join(imgformats, f)
            saved_mb += os.path.getsize(p) / 1024 / 1024
            safe_remove(p)

# ============================================================
# 4. FONTS: Remove extra OpenSans weights (keep only Regular, Bold)
# ============================================================
print("\n=== Trimming extra font weights ===")
fonts_dir = os.path.join(app_dir, 'fonts')
font_remove = [
    'OpenSans-ExtraBold.ttf',
    'OpenSans-Light.ttf',
    'OpenSans-Semibold.ttf',
]
for f in font_remove:
    p = os.path.join(fonts_dir, f)
    if os.path.exists(p):
        saved_mb += os.path.getsize(p) / 1024 / 1024
        safe_remove(p)

# Remove extra font families (asana = math font, generally not needed for Word)
for d in ['asana', 'crosextra', 'openoffice']:
    p = os.path.join(fonts_dir, d)
    if os.path.exists(p):
        for f in os.listdir(p):
            fp = os.path.join(p, f)
            if os.path.isfile(fp):
                saved_mb += os.path.getsize(fp) / 1024 / 1024
        safe_remove(p)

# ============================================================
# 5. DISABLE SERVICE WORKER in the editor (unnecessary for desktop)
# ============================================================
print("\n=== Disabling service worker ===")
editor_html = os.path.join(app_dir, 'editors', 'web-apps', 'apps', 'documenteditor', 'main', 'index_loader.html')
if os.path.exists(editor_html):
    with codecs.open(editor_html, 'r', 'utf8') as f:
        text = f.read()
    
    # Comment out the service worker registration
    old = '+function registerServiceWorker(){'
    new = '+function registerServiceWorker(){return;'
    if old in text and 'return;' not in text.split('registerServiceWorker')[1][:50]:
        text = text.replace(old, new)
        with codecs.open(editor_html, 'w', 'utf8') as f:
            f.write(text)
        print("  Service worker disabled in editor.")
    else:
        print("  Service worker already disabled or not found.")

# ============================================================
# 6. Reduce require.js timeout from 30s to 10s (faster error feedback)
# ============================================================
    if 'waitSeconds: 30' in text:
        text2 = text.replace('waitSeconds: 30', 'waitSeconds: 10')
        text2 = text2.replace('}, 30000);', '}, 10000);')
        with codecs.open(editor_html, 'w', 'utf8') as f:
            f.write(text2)
        print("  Reduced JS load timeout from 30s to 10s.")

# ============================================================
# 7. REMOVE d3dcompiler_47.dll if GPU compositing is disabled
#    (our shortcut has --disable-gpu-compositing, so this is unused)
# ============================================================
print("\n=== Removing d3dcompiler (GPU compositing disabled) ===")
d3d = os.path.join(app_dir, 'd3dcompiler_47.dll')
if os.path.exists(d3d):
    saved_mb += os.path.getsize(d3d) / 1024 / 1024
    safe_remove(d3d)

# ============================================================
# 8. REMOVE libEGL.dll and libGLESv2.dll (GPU compositing disabled)
# ============================================================
print("\n=== Removing OpenGL ES DLLs (GPU compositing disabled) ===")
for f in ['libEGL.dll', 'libGLESv2.dll']:
    p = os.path.join(app_dir, f)
    if os.path.exists(p):
        saved_mb += os.path.getsize(p) / 1024 / 1024
        safe_remove(p)

# ============================================================
# 9. Trim videoplayer.dll (VLC already removed)
# ============================================================
vp = os.path.join(app_dir, 'videoplayer.dll')
if os.path.exists(vp):
    saved_mb += os.path.getsize(vp) / 1024 / 1024
    safe_remove(vp)

# ============================================================
# 10. Remove printsupport, platformthemes, styles (rarely used Qt plugins)
# ============================================================
print("\n=== Removing rarely-used Qt support dirs ===")
for d in ['printsupport', 'platformthemes', 'styles']:
    p = os.path.join(app_dir, d)
    if os.path.exists(p):
        for f in os.listdir(p):
            fp = os.path.join(p, f)
            if os.path.isfile(fp):
                saved_mb += os.path.getsize(fp) / 1024 / 1024
        safe_remove(p)

print(f"\n{'='*50}")
print(f"Total space freed: ~{saved_mb:.1f} MB")
print(f"These components also won't be loaded into RAM at startup.")
print(f"{'='*50}")
