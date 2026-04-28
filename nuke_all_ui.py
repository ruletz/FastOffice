import codecs
import re
import os

app_dir = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps'

targets = [
    'documenteditor/main/index.html',
    'spreadsheeteditor/main/index.html',
    'presentationeditor/main/index.html'
]

style_and_script = """<style id="nuclear-style-safe">
/* 1. Eliminate visual clutter safely */
li[data-layout-name="toolbar-collaboration"],
li[data-layout-name="toolbar-plugins"],
li[data-layout-name="toolbar-protect"],
div[data-layout-name="header-editMode"],
li[data-tab="review"],
li[data-tab="plugins"],
li[data-tab="protect"],
#slot-btn-edit-mode,
.logo-text, .title-text, .app-name, span[class*='logo-text'] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* 2. Overlap the Top Header and the Toolbar to save space */
#app-title, .box-header, .main-header {
    height: 0px !important;
    min-height: 0px !important;
    border: none !important;
    background: transparent !important;
}
#toolbar, .toolbar, #viewport {
    top: 0px !important; 
}
.main-panel, #mainpnl, .app-body {
    top: 84px !important; 
}

/* 3. The Save/Undo/Title buttons are inside #app-title. 
   We float them cleanly over the toolbar space so the DOM structure remains intact! */
#box-document-title {
    position: absolute !important;
    top: 6px !important;
    right: 20px !important;
    display: flex !important;
    align-items: center !important;
    z-index: 9999 !important;
}
/* Ensure the Save/Undo buttons look like regular toolbar icons */
#box-document-title button {
    background: transparent !important;
    border: none !important;
}
#box-document-title .custom-header-title {
    color: var(--text-normal) !important;
    font-size: 13px !important;
}
/* Hide the home btn logo icon */
#slot-btn-dt-home i.btn-home {
    display: none !important;
}
#slot-btn-dt-home { display: none !important; }

/* 4. The mode switchers */
button[id*='mode'], button[id*='cloud'] {
    display: none !important;
}
</style>
<script id="nuclear_ui_safe">
// Pure CSS handles the visual cleanup! The JS just ensures we don't have text we missed.
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        var tabs = document.querySelectorAll("li.ribtab, a.ribtab, button");
        for (var i = 0; i < tabs.length; i++) {
            var txt = (tabs[i].innerText || tabs[i].textContent || "").toLowerCase();
            if (txt.includes("collaboration") || 
                txt.includes("plugin") || 
                txt.includes("protection") || 
                txt.startsWith("ai ") || 
                txt.includes("editing") ||
                txt.includes("reviewing") ||
                txt.includes("viewing") ) {
                tabs[i].style.display = "none !important";
                tabs[i].style.visibility = "hidden !important";
            }
        }
    }, 1000); // Check once a second, no heavy DOM manipulation
});
</script>"""

for t in targets:
    html_path = os.path.join(app_dir, t)
    if os.path.exists(html_path):
        with codecs.open(html_path, 'r', 'utf8') as f:
            text = f.read()

        # Clean previous 
        text = re.sub(r'<style id="nuclear-style.*?">.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<script id="nuclear_ui.*?">.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<script id="dom_dumper_local">.*?</script>', '', text, flags=re.DOTALL)
        
        if '</head>' in text:
            # Insert just before </head>
            text = text.replace('</head>', style_and_script + '\n</head>')

        with codecs.open(html_path, 'w', 'utf8') as f:
            f.write(text)
        print(f"Patched {t}")
    else:
        print(f"File not found: {html_path}")
