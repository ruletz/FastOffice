import codecs
import re
import os
import shutil

# --- CONFIGURATION ---
APP_DIR = r'C:/Projects/OnlyOffice/app'
EDITORS_DIR = os.path.join(APP_DIR, 'editors', 'web-apps', 'apps')
HUB_PATH = os.path.join(APP_DIR, 'index.html')
EDITORS = ['documenteditor', 'spreadsheeteditor', 'presentationeditor', 'pdfeditor']

# --- RUST WASM ---
WASM_B64 = "AGFzbQEAAAAB/wEcYAJ/fwF/YAN/f38Bf2ABfwBgAn9/AGAGf39/f39/AGADf39/AGAEf39/fwBgAX8Bf2AHf39/f39/fwBgBX9/f39/AGAEf39/fwF/YAV/f39/fwF/YAAAYAACf39gBn9/f39/fwF/YAJ/fwF+YAN/f38BfmAHf39/f39/fwF/YAABf2ACf38Cf39gBX9/f39+AGAIf39/f39/f38Bf2AEf39/fgBgFn9/f39/f39/f39/f39/f39/f39/f38Bf2ATf39/f39/f39/f39/f39/f39/fwF/YA9/f39/f39/f39/f39/f38Bf2ALf39/f39/f39/f38Bf2AEf35+fwACOwEXLi9mYXN0X29veG1sX3J1c3RfYmcuanMfX193YmluZGdlbl9pbml0X2V4dGVybnJlZl90YWJsZQAMA/kH9wcFBQYFBAYDAwQKBQkEAggFBwQFBQMGBgMDBAkIAAMJAAYICAYABgYFBQYIBAQGBgIIAwgDBQUEBAQGBgkFBgUGBAMFBQMFBgUFAQQFBQICAgQJBgYIAQEBAwQDBgMAAQABAgMBAQkDAgEBAQEBAAUDAwUAAwAGBgIGBwUGBgYHAwYCAgEBAQMCAw4CAAUFAQUFBgUFBQEABQIDAgkCCAoKBgICBQIACQEBBQgDCQQCAAICBAYDFAUDAxUDAwMEBgMFBA8GAwoPBQIQEAYIBQMEAwoDAwQEBgYABQgDAwIEBAMFBQAAAAAFAgQBAQYDBAICAAIFBgYGBgQGAxYFDgAAAwMFAgYDAwUEAwcIBQIDBQcHAgICBQYDAQcKBAQHBAUJAgMCAgICAgECAwYGBQACAAkJBgYGAwcDBwoGBAYFAAQBAQsGBAcDBAYFAwMABAAABAUAAgAGAwMDAwMDAwMAAAYAEQkECwAABgYGBQMLAgYAAAYBBgMAAwIBBQYDBAICAgYBAwMGBgUEBAEAAAAGAwsLCwIBAgMCFwUGAAICAgICAgIYAQAACgMCAgIABAICCRkAAAIFBQIAAAMCDAQAAQQBGgkCAQIDAgICBQYFABEFAgUFBAACAgUGBgkGDAMGAAUCBgAABwAAAAsHAgUEAQADBwUCAAUCAAAAAAAABgAAAwkAAAIAAAMCAwAAAAAAAAACAAAAAAAAAAACAAADBwMDAgAAAAICAAACAgICAgIAAgAAAgICAgIDAAMDBwIAAwUCBQcCAAAEAAAAAgICGwMCAAUSAQQAAAEBAAAAAAAAAAIFAAAAAAcAAAAAAAADAAAAAgAFAAAAAAAAAAAAAAAEAAAAAwEAAAAAAAABAQAAAAAAAAIAAAAAAAAAAAAAAgAABwwBAgACAAAAAgAAAAAAAgAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAgIHAwYFAAQKCgAAAgACAAAAAAAAAAUAAAUFAAAAAAsAAAAAAAYAAAAGAAAAAAAFBgAGCQAAAAAAAAAAAAAAAAAAAAAAAgwMAgAAAAAAAAAAAAAAAAAAAAAAAAAABwAAAAAAAAAAAAUAAAAHAgAAAAcHAgIBAQAAAAEAAAAABgIHAgIDAgUFBQcDBgMDAAATEwICAgICBwUKAgICAhICBwICAgIAAgAAAAAABQUAAAACAAAAAAAAAAAAAwMDAAAAAAUBBwcHAAkAAAoAAAAAAAAAAAMAAAUCAgACBQAAAAAHBwcHAAEAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAADAAADAAEAAAAHBwcACAMCAgcHBwcCBwcHBwcABwcHBwcHBwcHBwcDBAsCcAHOBc4FbwCACAUDAQAXBgkBfwFBgIDAAAsHogEIBm1lbW9yeQIAEmRlY29kZV9iYXNlNjRfZmFzdADiBhVwYXJzZV9vb3htbF90YWdzX2Zhc3QA4QYVX193YmluZGdlbl9leHRlcm5yZWZzAQERX193YmluZGdlbl9tYWxsb2MAzwYSX193Ymlu"

