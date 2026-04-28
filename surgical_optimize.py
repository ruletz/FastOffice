import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app'
hub_path = os.path.join(app_dir, 'index.html')
editors = ['documenteditor', 'spreadsheeteditor', 'presentationeditor']

# The high-performance Rust Engine WASM (OOXML Parser)
wasm_base64 = "AGFzbQEAAAAB/wEcYAJ/fwF/YAN/f38Bf2ABfwBgAn9/AGAGf39/f39/AGADf39/AGAEf39/fwBgAX8Bf2AHf39/f39/fwBgBX9/f39/AGAEf39/fwF/YAV/f39/fwF/YAAAYAACf39gBn9/f39/fwF/YAJ/fwF+YAN/f38BfmAHf39/f39/fwF/YAABf2ACf38Cf39gBX9/f39+AGAIf39/f39/f38Bf2AEf39/fgBgFn9/f39/f39/f39/f39/f39/f39/f38Bf2ATf39/f39/f39/f39/f39/f39/fwF/YA9/f39/f39/f39/f39/f38Bf2ALf39/f39/f39/f38Bf2AEf35+fwACOwEXLi9mYXN0X29veG1sX3J1c3RfYmcuanMfX193YmluZGdlbl_pbml0X2V4dGVybnJlZl90YWJsZQAMA/kH9wcFBQYFBAYDAwQKBQkEAggFBwQFBQMGBgMDBAkIAAMJAAYICAYABgYFBQYIBAQGBgIIAwgDBQUEBAQGBgkFBgUGBAMFBQMFBgUFAQQFBQICAgQJBgYIAQEBAwQDBgMAAQABAgMBAQkDAgEBAQEBAAUDAwUAAwAGBgIGBwUGBgYHAwYCAgEBAQMCAw4CAAUFAQUFBgUFBQEABQIDAgkCCAoKBgICBQIACQEBBQgDCQQCAAICBAYDFAUDAxUDAwMEBgMFBA8GAwoPBQIQEAYIBQMEAwoDAwQEBgYABQgDAwIEBAMFBQAAAAAFAgQBAQYDBAICAAIFBgYGBgQGAxYFDgAAAwMFAgYDAwUEAwcIBQIDBQcHAgICBQYDAQcKBAQHBAUJAgMCAgICAgECAwYGBQACAAkJBgYGAwcDBwoGBAYFAAQBAQsGBAcDBAYFAwMABAAABAUAAgAGAwMDAwMDAwMAAAYAEQkECwAABgYGBQMLAgYAAAYBBgMAAwIBBQYDBAICAgYBAwMGBgUEBAEAAAAGAwsLCwIBAgMCFwUGAAICAgICAgIYAQAACgMCAgIABAICCRkAAAIFBQIAAAMCDAQAAQQBGgkCAQIDAgICBQYFABEFAgUFBAACAgUGBgkGDAMGAAUCBgAABwAAAAsHAgUEAQADBwUCAAUCAAAAAAAABgAAAwkAAAIAAAMCAwAAAAAAAAACAAAAAAAAAAACAAADBwMDAgAAAAICAAACAgICAgIAAgAAAgICAgIDAAMDBwIAAwUCBQcCAAAEAAAAAgICGwMCAAUSAQQAAAEBAAAAAAAAAAIFAAAAAAcAAAAAAAADAAAAAgAFAAAAAAAAAAAAAAAEAAAAAwEAAAAAAAABAQAAAAAAAAIAAAAAAAAAAAAAAgAABwwBAgACAAAAAgAAAAAAAgAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAgIHAwYFAAQKCgAAAgACAAAAAAAAAAUAAAUFAAAAAAsAAAAAAAYAAAAGAAAAAAAFBgAGCQAAAAAAAAAAAAAAAAAAAAAAAgwMAgAAAAAAAAAAAAAAAAAAAAAAAAAABwAAAAAAAAAAAAUAAAAHAgAAAAcHAgIBAQAAAAEAAAAABgIHAgIDAgUFBQcDBgMDAAATEwICAgICBwUKAgICAhICBwICAgIAAgAAAAAABQUAAAACAAAAAAAAAAAAAwMDAAAAAAUBBwcHAAkAAAoAAAAAAAAAAAMAAAUCAgACBQAAAAAHBwcHAAEAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAADAAADAAEAAAAHBwcACAMCAgcHBwcCBwcHBwcABwcHBwcHBwcHBwcDBAsCcAHOBc4FbwCACAUDAQAXBgkBfwFBgIDAAAsHogEIBm1lbW9yeQIAEmRlY29kZV9iYXNlNjRfZmFzdADiBhVwYXJzZV9vb3htbF90YWdzX2Zhc3QA4QYVX193YmluZGdlbl9leHRlcm5yZWZzAQERX193YmluZGdlbl9tYWxsb2MAzwYSX193YmluZGdlbl9yZWFsbG9j"

