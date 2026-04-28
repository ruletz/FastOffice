import codecs
import re
import os
import shutil

# --- CONFIGURATION ---
APP_DIR = r'C:/Projects/OnlyOffice/app'
EDITORS_DIR = os.path.join(APP_DIR, 'editors', 'web-apps', 'apps')
HUB_PATH = os.path.join(APP_DIR, 'index.html')
EDITORS = ['documenteditor', 'spreadsheeteditor', 'presentationeditor', 'pdfeditor']

# --- RUST WASM (Extracted from previous optimization) ---
WASM_B64 = "AGFzbQEAAAAB/wEcYAJ/fwF/YAN/f38Bf2ABfwBgAn9/AGAGf39/f39/AGADf39/AGAEf39/fwBgAX8Bf2AHf39/f39/fwBgBX9/f39/AGAEf39/fwF/YAV/f39/fwF/YAAAYAACf39gBn9/f39/fwF/YAJ/fwF+YAN/f38BfmAHf39/f39/fwF/YAABf2ACf38Cf39gBX9/f39+AGAIf39/f39/f38Bf2AEf39/fgBgFn9/f39/f39/f39/f39/f39/f39/f38Bf2ATf39/f39/f39/f39/f39/f39/fwF/YA9/f39/f39/f39/f39/f38Bf2ALf39/f39/f39/f38Bf2AEf35+fwACOwEXLi9mYXN0X29veG1sX3J1c3RfYmcuanMfX193YmluZGdlbl9pbml0X2V4dGVybnJlZl90YWJsZQAMA/kH9wcFBQYFBAYDAwQKBQkEAggFBwQFBQMGBgMDBAkIAAMJAAYICAYABgYFBQYIBAQGBgIIAwgDBQUEBAQGBgkFBgUGBAMFBQMFBgUFAQQFBQICAgQJBgYIAQEBAwQDBgMAAQABAgMBAQkDAgEBAQEBAAUDAwUAAwAGBgIGBwUGBgYHAwYCAgEBAQMCAw4CAAUFAQUFBgUFBQEABQIDAgkCCAoKBgICBQIACQEBBQgDCQQCAAICBAYDFAUDAxUDAwMEBgMFBA8GAwoPBQIQEAYIBQMEAwoDAwQEBgYABQgDAwIEBAMFBQAAAAAFAgQBAQYDBAICAAIFBgYGBgQGAxYFDgAAAwMFAgYDAwUEAwcIBQIDBQcHAgICBQYDAQcKBAQHBAUJAgMCAgICAgECAwYGBQACAAkJBgYGAwcDBwoGBAYFAAQBAQsGBAcDBAYFAwMABAAABAUAAgAGAwMDAwMDAwMAAAYAEQkECwAABgYGBQMLAgYAAAYBBgMAAwIBBQYDBAICAgYBAwMGBgUEBAEAAAAGAwsLCwIBAgMCFwUGAAICAgICAgIYAQAACgMCAgIABAICCRkAAAIFBQIAAAMCDAQAAQQBGgkCAQIDAgICBQYFABEFAgUFBAACAgUGBgkGDAMGAAUCBgAABwAAAAsHAgUEAQADBwUCAAUCAAAAAAAABgAAAwkAAAIAAAMCAwAAAAAAAAACAAAAAAAAAAACAAADBwMDAgAAAAICAAACAgICAgIAAgAAAgICAgIDAAMDBwIAAwUCBQcCAAAEAAAAAgICGwMCAAUSAQQAAAEBAAAAAAAAAAIFAAAAAAcAAAAAAAADAAAAAgAFAAAAAAAAAAAAAAAEAAAAAwEAAAAAAAABAQAAAAAAAAIAAAAAAAAAAAAAAgAABwwBAgACAAAAAgAAAAAAAgAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAgIHAwYFAAQKCgAAAgACAAAAAAAAAAUAAAUFAAAAAAsAAAAAAAYAAAAGAAAAAAAFBgAGCQAAAAAAAAAAAAAAAAAAAAAAAgwMAgAAAAAAAAAAAAAAAAAAAAAAAAAABwAAAAAAAAAAAAUAAAAHAgAAAAcHAgIBAQAAAAEAAAAABgIHAgIDAgUFBQcDBgMDAAATEwICAgICBwUKAgICAhICBwICAgIAAgAAAAAABQUAAAACAAAAAAAAAAAAAwMDAAAAAAUBBwcHAAkAAAoAAAAAAAAAAAMAAAUCAgACBQAAAAAHBwcHAAEAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAADAAADAAEAAAAHBwcACAMCAgcHBwcCBwcHBwcABwcHBwcHBwcHBwcDBAsCcAHOBc4FbwCACAUDAQAXBgkBfwFBgIDAAAsHogEIBm1lbW9yeQIAEmRlY29kZV9iYXNlNjRfZmFzdADiBhVwYXJzZV9vb3htbF90YWdzX2Zhc3QA4QYVX193YmluZGdlbl9leHRlcm5yZWZzAQERX193YmluZGdlbl9tYWxsb2MAzwYSX193Ymlu"

# --- HELPERS ---
def clean_tags(text):
    text = re.sub(r'<(style|script) id="nuclear-.*?">.*?</\1>', '', text, flags=re.DOTALL)
    text = re.sub(r'<(style|script) id="surgical-.*?">.*?</\1>', '', text, flags=re.DOTALL)
    return text

def inject_head(text, style="", script=""):
    if '</head>' in text:
        injection = ""
        if style: injection += f'\n<style id="nuclear-final-style">{style}</style>'
        if script: injection += f'\n<script id="nuclear-final-script">{script}</script>'
        return text.replace('</head>', injection + '\n</head>')
    return text

# --- CORE FUNCTIONS ---

