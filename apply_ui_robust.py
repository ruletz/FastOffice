import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app'
broken_path = 'c:/Projects/OnlyOffice/app_broken/index.html'
hub_path = os.path.join(app_dir, 'index.html')
editors = ['documenteditor', 'spreadsheeteditor', 'presentationeditor']

# --- 1. RESTORE SVG SYMBOLS (Essential for icons) ---
if os.path.exists(broken_path):
    with codecs.open(broken_path, 'r', 'utf8') as f:
        broken_text = f.read()
    match = re.search(r'<div class="injected-svg">.*?</div>', broken_text, flags=re.DOTALL)
    if match:
        svg_block = match.group(0)
        with codecs.open(hub_path, 'r', 'utf8') as f:
            hub_text = f.read()
        hub_text = re.sub(r'<div class="injected-svg">.*?</div>', '', hub_text, flags=re.DOTALL)
        if '</body>' in hub_text:
            hub_text = hub_text.replace('</body>', svg_block + '\n</body>')
        with codecs.open(hub_path, 'w', 'utf8') as f:
            f.write(hub_text)

# --- 2. HUB FINAL POLISH (Big Icons + Single Header) ---
with codecs.open(hub_path, 'r', 'utf8') as f:
    text = f.read()

hub_style = """<style id="nuclear-hub-v12">
/* HIDE 1st HEADER (Branding) */
.logo, .logo-text, .app-name, .title-text, #idx-about-appname { display: none !important; }

/* FIX SIDEBAR */
.nav-item[data-id="templates"], .nav-item[data-id="connect"], #idx-sidebar-portals { display: none !important; }

/* FORCE BIG ICONS CONTAINER */
#placeholder { display: block !important; }
.custom-big-icons {
    display: flex; justify-content: center; align-items: center;
    gap: 50px; height: 100%; padding-top: 100px;
}
.big-icon-item {
    display: flex; flex-direction: column; align-items: center; cursor: pointer;
}
.big-icon-item svg { width: 120px; height: 120px; margin-bottom: 10px; }
.big-icon-item span { font-family: 'Open Sans'; font-weight: 600; color: var(--text-normal, #444); }
</style>"""

hub_script = """<script id="nuclear-hub-js-v12">
document.addEventListener("DOMContentLoaded", function() {
    // Manual injection of Big Icons since internal scripts are failing
    var checkPlaceholder = setInterval(function() {
        var p = document.getElementById('placeholder');
        if (p && !document.querySelector('.custom-big-icons')) {
            p.innerHTML = `
                <div class="custom-big-icons">
                    <div class="big-icon-item" onclick="window.AscDesktopEditor.createDocument(65)">
                        <svg><use xlink:href="#file-docx"/></svg><span>Document</span>
                    </div>
                    <div class="big-icon-item" onclick="window.AscDesktopEditor.createDocument(257)">
                        <svg><use xlink:href="#file-xlsx"/></svg><span>Spreadsheet</span>
                    </div>
                    <div class="big-icon-item" onclick="window.AscDesktopEditor.createDocument(129)">
                        <svg><use xlink:href="#file-pptx"/></svg><span>Presentation</span>
                    </div>
                </div>
            `;
        }
    }, 500);
});
</script>"""

text = re.sub(r'<style id="nuclear-hub-v\d+">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-hub-js-v\d+">.*?</script>', '', text, flags=re.DOTALL)
if '</head>' in text: text = text.replace('</head>', hub_style + '\n</head>')
if '</body>' in text: text = text.replace('</body>', hub_script + '\n</body>')

with codecs.open(hub_path, 'w', 'utf8') as f:
    f.write(text)

# --- 3. EDITOR FINAL POLISH (Unify Header, Center Title) ---
for editor in editors:
    html_path = os.path.join(app_dir, 'editors', 'web-apps', 'apps', editor, 'main', 'index.html')
    if not os.path.exists(html_path): continue
    with codecs.open(html_path, 'r', 'utf8') as f:
        text = f.read()

    editor_style = """<style id="nuclear-editor-v12">
/* NUKE LOADING */
#loading-mask, .loadmask, .loader-page, .brendpanel { display: none !important; }

/* 1st HEADER GOES AWAY */
.logo-text, .title-text, .app-name { display: none !important; }

/* 2nd HEADER (TOOLBAR) TAKES CONTROL */
#viewport { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 44px !important; }

/* CENTER TITLE BETWEEN VIEW AND TOOLS */
#app-title, .box-header, .main-header {
    height: 44px !important; background: transparent !important;
    display: flex !important; align-items: center !important;
    justify-content: center !important;
}

#box-document-title {
    display: flex !important; align-items: center !important;
    justify-content: center !important; width: 100% !important;
}

/* Move Save/Print icons to the far left of the title bar */
#box-document-title .btn-slot:not(#id-box-doc-name) {
    position: absolute !important; left: 10px !important;
}

/* Center Title Text */
#id-box-doc-name {
    margin: 0 auto !important;
    font-weight: bold !important;
}

/* Move Search/Account to far right */
#box-header-tools {
    position: absolute !important; right: 10px !important;
    display: flex !important; align-items: center !important;
}

/* CLUTTER REMOVAL */
li[data-layout-name*="collaboration"], li[data-layout-name*="plugins"],
li[data-tab="review"], li[data-tab="plugins"], li[data-tab="protect"] {
    display: none !important;
}
</style>"""

    text = re.sub(r'<style id="nuclear-editor-v\d+">.*?</style>', '', text, flags=re.DOTALL)
    if '</head>' in text: text = text.replace('</head>', editor_style + '\n</head>')
    with codecs.open(html_path, 'w', 'utf8') as f:
        f.write(text)

print("UI V12 DEPLOYED: Single header unified, Title centered, Big Icons forced.")