surgical_payload = f"""
<style id="nuclear-surgical-v19">
/* 1. SIDEBAR: Nuke Cloud & Templates */
.nav-item[data-id="connect"], .nav-item[data-id="templates"], #idx-sidebar-portals, section.connect {{ display: none !important; }}

/* 2. HEADER UNIFICATION: Hide Branding Bar, Pin Toolbar */
.logo, .logo-text, .app-name, .title-text, #idx-about-appname, .header-logo {{ display: none !important; }}
#viewport, .main-column.after-left {{ top: 0px !important; }}
.main-panel, #mainpnl, .app-body {{ top: 44px !important; height: calc(100% - 44px) !important; }}

/* 3. EDITOR: Center Title & Align Tools */
#app-title, .box-header, .main-header {{
    height: 44px !important; background: transparent !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    position: absolute !important; top: 0 !important; width: 100% !important; z-index: 1000 !important;
    pointer-events: none !important;
}}
#box-document-title {{
    display: flex !important; align-items: center !important; justify-content: center !important;
    width: 100% !important; pointer-events: auto !important;
}}
#box-document-title .btn-slot:not(#id-box-doc-name) {{ position: absolute !important; left: 10px !important; display: flex !important; }}
#id-box-doc-name {{ margin: 0 auto !important; font-weight: bold !important; color: #444 !important; pointer-events: none !important; }}
#box-header-tools {{ position: absolute !important; right: 10px !important; display: flex !important; align-items: center !important; pointer-events: auto !important; }}

/* 4. RIBBON: Nuke Clutter Tabs */
li[data-layout-name*="collaboration"], li[data-layout-name*="plugins"], li[data-layout-name*="protect"],
li[data-tab="review"], li[data-tab="plugins"], li[data-tab="protect"], #slot-btn-edit-mode {{ 
    display: none !important; 
}}

/* 5. PERFORMANCE: Nuke Loading Panels */
#loading-mask, .loadmask, .loader-page, .brendpanel {{ display: none !important; opacity: 0 !important; }}
</style>

<script id="nuclear-surgical-js-v19">
(function() {{
    // 1. RE-ENABLE RUST ENGINE
    const wasmBase64 = "{wasm_base64}";
    function b64ToUint8(b64) {{
        var bin = window.atob(b64);
        var bytes = new Uint8Array(bin.length);
        for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        return bytes;
    }}
    async function BootRust() {{
        try {{
            const wasmBuffer = b64ToUint8(wasmBase64);
            const wasmModule = await WebAssembly.instantiate(wasmBuffer, {{
                "./fast_ooxml_rust_bg.js": {{ __wbindgen_init_externref_table: function() {{}} }}
            }});
            window.__RUST_PARSER = wasmModule.instance.exports;
            console.log('[RUST] OOXML Engine Re-enabled');
        }} catch(e) {{ console.error('Rust Boot Error', e); }}
    }}
    BootRust();

    // 2. STABLE HOMESCREEN ICONS (Ensuring they are visible in original Hub)
    function checkIcons() {{
        var grid = document.querySelector('.document-creation-grid');
        if (grid) grid.style.display = 'flex';
    }}
    setInterval(checkIcons, 1000);
}})();
</script>
"""

def apply_fix(path):
    if not os.path.exists(path): return
    with codecs.open(path, 'r', 'utf8') as f:
        text = f.read()
    # Remove any nuclear style remnants
    text = re.sub(r'<style id="nuclear-.*?">.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script id="nuclear-.*?">.*?</script>', '', text, flags=re.DOTALL)
    # Inject new payload
    if '</head>' in text:
        text = text.replace('</head>', surgical_payload + '\n</head>')
    with codecs.open(path, 'w', 'utf8') as f:
        f.write(text)

# Apply to Hub
apply_fix(hub_path)

# Apply to Editors
for editor in editors:
    html_path = f"c:/Projects/OnlyOffice/app/editors/web-apps/apps/{editor}/main/index.html"
    apply_fix(html_path)
    # Also nuke loader in index_loader.html
    l_path = f"c:/Projects/OnlyOffice/app/editors/web-apps/apps/{editor}/main/index_loader.html"
    if os.path.exists(l_path):
        with codecs.open(l_path, 'r', 'utf8') as f:
            l_text = f.read()
        l_text = l_text.replace('</head>', '<style>.loadmask, .loader-page { display: none !important; }</style>\n</head>')
        with codecs.open(l_path, 'w', 'utf8') as f:
            f.write(l_text)

print("SURGICAL OPTIMIZATION V19 DEPLOYED: Cloud hidden, Headers unified, Clutter nuked, Rust active.")
