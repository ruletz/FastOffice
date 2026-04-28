import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<style id="nuclear-style-v6">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui_v6">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<style id="nuclear-style-v7">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui_v7">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-style-v8">
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
    width: 0 !important;
    margin: 0 !important;
}

button[id*='mode'], button[id*='cloud'], #slot-btn-dt-home i.btn-home, #slot-btn-dt-home {
    display: none !important;
}

/* Fix loader flash! Visually hide it but DO NOT REMOVE the div using display:none, 
   that breaks ExtJS loading sequence. Just make it purely invisible. */
#loading-mask, .loadmask, .preloader, #box-loadmask {
    opacity: 0 !important;
    visibility: hidden !important;
    background: transparent !important;
    pointer-events: none !important;
}

/* 2. Reclaim vertical space */
#toolbar, .toolbar, #viewport { top: 0px !important; }
.main-panel, #mainpnl, .app-body { top: 84px !important; }

/* 3. Make #app-title an overlay on top of the tabs! */
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

script = """<script id="nuclear_ui_v8">
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
                tabs[i].style.visibility = "hidden";
            }
        }
    }, 1500);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("V8 UI deployed - Loading mask fixed")
