import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<style id="nuclear-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui.*?">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-style-v5">
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
    width: 0 !important;
    margin: 0 !important;
}

button[id*='mode'], button[id*='cloud'], #slot-btn-dt-home i.btn-home, #slot-btn-dt-home {
    display: none !important;
}

#toolbar, .toolbar, #viewport { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 84px !important; }

#app-title, .box-header, .main-header {
    height: 0px !important; min-height: 0px !important;
    border: none !important; background: transparent !important;
    position: absolute !important; top: 0px !important; z-index: 100 !important;
    left: 0 !important; right: 0 !important; display: block !important;
}

/* Float Save/Undo leftwards, dynamically shifted */
#box-document-title {
    position: absolute !important;
    top: 6px !important; 
    left: 450px !important; /* Starts after standard sized tabs */
    display: flex !important;
    align-items: center !important;
    z-index: 110 !important;
    width: calc(100vw - 450px - 150px) !important; 
}

/* Ensure the title text is flexible and perfectly centered */
#id-box-doc-name {
    flex-grow: 1 !important;
    text-align: center !important;
    padding-right: 450px !important; /* visual counterbalance to keep it strictly center of screen */
    color: var(--text-normal) !important;
    font-size: 13px !important;
    pointer-events: auto !important;
}

/* Keep the tools inside usable */
#box-document-title .btn-slot {
    pointer-events: auto !important;
}

/* Float the user/search tools specifically to the top right */
#box-header-tools, .box-header-tools, .box-header .extra {
    position: absolute !important;
    top: 6px !important;
    right: 15px !important;
    display: flex !important;
    z-index: 110 !important;
}

/* Force flex reorder: user AFTER search */
#slot-btn-search, .btn-search { order: -2 !important; }
#slot-btn-user, .btn-user { order: -1 !important; }

</style>"""

script = """<script id="nuclear_ui_v5">
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
                txt.includes("viewing") ||
                txt.includes("cloud") ) {
                tabs[i].style.display = "none";
            }
        }
    }, 1000);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("V5 UI Deployed")
