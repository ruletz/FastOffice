import os, shutil, codecs

app = 'c:/Projects/OnlyOffice/app'
removed_mb = 0

def rm(path):
    global removed_mb
    full = os.path.join(app, path) if not os.path.isabs(path) else path
    if os.path.isdir(full):
        size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(full) for f in fn)
        shutil.rmtree(full)
        mb = size / (1024*1024)
        removed_mb += mb
        print(f"  Removed DIR  {path}  ({mb:.1f} MB)")
    elif os.path.isfile(full):
        size = os.path.getsize(full)
        os.remove(full)
        mb = size / (1024*1024)
        removed_mb += mb
        print(f"  Removed FILE {path}  ({mb:.1f} MB)")
    else:
        print(f"  SKIP (not found): {path}")

print("=" * 60)
print("OnlyOffice Word-Only Size Optimization")
print("=" * 60)

# ============================================================
# 1. PLUGINS: Remove unnecessary editor plugins (~33 MB)
# Keep only: Thesaurus (useful for Word), Plugin Manager, Encryption
# ============================================================
print("\n[1] Removing unnecessary editor plugins...")
plugin_dir = os.path.join(app, 'editors/sdkjs-plugins')
keep_plugins = {
    '{B509123E-6335-40BD-B965-91EB799346E3}',  # Thesaurus (0.2 MB)
    '{BE5CBF95-C0AD-4842-B157-AC40FEDD9840}',  # Plugin Manager (0.6 MB)
    '{FFF0E1EB-13DB-4678-B67D-FF0A41DBBCEF}',  # Encryption (0 MB)
    'v1',
}
if os.path.isdir(plugin_dir):
    for name in os.listdir(plugin_dir):
        if name not in keep_plugins and name != 'pluginBase.js':
            rm(os.path.join(plugin_dir, name))

# ============================================================
# 2. CONVERTER: Remove unused format DLLs (~8 MB)
# IWorkFile.dll = Apple iWork (Pages/Numbers/Keynote)
# EpubFile.dll = EPUB format
# ooxmlsignature.dll = XML digital signatures
# PdfFile.dll = standalone PDF (user said no standalone PDF editor)
# icudtl_extra.dat = extra ICU data
# ============================================================
print("\n[2] Removing unused converter components...")
rm('converter/IWorkFile.dll')        # 2.75 MB - Apple formats
rm('converter/EpubFile.dll')         # 0.1 MB - EPUB
rm('converter/ooxmlsignature.dll')   # 1.71 MB - XML signatures
rm('converter/icudtl_extra.dat')     # 1.72 MB - Extra ICU data

# ============================================================
# 3. VLC PLUGINS: Remove video/multimedia plugins (~55 MB)
# A word processor does not need video playback
# ============================================================
print("\n[3] Removing VLC multimedia plugins...")
rm('plugins')

# ============================================================
# 4. VLC DLLs in app root
# ============================================================
print("\n[4] Removing VLC root DLLs...")
rm('libvlc.dll')
rm('libvlccore.dll')
rm('videoplayer.dll')

# ============================================================
# 5. Vulkan/SwiftShader - software GPU rendering fallback
# These are rarely needed on modern systems
# ============================================================
print("\n[5] Removing Vulkan/SwiftShader fallback...")
rm('vk_swiftshader.dll')
rm('vk_swiftshader_icd.json')
rm('vulkan-1.dll')

# ============================================================
# 6. Monaco Editor (23 MB) - code editor for macros
# Not needed for basic Word usage
# ============================================================
print("\n[6] Removing Monaco Editor (macro code editor)...")
rm('editors/web-apps/vendor/monaco')

# ============================================================
# 7. Duplicate icudtl.dat in app root
# The converter has its own ICU data (icudt74.dll + icudtl.dat)
# The app root icudtl.dat is for Chromium/CEF
# We should NOT remove the root one - it's needed by libcef.dll
# But the converter duplicate can stay as it's needed by x2t
# ============================================================

# ============================================================
# 8. SmartArts data (8.6 MB) - mainly for presentations
# Keep it since SmartArts can appear in Word docs
# ============================================================

# ============================================================
# 9. updatesvc.exe - update service not needed
# ============================================================
print("\n[9] Removing update service...")
rm('updatesvc.exe')

# ============================================================
# 10. bearer folder - Qt network bearers (unused in local mode)
# ============================================================
print("\n[10] Removing Qt network bearer plugins...")
rm('bearer')

# ============================================================
# 11. printsupport - often empty or Qt fallback
# ============================================================
# Keep this - needed for printing documents

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print(f"Total removed: {removed_mb:.1f} MB")

# Recalculate total
total = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(app) for f in fn)
print(f"New total size: {total/(1024*1024):.1f} MB")
print("=" * 60)
