import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app'
hub_path = os.path.join(app_dir, 'index.html')

def clean_and_fix_hub():
    with codecs.open(hub_path, 'r', 'utf8') as f:
        text = f.read()

    # 1. TOTAL CLEANUP
    text = re.sub(r'<style id="nuclear-.*?">.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script id="nuclear-.*?">.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style id="nuclear_ui_optimization">.*?</style>', '', text, flags=re.DOTALL)

    # 2. PRECISION CSS
    style = """<style id="nuclear-hub-v21">
/* NUKE 1st HEADER (Branding) */
.logo, .logo-text, .app-name, .title-text, #idx-about-appname, .header-logo, .box-ver { display: none !important; }

/* FIX SIDEBAR */
.nav-item[data-id="templates"], .nav-item[data-id="connect"], #idx-sidebar-portals { display: none !important; }

/* STABLE BIG ICONS GRID */
.document-creation-grid {
    display: flex !important; align-items: center !important; gap: 32px !important; justify-content: center !important;
    padding: 104px 112px !important; height: 100% !important; width: 100% !important;
    background: #fff !important; position: absolute !important; top: 0 !important; left: 0 !important; z-index: 100 !important;
}
.document-creation-item {
    display: flex !important; flex-direction: column !important; gap: 12px !important; align-items: center !important; justify-content: center !important;
    flex-shrink: 0 !important; cursor: pointer !important; position: relative !important; width: 172px !important; height: 172px !important;
    padding: 24px 16px 16px !important; border-radius: 8px !important; background: #F3F3F3 !important; transition: background 0.2s !important;
}
.document-creation-item:hover { background: #E5E5E5 !important; }
.document-creation-item .format-label {
    position: absolute !important; top: 14px !important; left: 10px !important; display: flex !important; height: 28px !important;
    align-items: center !important; padding: 0px 6px !important; border-radius: 6px !important;
    background: conic-gradient(from 225deg at 50% 50%, var(--format-bg-start) 0deg, var(--format-bg-end) 360deg) !important;
}
.document-creation-item .format-label span { color: #fff !important; font-size: 16px !important; font-weight: 700 !important; }
.document-creation-item .icon { width: 108px !important; height: 100px !important; }
.document-creation-item .title { font-size: 14px !important; color: #444 !important; font-weight: 600 !important; font-family: 'Open Sans', sans-serif !important; }

/* FIX FONT FOR TITLE */
#id-box-doc-name, .title { font-family: 'Open Sans', sans-serif !important; }
</style>"""

    script = """<script id="nuclear-hub-js-v21">
(function() {
    function injectGrid() {
        var placeholder = document.getElementById('placeholder');
        if (placeholder && !document.querySelector('.document-creation-grid')) {
            placeholder.innerHTML = `
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
    var obs = new MutationObserver(function() {
        if (!document.querySelector('.document-creation-grid')) injectGrid();
    });
    document.addEventListener("DOMContentLoaded", function() {
        obs.observe(document.body, { childList: true, subtree: true });
        injectGrid();
    });
})();
</script>"""

    if '</head>' in text: text = text.replace('</head>', style + '\n</head>')
    if '</body>' in text: text = text.replace('</body>', script + '\n</body>')
    with codecs.open(hub_path, 'w', 'utf8') as f:
        f.write(text)

clean_and_fix_hub()
