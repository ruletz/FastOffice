import codecs
import re
import os
import shutil

# --- CONFIGURATION ---
APP_DIR = r'C:/Projects/OnlyOffice/app'
EDITORS_DIR = os.path.join(APP_DIR, 'editors', 'web-apps', 'apps')
HUB_PATH = os.path.join(APP_DIR, 'index.html')
EDITORS = ['documenteditor', 'spreadsheeteditor', 'presentationeditor', 'pdfeditor']

# --- RUST WASM (Performance Engine) ---
WASM_B64 = "AGFzbQEAAAAB/wEcYAJ/fwF/YAN/f38Bf2ABfwBgAn9/AGAGf39/f39/AGADf39/AGAEf39/fwBgAX8Bf2AHf39/f39/fwBgBX9/f39/AGAEf39/fwF/YAV/f39/fwF/YAAAYAACf39gBn9/f39/fwF/YAJ/fwF+YAN/f38BfmAHf39/f39/fwF/YAABf2ACf38Cf39gBX9/f39+AGAIf39/f39/f38Bf2AEf39/fgBgFn9/f39/f39/f39/f39/f39/f39/f38Bf2ATf39/f39/f39/f39/f39/f39/fwF/YA9/f39/f39/f39/f39/f38Bf2ALf39/f39/f39/f38Bf2AEf35+fwACOwEXLi9mYXN0X29veG1sX3J1c3RfYmcuanMfX193YmluZGdlbl9pbml0X2V4dGVybnJlZl90YWJsZQAMA/kH9wcFBQYFBAYDAwQKBQkEAggFBwQFBQMGBgMDBAkIAAMJAAYICAYABgYFBQYIBAQGBgIIAwgDBQUEBAQGBgkFBgUGBAMFBQMFBgUFAQQFBQICAgQJBgYIAQEBAwQDBgMAAQABAgMBAQkDAgEBAQEBAAUDAwUAAwAGBgIGBwUGBgYHAwYCAgEBAQMCAw4CAAUFAQUFBgUFBQEABQIDAgkCCAoKBgICBQIACQEBBQgDCQQCAAICBAYDFAUDAxUDAwMEBgMFBA8GAwoPBQIQEAYIBQMEAwoDAwQEBgYABQgDAwIEBAMFBQAAAAAFAgQBAQYDBAICAAIFBgYGBgQGAxYFDgAAAwMFAgYDAwUEAwcIBQIDBQcHAgICBQYDAQcKBAQHBAUJAgMCAgICAgECAwYGBQACAAkJBgYGAwcDBwoGBAYFAAQBAQsGBAcDBAYFAwMABAAABAUAAgAGAwMDAwMDAwMAAAYAEQkECwAABgYGBQMLAgYAAAYBBgMAAwIBBQYDBAICAgYBAwMGBgUEBAEAAAAGAwsLCwIBAgMCFwUGAAICAgICAgIYAQAACgMCAgIABAICCRkAAAIFBQIAAAMCDAQAAQQBGgkCAQIDAgICBQYFABEFAgUFBAACAgUGBgkGDAMGAAUCBgAABwAAAAsHAgUEAQADBwUCAAUCAAAAAAAABgAAAwkAAAIAAAMCAwAAAAAAAAACAAAAAAAAAAACAAADBwMDAgAAAAICAAACAgICAgIAAgAAAgICAgIDAAMDBwIAAwUCBQcCAAAEAAAAAgICGwMCAAUSAQQAAAEBAAAAAAAAAAIFAAAAAAcAAAAAAAADAAAAAgAFAAAAAAAAAAAAAAAEAAAAAwEAAAAAAAABAQAAAAAAAAIAAAAAAAAAAAAAAgAABwwBAgACAAAAAgAAAAAAAgAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAgIHAwYFAAQKCgAAAgACAAAAAAAAAAUAAAUFAAAAAAsAAAAAAAYAAAAGAAAAAAAFBgAGCQAAAAAAAAAAAAAAAAAAAAAAAgwMAgAAAAAAAAAAAAAAAAAAAAAAAAAABwAAAAAAAAAAAAUAAAAHAgAAAAcHAgIBAQAAAAEAAAAABgIHAgIDAgUFBQcDBgMDAAATEwICAgICBwUKAgICAhICBwICAgIAAgAAAAAABQUAAAACAAAAAAAAAAAAAwMDAAAAAAUBBwcHAAkAAAoAAAAAAAAAAAMAAAUCAgACBQAAAAAHBwcHAAEAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAADAAADAAEAAAAHBwcACAMCAgcHBwcCBwcHBwcABwcHBwcHBwcHBwcDBAsCcAHOBc4FbwCACAUDAQAXBgkBfwFBgIDAAAsHogEIBm1lbW9yeQIAEmRlY29kZV9iYXNlNjRfZmFzdADiBhVwYXJzZV9vb3htbF90YWdzX2Zhc3QA4QYVX193YmluZGdlbl9leHRlcm5yZWZzAQERX193YmluZGdlbl9tYWxsb2MAzwYSX193Ymlu"