# --- HELPERS ---
def inject_head(text, style="", script="", id_suffix="v5"):
    if '</head>' in text:
        injection = ""
        if style: injection += f'\n<style id="v5-style-{id_suffix}">{style}</style>'
        if script: injection += f'\n<script id="v5-script-{id_suffix}">{script}</script>'
        return text.replace('</head>', injection + '\n</head>')
    return text

# --- CORE FUNCTIONS ---

def prune_languages():
    print("[1/5] Pruning languages...")
    keep_prefixes = ('en', 'pt', 'default')
    for root, dirs, files in os.walk(APP_DIR):
        dirname = os.path.basename(root).lower()
        if dirname in ('locale', 'locales', 'lang', 'languages', 'translations', 'dictionaries'):
            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                name, ext = os.path.splitext(item)
                if not name.lower().startswith(keep_prefixes) and name.lower() != 'default':
                    try:
                        if os.path.isdir(item_path): shutil.rmtree(item_path)
                        else: os.remove(item_path)
                    except: pass

def apply_hub_ui():
    print("[2/5] Applying Hub UI...")
    if not os.path.exists(HUB_PATH): return
    with codecs.open(HUB_PATH, 'r', 'utf8') as f:
        text = f.read()
    
    style = """
.main-column.col-left { width: 60px !important; min-width: 60px !important; flex: 0 0 60px !important; }
.tool-menu .menu-item span.text { display: none !important; }
.tool-menu .menu-item a { justify-content: center !important; padding: 12px !important; }
.tool-menu .icon-box { margin-right: 0 !important; }
li[action="templates"], #idx-sidebar-portals, .connect, .sidebar-block-title, .btn-clouds { display: none !important; }
#loading-mask, .loadmask, .loader-page { display: none !important; }
"""
    text = inject_head(text, style, id_suffix="hub")
    with codecs.open(HUB_PATH, 'w', 'utf8') as f:
        f.write(text)

def apply_editor_ui():
    print("[3/5] Applying Editor UI (Consolidating first icons into toolbar)...")
    for editor in EDITORS:
        path = os.path.join(EDITORS_DIR, editor, 'main', 'index.html')
        if not os.path.exists(path): continue
        with codecs.open(path, 'r', 'utf8') as f:
            text = f.read()
            
        style = """
#loading-mask, .loadmask, .loader-page, .preloader { display: none !important; }
#viewport { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 32px !important; height: calc(100% - 32px) !important; }

/* Remove First Header (Branding) */
.brendpanel, .main-header, #app-title { display: none !important; height: 0 !important; }

/* Second Header (Ribbon/Toolbar) as the TOP bar */
#toolbar, .sktoolbar { 
    position: fixed !important; top: 0 !important; left: 0 !important;
    width: 100% !important; height: 32px !important;
    z-index: 10000 !important; background: #f3f3f3 !important;
    display: flex !important; align-items: center !important;
    padding: 0 10px !important; box-sizing: border-box !important;
    border-bottom: 1px solid #ddd !important;
}

/* Move First Icons (Save, etc) to Right side of this TOP bar */
#box-header-tools {
    position: absolute !important; right: 10px !important; top: 0 !important;
    display: flex !important; align-items: center !important;
    height: 32px !important; z-index: 10001 !important;
    pointer-events: auto !important;
}

/* Title centered in this bar, between the 'view' (tabs) and the icons */
#box-document-title {
    position: absolute !important; left: 0 !important; top: 0 !important;
    width: 100% !important; height: 32px !important;
    display: flex !important; justify-content: center !important; align-items: center !important;
    pointer-events: none !important; z-index: 9999 !important;
}
#id-box-doc-name { pointer-events: auto !important; font-weight: bold !important; font-size: 13px !important; }

.ribtab-container { height: 32px !important; display: flex !important; align-items: center !important; padding-right: 250px !important; }

li[data-layout-name="toolbar-collaboration"], li[data-tab="review"],
li[data-layout-name="toolbar-plugins"], li[data-tab="plugins"],
li[data-layout-name="toolbar-protect"], li[data-tab="protect"],
#slot-btn-edit-mode, #file-menu-btn, .btn-file-menu {
    display: none !important; visibility: hidden !important;
}
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
            document.querySelectorAll("li.ribtab, a.ribtab").forEach(t => {
                var txt = (t.textContent || "").toLowerCase();
                if (txt.includes("collaboration") || txt.includes("plugin") || txt.includes("protection") || txt.includes("review")) {
                    t.style.display = "none";
                }
            });
        }, 1000);
    });
})();
"""
        text = inject_head(text, style, script, "editor")
        with codecs.open(path, 'w', 'utf8') as f:
            f.write(text)

if __name__ == "__main__":
    prune_languages()
    apply_hub_ui()
    apply_editor_ui()
    print("\\nSUCCESS: Consolidated toolbar redeployed.")
