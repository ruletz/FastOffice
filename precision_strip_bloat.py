import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app'
hub_path = os.path.join(app_dir, 'index.html')
editors = ['documenteditor', 'spreadsheeteditor', 'presentationeditor']

def strip_and_optimize(path, is_hub=False):
    if not os.path.exists(path): return
    with codecs.open(path, 'r', 'utf8') as f:
        text = f.read()

    # --- 1. PHYSICAL REMOVAL (NUKING THE DOM) ---
    # Specifically target the 1st header containers found in ONLYOFFICE
    # branding header, logo text, version info, account info in hub
    text = re.sub(r'<div[^>]*class="[^"]*box-ver[^"]*"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*id="idx-about-appname"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    
    if is_hub:
        # Sidebar cleanup
        text = re.sub(r'<li[^>]*data-id="templates"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-id="connect"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<section[^>]*id="idx-sidebar-portals"[^>]*>.*?</section>', '', text, flags=re.DOTALL)
    else:
        # Editor tabs cleanup
        text = re.sub(r'<li[^>]*data-layout-name="toolbar-collaboration"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-layout-name="toolbar-protect"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-layout-name="toolbar-plugins"[^>]*>.*?</li>', '', text, flags=re.DOTALL)

    # --- 2. CSS FOR UNIFICATION & CENTERING (NO BACKGROUND OVERRIDE) ---
    precision_css = """
<style id="nuclear-final-precision">
/* HIDE LOGOS & BRANDING TEXT WITHOUT OVERWRITING BACKGROUND */
.logo, .logo-text, .app-name, .title-text, .header-logo, .brendpanel { display: none !important; opacity: 0 !important; }

/* UNIFY HEADER */
#viewport, .main-column.after-left { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 44px !important; height: calc(100% - 44px) !important; }

/* CENTER TITLE & POSITION TOOLS (Editor) */
#app-title, .box-header, .main-header {
    height: 44px !important; background: transparent !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    position: absolute !important; top: 0 !important; width: 100% !important; z-index: 1000 !important;
}
#box-document-title { display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; pointer-events: auto !important; }
#box-document-title .btn-slot:not(#id-box-doc-name) { position: absolute !important; left: 10px !important; display: flex !important; }
#id-box-doc-name { margin: 0 auto !important; font-weight: bold !important; color: #444 !important; font-family: 'Open Sans', sans-serif !important; font-size: 14px !important; }
#box-header-tools { position: absolute !important; right: 10px !important; display: flex !important; align-items: center !important; }

/* NUKE LOADING */
#loading-mask, .loadmask, .loader-page { display: none !important; }
</style>
"""
    wasm_b64 = "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"
    
    is_hub_str = "true" if is_hub else "false"
    nuclear_js = """
<script id="nuclear-logic-v22">
(function() {
    // 1. RUST ENGINE
    async function BootRust() {
        try {
            var bin = atob('""" + wasm_b64 + """');
            var bytes = new Uint8Array(bin.length);
            for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            const wasmModule = await WebAssembly.instantiate(bytes, {
                "./fast_ooxml_rust_bg.js": { __wbindgen_init_externref_table: function() {} }
            });
            window.__RUST_PARSER = wasmModule.instance.exports;
            console.log('[RUST] Engine Active');
        } catch(e) { console.error('Rust Error', e); }
    }
    BootRust();

    // 2. STABLE GRID INJECTION
    function inject() {
        var p = document.getElementById('placeholder');
        if (p && !document.querySelector('.document-creation-grid')) {
            p.innerHTML = `
                <div class="document-creation-grid" style="background: transparent !important;">
                    <div class="document-creation-item" onclick="window.AscDesktopEditor.createDocument(64)" style="--format-bg-start: #4298C5; --format-bg-end: #2D84B2;">
                        <div class="format-label"><span>DOCX</span></div>
                        <svg class="icon"><use xlink:href="#file-docx"></use></svg>
                        <div class="title">Document</div>
                    </div>
                    <div class="document-creation-item" onclick="window.AscDesktopEditor.createDocument(256)" style="--format-bg-start: #5BB514; --format-bg-end: #318C2B;">
                        <div class="format-label"><span>XLSX</span></div>
                        <svg class="icon"><use xlink:href="#file-xlsx"></use></svg>
                        <div class="title">Spreadsheet</div>
                    </div>
                    <div class="document-creation-item" onclick="window.AscDesktopEditor.createDocument(128)" style="--format-bg-start: #F4893A; --format-bg-end: #DE7341;">
                        <div class="format-label"><span>PPTX</span></div>
                        <svg class="icon"><use xlink:href="#file-pptx"></use></svg>
                        <div class="title">Presentation</div>
                    </div>
                </div>`;
        }
    }
    if (""" + is_hub_str + """) {
        var obs = new MutationObserver(function() { if (!document.querySelector('.document-creation-grid')) inject(); });
        document.addEventListener("DOMContentLoaded", function() { obs.observe(document.body, { childList: true, subtree: true }); inject(); });
    }
})();
</script>
"""
    # Remove previous attempts
    text = re.sub(r'<style id="nuclear-.*?">.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script id="nuclear-.*?">.*?</script>', '', text, flags=re.DOTALL)
    if '</head>' in text:
        text = text.replace('</head>', precision_css + '\n' + nuclear_js + '\n</head>')
    with codecs.open(path, 'w', 'utf8') as f:
        f.write(text)

# Execution
strip_and_optimize(hub_path, is_hub=True)
for editor in editors:
    e_path = os.path.join(app_dir, 'editors', 'web-apps', 'apps', editor, 'main', 'index.html')
    strip_and_optimize(e_path, is_hub=False)
    l_path = os.path.join(app_dir, 'editors', 'web-apps', 'apps', editor, 'main', 'index_loader.html')
    if os.path.exists(l_path):
        with codecs.open(l_path, 'r', 'utf8') as f:
            l_text = f.read()
        l_text = l_text.replace('</head>', '<style>.loadmask, .loader-page { display: none !important; }</style>\n</head>')
        with codecs.open(l_path, 'w', 'utf8') as f:
            f.write(l_text)

print("PRECISION STRIP COMPLETE: Native theme preserved, bloat removed.")
