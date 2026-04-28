import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app'
hub_path = os.path.join(app_dir, 'index.html')
editors = ['documenteditor', 'spreadsheeteditor', 'presentationeditor']

# --- FINAL RECONSTRUCTION (COPY FROM ORIGINAL) ---

hub_style = """<style id="nuclear-final-style">
/* 1. ORIGINAL DOCUMENT CREATION GRID (Copied from Source) */
.document-creation-grid {
    display: flex; align-items: center; gap: 32px; justify-content: center;
    padding: 104px 112px; height: 100%; width: 100%;
    background: #fff; position: absolute; top: 0; left: 0; z-index: 100;
}
.document-creation-item {
    display: flex; flex-direction: column; gap: 12px; align-items: center; justify-content: center;
    flex-shrink: 0; cursor: pointer; position: relative; width: 172px; height: 172px;
    padding: 24px 16px 16px; border-radius: 8px; background: #F3F3F3; transition: background 0.2s;
}
.document-creation-item:hover { background: #E5E5E5; }
.document-creation-item .format-label {
    position: absolute; top: 14px; left: 10px; display: flex; height: 28px;
    align-items: center; padding: 0px 6px; border-radius: 6px;
    background: conic-gradient(from 225deg at 50% 50%, var(--format-bg-start) 0deg, var(--format-bg-end) 360deg);
}
.document-creation-item .format-label span { color: #fff; font-size: 16px; font-weight: 700; }
.document-creation-item .icon { width: 108px; height: 100px; }
.document-creation-item .title { font-size: 14px; color: #444; font-weight: 600; }

/* 2. HEADER UNIFICATION (Single Header) */
.logo, .logo-text, .app-name, .title-text, #idx-about-appname, .header-logo, .brendpanel { display: none !important; }
#viewport, .main-column.after-left { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 44px !important; height: calc(100% - 44px) !important; }

#app-title, .box-header, .main-header {
    height: 44px !important; background: transparent !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    position: absolute !important; top: 0 !important; width: 100% !important; z-index: 1000 !important;
    pointer-events: none !important;
}
#box-document-title {
    display: flex !important; align-items: center !important; justify-content: center !important;
    width: 100% !important; pointer-events: auto !important;
}
#box-document-title .btn-slot:not(#id-box-doc-name) { position: absolute !important; left: 10px !important; display: flex !important; }
#id-box-doc-name { margin: 0 auto !important; font-weight: bold !important; color: #444 !important; }
#box-header-tools { position: absolute !important; right: 10px !important; display: flex !important; align-items: center !important; pointer-events: auto !important; }

/* 3. CLUTTER & LOADING */
li[data-layout-name*="collaboration"], li[data-layout-name*="plugins"],
li[data-tab="review"], li[data-tab="plugins"], li[data-tab="protect"],
#slot-btn-edit-mode, .nav-item[data-id="templates"], .nav-item[data-id="connect"] { display: none !important; }
#loading-mask, .loadmask, .loader-page { display: none !important; }
</style>"""

hub_script = """<script id="nuclear-final-js">
(function() {
    function injectOriginalGrid() {
        var placeholder = document.getElementById('placeholder');
        if (!placeholder) return;
        if (document.querySelector('.document-creation-grid')) return;

        placeholder.innerHTML = `
            <div class="document-creation-grid">
                <div class="document-creation-item" onclick="window.AscDesktopEditor.createDocument(65)" style="--format-bg-start: #4298C5; --format-bg-end: #2D84B2;">
                    <div class="format-label"><span>DOCX</span></div>
                    <svg class="icon"><use xlink:href="#file-docx"></use></svg>
                    <div class="title">Document</div>
                </div>
                <div class="document-creation-item" onclick="window.AscDesktopEditor.createDocument(257)" style="--format-bg-start: #5BB514; --format-bg-end: #318C2B;">
                    <div class="format-label"><span>XLSX</span></div>
                    <svg class="icon"><use xlink:href="#file-xlsx"></use></svg>
                    <div class="title">Spreadsheet</div>
                </div>
                <div class="document-creation-item" onclick="window.AscDesktopEditor.createDocument(129)" style="--format-bg-start: #F4893A; --format-bg-end: #DE7341;">
                    <div class="format-label"><span>PPTX</span></div>
                    <svg class="icon"><use xlink:href="#file-pptx"></use></svg>
                    <div class="title">Presentation</div>
                </div>
            </div>
        `;
    }

    var observer = new MutationObserver(function() {
        var colCenter = document.querySelector('.col-center');
        if (colCenter && !document.querySelector('.document-creation-grid')) {
            injectOriginalGrid();
        }
    });

    document.addEventListener("DOMContentLoaded", function() {
        observer.observe(document.body, { childList: true, subtree: true });
        injectOriginalGrid();
    });
})();
</script>"""

# Apply to Hub
with codecs.open(hub_path, 'r', 'utf8') as f:
    text = f.read()
text = re.sub(r'<style id="nuclear-.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-.*?">.*?</script>', '', text, flags=re.DOTALL)
if '</head>' in text: text = text.replace('</head>', hub_style + '\n</head>')
if '</body>' in text: text = text.replace('</body>', hub_script + '\n</body>')
with codecs.open(hub_path, 'w', 'utf8') as f:
    f.write(text)

# Apply to Editors
for editor in editors:
    html_path = os.path.join(app_dir, 'editors', 'web-apps', 'apps', editor, 'main', 'index.html')
    if not os.path.exists(html_path): continue
    with codecs.open(html_path, 'r', 'utf8') as f:
        text = f.read()
    text = re.sub(r'<style id="nuclear-.*?">.*?</style>', '', text, flags=re.DOTALL)
    if '</head>' in text: text = text.replace('</head>', hub_style + '\n</head>')
    with codecs.open(html_path, 'w', 'utf8') as f:
        f.write(text)

print("TOTAL UI SYNCED: Original HTML/CSS copied, headers unified, title centered.")