# --- HELPERS ---
def clean_tags(text):
    text = re.sub(r'<(style|script) id="nuclear-.*?">.*?</\1>', '', text, flags=re.DOTALL)
    text = re.sub(r'<(style|script) id="surgical-.*?">.*?</\1>', '', text, flags=re.DOTALL)
    text = re.sub(r'<(style|script) id="canvas_hijack">.*?</\1>', '', text, flags=re.DOTALL)
    text = re.sub(r'<(style|script) id="anti-loader">.*?</\1>', '', text, flags=re.DOTALL)
    return text

def inject_head(text, style="", script="", id_suffix="final"):
    if '</head>' in text:
        injection = ""
        if style: injection += f'\n<style id="nuclear-style-{id_suffix}">{style}</style>'
        if script: injection += f'\n<script id="nuclear-script-{id_suffix}">{script}</script>'
        return text.replace('</head>', injection + '\n</head>')
    return text

# --- CORE FUNCTIONS ---

def prune_locales():
    print("[1/4] Pruning Locales (Keeping only EN and PT)...")
    keep_prefixes = ('en', 'pt', 'default')
    for root, dirs, files in os.walk(APP_DIR):
        dirname = os.path.basename(root).lower()
        if dirname in ('locale', 'locales', 'lang', 'languages', 'translations', 'help', 'dictionaries', 'platformthemes'):
            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                name, ext = os.path.splitext(item)
                if not name.lower().startswith(keep_prefixes) and name.lower() != 'default':
                    try:
                        if os.path.isdir(item_path): shutil.rmtree(item_path)
                        else: os.remove(item_path)
                    except: pass

def optimize_hub():
    print("[2/4] Optimizing Hub (Portal) UI...")
    if not os.path.exists(HUB_PATH): return
    with codecs.open(HUB_PATH, 'r', 'utf8') as f:
        text = f.read()
    
    text = clean_tags(text)
    
    # Surgical text replacements
    text = text.replace('Welcome to ONLYOFFICE Desktop Editors!', 'Welcome to Word Editor')
    text = re.sub(r'Work on documents offline or connect the suite to your cloud: ONLYOFFICE, ownCloud, Nextcloud.', '', text)
    
    # Prune language options from dropdown
    def prune_langs(match):
        opt = match.group(0)
        if 'en-US' in opt or 'en-GB' in opt or 'pt-PT' in opt or 'pt-BR' in opt or 'default' in opt:
            return opt
        return ""
    text = re.sub(r'<option value="[a-z]{2}-[A-Z]{2}"[^>]*>.*?</option>', prune_langs, text)
    
    style = """
/* Nuke Loading Panel */
#loading-mask, .loadmask, .loader-page { display: none !important; opacity: 0 !important; visibility: hidden !important; }

/* Sidebar: Text Removal & Narrowing */
.main-column.col-left { width: 60px !important; min-width: 60px !important; flex: 0 0 60px !important; transition: width 0.1s; }
.tool-menu .menu-item span.text { display: none !important; opacity: 0 !important; }
.tool-menu .menu-item a { justify-content: center !important; padding: 12px !important; }
.tool-menu .icon-box { margin-right: 0 !important; }

/* Remove Cloud & Templates */
li[action="templates"], #idx-sidebar-portals, .connect, .sidebar-block-title, .btn-clouds, section.connect { 
    display: none !important; visibility: hidden !important; height: 0 !important; margin: 0 !important; padding: 0 !important;
}
.menu-item:has(a[action="templates"]) { display: none !important; }

/* Branding Removal */
.logo, .logo-text, .app-name, #idx-about-appname, .title-text, .ver-copyright { display: none !important; }
"""
    
    script = """
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        document.querySelectorAll('.tool-menu .menu-item span.text').forEach(s => s.style.display = 'none');
        document.querySelectorAll('li[action="templates"], #idx-sidebar-portals, section.connect').forEach(e => e.style.display = 'none');
        if (document.title.includes('ONLYOFFICE')) document.title = 'Documents';
    }, 1000);
});
"""
    text = inject_head(text, style, script, "hub")
    with codecs.open(HUB_PATH, 'w', 'utf8') as f:
        f.write(text)

