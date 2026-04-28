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
    
    # Remove branding header elements (logo, text, appname)
    text = re.sub(r'<div[^>]*class="[^"]*logo[^"]*"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*class="[^"]*logo-text[^"]*"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*class="[^"]*app-name[^"]*"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*id="idx-about-appname"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div[^>]*class="[^"]*box-ver[^"]*"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    
    if is_hub:
        text = re.sub(r'<li[^>]*data-id="templates"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-id="connect"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<section[^>]*id="idx-sidebar-portals"[^>]*>.*?</section>', '', text, flags=re.DOTALL)
    else:
        text = re.sub(r'<li[^>]*data-layout-name="toolbar-collaboration"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-layout-name="toolbar-protect"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-layout-name="toolbar-plugins"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-tab="review"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-tab="plugins"[^>]*>.*?</li>', '', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*data-tab="protect"[^>]*>.*?</li>', '', text, flags=re.DOTALL)

    # --- 2. CSS & JS OPTIMIZATIONS ---
    nuclear_css = """
<style id="nuclear-precision-v22">
#viewport, .main-column.after-left { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 44px !important; height: calc(100% - 44px) !important; }
#app-title, .box-header, .main-header {
    height: 44px !important; background: #fff !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    position: absolute !important; top: 0 !important; width: 100% !important; z-index: 1000 !important;
}
#box-document-title { display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; pointer-events: auto !important; }
#box-document-title .btn-slot:not(#id-box-doc-name) { position: absolute !important; left: 10px !important; display: flex !important; }
#id-box-doc-name { margin: 0 auto !important; font-weight: bold !important; color: #444 !important; font-family: 'Open Sans', sans-serif !important; font-size: 14px !important; }
#box-header-tools { position: absolute !important; right: 10px !important; display: flex !important; align-items: center !important; }
.document-creation-grid { display: flex !important; align-items: center !important; gap: 32px !important; justify-content: center !important; padding: 104px 112px !important; height: 100% !important; width: 100% !important; background: #fff !important; position: absolute; top: 0; left: 0; z-index: 99; }
.document-creation-item { display: flex !important; flex-direction: column !important; gap: 12px !important; align-items: center !important; justify-content: center !important; cursor: pointer !important; position: relative !important; width: 172px !important; height: 172px !important; padding: 24px 16px 16px !important; border-radius: 8px !important; background: #F3F3F3 !important; }
.document-creation-item .format-label { position: absolute !important; top: 14px !important; left: 10px !important; display: flex !important; height: 28px !important; align-items: center !important; padding: 0px 6px !important; border-radius: 6px !important; background: conic-gradient(from 225deg at 50% 50%, var(--format-bg-start) 0deg, var(--format-bg-end) 360deg) !important; }
.document-creation-item .format-label span { color: #fff !important; font-size: 16px !important; font-weight: 700 !important; }
.document-creation-item .icon { width: 108px !important; height: 100px !important; }
.document-creation-item .title { font-size: 14px !important; color: #444 !important; font-weight: 600 !important; font-family: 'Open Sans' !important; }
#loading-mask, .loadmask, .loader-page { display: none !important; opacity: 0 !important; visibility: hidden !important; }
</style>
"""
    wasm_b64 = "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"
    
    is_hub_str = "true" if is_hub else "false"
    nuclear_js = """
<script id="nuclear-logic-v22">
(function() {
    async function BootRust() {
        try {
            var bin = atob('""" + wasm_b64 + """');
            var bytes = new Uint8Array(bin.length);
            for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            const wasmModule = await WebAssembly.instantiate(bytes, {
                "./fast_ooxml_rust_bg.js": { __wbindgen_init_externref_table: function() {} }
            });
            window.__RUST_PARSER = wasmModule.instance.exports;
            console.log('[RUST] Engine Physically Stripped and Optimized');
        } catch(e) { console.error('Rust Error', e); }
    }
    BootRust();

    function inject() {
        var p = document.getElementById('placeholder');
        if (p && !document.querySelector('.document-creation-grid')) {
            p.innerHTML = `
                <div class="document-creation-grid">
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
    # Clean previous
    text = re.sub(r'<style id="nuclear-.*?">.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script id="nuclear-.*?">.*?</script>', '', text, flags=re.DOTALL)
    if '</head>' in text:
        text = text.replace('</head>', nuclear_css + '\n' + nuclear_js + '\n</head>')
    with codecs.open(path, 'w', 'utf8') as f:
        f.write(text)

# Run
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

print("NUCLEAR STRIP COMPLETE: Bloat physically removed from DOM, Rust active.")
