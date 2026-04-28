import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<style id="nuclear-style-v10">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui_v10">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-style-v11">
/* 1. Eliminate tabs cleanly */
li[data-layout-name="toolbar-collaboration"],
li[data-layout-name="toolbar-plugins"],
li[data-layout-name="toolbar-protect"],
div[data-layout-name="header-editMode"],
li[data-tab="review"],
li[data-tab="plugins"],
li[data-tab="protect"],
#slot-btn-edit-mode,
.logo-text, .title-text, .app-name, span[class*='logo-text'] {
    position: absolute !important;
    left: -9999px !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

button[id*='mode'], button[id*='cloud'], #slot-btn-dt-home i.btn-home, #slot-btn-dt-home {
    display: none !important;
}

/* THE 45% LOADER BUG FIX:
   Instead of touching visibility or opacity on the container, 
   we only hide the *contents* of the loader and make the background transparent. 
   This safely bypasses ExtJS loader size/visibility checks!
*/
#loading-mask {
    background: transparent !important;
    pointer-events: none !important;
    z-index: 1 !important;
}
#loading-mask .loadmask, #loading-mask .preloader, #box-loadmask {
    display: none !important;
}

/* 2. Reclaim vertical space without stretching canvas (Fixing squiggly lines) */
#toolbar, .toolbar, #viewport { margin-top: -28px !important; }

/* 3. Make #app-title an overlay */
#app-title, .box-header, .main-header {
    height: 0px !important; min-height: 0px !important;
    border: none !important; background: transparent !important;
    position: absolute !important; top: 0px !important; z-index: 100 !important;
    left: 0 !important; right: 0 !important; display: block !important;
    pointer-events: none !important;
}

#box-document-title {
    position: absolute !important;
    top: 6px !important; 
    left: 450px !important;
    right: 150px !important; 
    display: flex !important;
    align-items: center !important;
    height: 38px !important;
    pointer-events: none !important;
}

#box-document-title .hedset {
    display: flex !important;
    align-items: center !important;
    pointer-events: auto !important;
    flex-shrink: 0 !important;
}

#id-box-doc-name {
    flex-grow: 1 !important;
    text-align: center !important;
    margin-right: 450px !important;
    color: var(--text-normal) !important;
    font-size: 13px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

#box-header-tools, .box-header-tools, .box-header .extra {
    position: absolute !important;
    top: 6px !important;
    right: 15px !important;
    display: flex !important;
    z-index: 101 !important;
    pointer-events: auto !important;
}

#slot-btn-search, .btn-search { order: -2 !important; }
#slot-btn-user, .btn-user { order: -1 !important; }
</style>"""

script = """<script id="nuclear_ui_v11">
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        var tabs = document.querySelectorAll("li.ribtab, a.ribtab");
        for (var i = 0; i < tabs.length; i++) {
            var txt = (tabs[i].textContent || "").toLowerCase();
            if (txt.includes("collaboration") || 
                txt.includes("plugin") || 
                txt.includes("protection") || 
                txt.startsWith("ai ") || 
                txt.includes("cloud") ) {
                tabs[i].style.position = "absolute";
                tabs[i].style.left = "-9999px";
                tabs[i].style.opacity = "0";
                tabs[i].style.pointerEvents = "none";
            }
        }
    }, 1500);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("V11 Editor UI Deployed - Testing loader and squiggle fixes")