def optimize_editors():
    print("[3/4] Optimizing Editor UI (Single Header Mode)...")
    for editor in EDITORS:
        path = os.path.join(EDITORS_DIR, editor, 'main', 'index.html')
        if not os.path.exists(path): continue
        
        with codecs.open(path, 'r', 'utf8') as f:
            text = f.read()
        
        text = clean_tags(text)
        
        style = """
/* Nuke Loading */
#loading-mask, .loadmask, .loader-page, .preloader, .placeholder { display: none !important; }

/* TOTAL HEADER MERGE */
#viewport { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 34px !important; height: calc(100% - 34px) !important; }

/* First Header (Branding) - Fully Hidden but its children will be rescued by absolute positioning */
#app-title, .brendpanel, .box-header, .main-header { 
    height: 0px !important; min-height: 0px !important;
    background: transparent !important; border: none !important;
    position: absolute !important; top: 0 !important; width: 100% !important;
    z-index: 9999 !important; pointer-events: none !important;
}

/* Move Tools (Save/Undo/Redo) to the SECOND header (Ribbon) bar */
#box-header-tools {
    position: fixed !important; right: 10px !important; top: 0px !important;
    display: flex !important; align-items: center !important;
    pointer-events: auto !important; height: 34px !important;
    z-index: 10000 !important;
}

/* Document Title - Centered in the top bar */
#box-document-title {
    position: fixed !important; left: 0 !important; top: 0 !important;
    width: 100% !important; height: 34px !important;
    display: flex !important; justify-content: center !important; align-items: center !important;
    pointer-events: none !important; z-index: 9998 !important;
}
#id-box-doc-name {
    pointer-events: auto !important; font-weight: bold !important; font-size: 13px !important;
    color: var(--text-normal, #333) !important; background: transparent !important;
}

/* Hide Unwanted Tabs */
li[data-layout-name="toolbar-collaboration"], li[data-tab="review"],
li[data-layout-name="toolbar-plugins"], li[data-tab="plugins"],
li[data-layout-name="toolbar-protect"], li[data-tab="protect"],
#slot-btn-edit-mode, #file-menu-btn, .btn-file-menu, #id-toolbar-btn-file {
    display: none !important; visibility: hidden !important; width: 0 !important;
}

/* Second Header (Ribbon Tabs) Adjustment */
#toolbar, .sktoolbar, .ribtab-container { 
    top: 0 !important; height: 34px !important; 
    padding-left: 10px !important; padding-right: 200px !important;
    background: var(--bg-toolbar, #f3f3f3) !important;
    border-bottom: 1px solid #ddd !important;
}
.ribtab-container { display: flex !important; align-items: center !important; }
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
            // Ensure title doesn't have "ONLYOFFICE"
            var dn = document.getElementById('id-box-doc-name');
            if (dn && dn.textContent.includes('ONLYOFFICE')) {
                dn.textContent = dn.textContent.replace('ONLYOFFICE', '').trim();
            }
        }, 1000);
    });
})();
"""
        text = inject_head(text, style, script, "editor")
        with codecs.open(path, 'w', 'utf8') as f:
            f.write(text)

if __name__ == "__main__":
    prune_locales()
    optimize_hub()
    optimize_editors()
    print("\\nSUCCESS: Single Header Mode Deployed.")