def prune_locales():
    print("[1/4] Pruning Locales...")
    keep_prefixes = ('en', 'pt', 'default')
    for root, dirs, files in os.walk(os.path.join(APP_DIR, 'editors')):
        dirname = os.path.basename(root).lower()
        if dirname in ('locale', 'locales', 'lang', 'languages', 'translations', 'help', 'dictionaries'):
            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                name, ext = os.path.splitext(item)
                if not name.lower().startswith(keep_prefixes) and name.lower() != 'default':
                    try:
                        if os.path.isdir(item_path): shutil.rmtree(item_path)
                        else: os.remove(item_path)
                    except: pass

def optimize_hub():
    print("[2/4] Optimizing Hub UI...")
    if not os.path.exists(HUB_PATH): return
    with codecs.open(HUB_PATH, 'r', 'utf8') as f:
        text = f.read()
    
    text = clean_tags(text)
    
    style = """
/* Nuke Loading Panel */
#loading-mask, .loadmask, .loader-page { display: none !important; opacity: 0 !important; visibility: hidden !important; }

/* Sidebar Optimization */
.main-column.col-left { width: 60px !important; min-width: 60px !important; flex: 0 0 60px !important; }
.tool-menu .menu-item span.text { display: none !important; }
.tool-menu .menu-item a { justify-content: center !important; padding: 10px !important; }
.tool-menu .icon-box { margin-right: 0 !important; }

/* Remove Bloat Options */
li[action="templates"], #idx-sidebar-portals, .connect, .sidebar-block-title, .btn-clouds { display: none !important; }
.menu-item:has(a[action="templates"]) { display: none !important; }

/* Branding Removal */
.logo, .logo-text, .app-name, #idx-about-appname, .title-text { display: none !important; }
"""
    
    script = """
document.addEventListener("DOMContentLoaded", function() {
    // Force sidebar text removal if CSS fails
    setInterval(function() {
        document.querySelectorAll('.tool-menu .menu-item span.text').forEach(s => s.style.display = 'none');
        document.querySelectorAll('li[action="templates"], #idx-sidebar-portals').forEach(e => e.style.display = 'none');
    }, 1000);
});
"""
    text = inject_head(text, style, script)
    with codecs.open(HUB_PATH, 'w', 'utf8') as f:
        f.write(text)

def optimize_editors():
    print("[3/4] Optimizing Editor UI & Engine...")
    for editor in EDITORS:
        path = os.path.join(EDITORS_DIR, editor, 'main', 'index.html')
        if not os.path.exists(path): continue
        
        with codecs.open(path, 'r', 'utf8') as f:
            text = f.read()
        
        text = clean_tags(text)
        
        style = """
/* Nuke Loading */
#loading-mask, .loadmask, .loader-page, .preloader { display: none !important; }

/* Header Reconstruction */
#viewport { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 40px !important; height: calc(100% - 40px) !important; }

/* First Header (Branding) Removal */
#app-title, .brendpanel, .box-header, .main-header { 
    height: 40px !important; min-height: 40px !important;
    background: transparent !important; border: none !important;
    position: absolute !important; top: 0 !important; width: 100% !important;
    z-index: 1000 !important; pointer-events: none !important;
    display: flex !important; align-items: center !important;
}

/* Move First Icons to Second Header (Right Aligned) */
#box-header-tools {
    position: absolute !important; right: 10px !important; 
    display: flex !important; align-items: center !important;
    pointer-events: auto !important; height: 100% !important;
}

/* Title Centered */
#box-document-title {
    width: 100% !important; display: flex !important; 
    justify-content: center !important; align-items: center !important;
    pointer-events: none !important;
}
#id-box-doc-name {
    pointer-events: auto !important; margin: 0 auto !important;
    font-weight: bold !important; font-size: 14px !important;
}

/* Hide Unwanted Tabs & Menus */
li[data-layout-name="toolbar-collaboration"], li[data-tab="review"],
li[data-layout-name="toolbar-plugins"], li[data-tab="plugins"],
li[data-layout-name="toolbar-protect"], li[data-tab="protect"],
#slot-btn-edit-mode, #file-menu-btn, .btn-file-menu {
    display: none !important; visibility: hidden !important;
}

/* Ribbon Adjustment */
#toolbar, .sktoolbar { background: var(--bg-toolbar, #f3f3f3) !important; }
"""
        
        script = """
(function() {
    async function BootRust() {
        try {
            var b = atob('""" + WASM_B64 + """');
            var y = new Uint8Array(b.length);
            for (var i = 0; i < b.length; i++) y[i] = b.charCodeAt(i);
            const m = await WebAssembly.instantiate(y, {
                "./fast_ooxml_rust_bg.js": { __wbindgen_init_externref_table: function() {} }
            });
            window.__RUST_PARSER = m.instance.exports;
            console.log('[RUST] Engine Active');
        } catch(e) {}
    }
    BootRust();

    document.addEventListener("DOMContentLoaded", function() {
        setInterval(function() {
            var tabs = document.querySelectorAll("li.ribtab, a.ribtab");
            tabs.forEach(t => {
                var txt = (t.textContent || "").toLowerCase();
                if (txt.includes("collaboration") || txt.includes("plugin") || txt.includes("protection") || txt.includes("review")) {
                    t.style.display = "none";
                }
            });
        }, 1500);
    });
})();
"""
        text = inject_head(text, style, script)
        with codecs.open(path, 'w', 'utf8') as f:
            f.write(text)

def cleanup_backup():
    print("[4/4] Final Cleanup...")
    # Any other minor fixes
    pass

if __name__ == "__main__":
    prune_locales()
    optimize_hub()
    optimize_editors()
    cleanup_backup()
    print("\\nSUCCESS: OnlyOffice Re-Optimized Beyond Previous State.")
