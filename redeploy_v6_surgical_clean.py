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
def clean_all_injections(text):
    # Aggressively remove any previous custom tags
    text = re.sub(r'<(style|script) id="(nuclear|v\d|surgical|v3|v4|v5|anti-loader).*?">.*?</\1>', '', text, flags=re.DOTALL)
    return text

def inject_head(text, style="", script="", id_suffix="final"):
    if '</head>' in text:
        injection = ""
        if style: injection += f'\n<style id="clean-style-{id_suffix}">{style}</style>'
        if script: injection += f'\n<script id="clean-script-{id_suffix}">{script}</script>'
        return text.replace('</head>', injection + '\n</head>')
    return text

# --- CORE FUNCTIONS ---

def prune_languages():
    print("[1/4] Pruning languages...")
    keep_prefixes = ('en', 'pt', 'default')
    for root, dirs, files in os.walk(APP_DIR):
        if os.path.basename(root).lower() in ('locale', 'locales', 'lang', 'languages', 'translations', 'dictionaries'):
            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                if not item.lower().startswith(keep_prefixes) and item.lower() != 'default':
                    try:
                        if os.path.isdir(item_path): shutil.rmtree(item_path)
                        else: os.remove(item_path)
                    except: pass

def apply_hub_clean():
    print("[2/4] Applying clean Hub UI...")
    if not os.path.exists(HUB_PATH): return
    with codecs.open(HUB_PATH, 'r', 'utf8') as f:
        text = f.read()
    
    text = clean_all_injections(text)
    
    style = """
/* Sidebar icon-only mode */
.main-column.col-left { width: 60px !important; min-width: 60px !important; flex: 0 0 60px !important; }
.tool-menu .menu-item span.text { display: none !important; }
.tool-menu .menu-item a { justify-content: center !important; padding: 12px !important; }
.tool-menu .icon-box { margin-right: 0 !important; }

/* Remove Bloat */
li[action="templates"], #idx-sidebar-portals, .connect, .sidebar-block-title, .btn-clouds { display: none !important; }

/* No loading panel */
#loading-mask, .loadmask, .loader-page { display: none !important; }
"""
    text = inject_head(text, style, id_suffix="hub")
    with codecs.open(HUB_PATH, 'w', 'utf8') as f:
        f.write(text)

def apply_editor_clean():
    print("[3/4] Applying clean Editor UI (Single Toolbar)...")
    for editor in EDITORS:
        path = os.path.join(EDITORS_DIR, editor, 'main', 'index.html')
        if not os.path.exists(path): continue
        with codecs.open(path, 'r', 'utf8') as f:
            text = f.read()
        
        text = clean_all_injections(text)
        
        style = """
/* Nuke all loading elements */
#loading-mask, .loadmask, .loader-page, .preloader, .placeholder { display: none !important; }

/* Viewport should take full height except for the single toolbar */
#viewport { top: 34px !important; height: calc(100% - 34px) !important; }
.main-panel, #mainpnl, .app-body { top: 0px !important; height: 100% !important; }

/* REMOVE FIRST HEADER (Branding) */
.brendpanel, .main-header, #app-title, .box-header { 
    display: none !important; height: 0 !important; visibility: hidden !important; 
}

/* SINGLE TOOLBAR (The Ribbon) at the absolute top */
#toolbar, .sktoolbar, .ribbon { 
    position: fixed !important; top: 0 !important; left: 0 !important;
    width: 100% !important; height: 34px !important;
    background: #f3f3f3 !important; border-bottom: 1px solid #ccc !important;
    z-index: 10000 !important; display: flex !important; align-items: center !important;
}

/* RE-POSITION RESCUED ICONS (Save, Undo, Redo) */
/* Note: These IDs are often inside the first header, we MUST make them visible and fixed */
#box-header-tools, .box-header-tools {
    position: fixed !important; right: 10px !important; top: 0 !important;
    display: flex !important; align-items: center !important;
    height: 34px !important; z-index: 10002 !important;
    pointer-events: auto !important; visibility: visible !important;
}

/* CENTERED TITLE */
#box-document-title, .box-document-title {
    position: fixed !important; left: 0 !important; top: 0 !important;
    width: 100% !important; height: 34px !important;
    display: flex !important; justify-content: center !important; align-items: center !important;
    pointer-events: none !important; z-index: 10001 !important;
    visibility: visible !important;
}
#id-box-doc-name { pointer-events: auto !important; font-weight: bold !important; font-size: 13px !important; color: #333 !important; }

/* Adjust Ribbon Tabs container */
.ribtab-container { height: 34px !important; display: flex !important; align-items: center !important; padding-right: 250px !important; }

/* Remove unwanted tabs/menus */
li[data-layout-name*="collaboration"], li[data-tab="review"],
li[data-layout-name*="plugins"], li[data-tab="plugins"],
li[data-layout-name*="protect"], li[data-tab="protect"],
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
            // Rescue icons if they are hidden by parent 'display:none'
            var tools = document.getElementById('box-header-tools');
            if (tools && tools.parentElement && getComputedStyle(tools.parentElement).display === 'none') {
                document.body.appendChild(tools); // Move to body to escape hidden parent
            }
            var title = document.getElementById('box-document-title');
            if (title && title.parentElement && getComputedStyle(title.parentElement).display === 'none') {
                document.body.appendChild(title);
            }
        }, 1000);
    });
})();
"""
        text = inject_head(text, style, script, "editor")
        with codecs.open(path, 'w', 'utf8') as f:
            f.write(text)

if __name__ == "__main__":
    prune_languages()
    apply_hub_clean()
    apply_editor_clean()
    print("\\nSUCCESS: Surgical clean redeployment complete.")
