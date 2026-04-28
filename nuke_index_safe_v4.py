import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Clean previous scripts
text = re.sub(r'<style id="nuclear-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui.*?">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="dom_dumper_local">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-style-v4">
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
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* The mode switchers and Cloud buttons */
button[id*='mode'], button[id*='cloud'] {
    display: none !important;
}

/* Hide home btn logo icon */
#slot-btn-dt-home i.btn-home {
    display: none !important;
}
#slot-btn-dt-home { display: none !important; }

/* 2. Reclaim vertical space */
#toolbar, .toolbar, #viewport {
    top: 0px !important; 
}
.main-panel, #mainpnl, .app-body {
    top: 84px !important; 
}

/* 3. Make #app-title an overlay on top of the tabs! */
#app-title, .box-header, .main-header {
    display: flex !important;
    width: 100vw !important;
    height: 0px !important;
    min-height: 0px !important;
    border: none !important;
    background: transparent !important;
    position: absolute !important;
    top: 0px !important;
    left: 0 !important;
    overflow: visible !important;
    pointer-events: none !important;
    z-index: 9999 !important;
}

/* 4. Left side: Quick Access + Document Title */
#box-document-title {
    display: flex !important;
    align-items: center !important;
    flex-grow: 1 !important;
    pointer-events: none !important;
    position: static !important;
    height: 38px !important; /* height of tabs text */
}

/* Make sure buttons inside are clickable */
#box-document-title .hedset,
#id-box-doc-name,
#box-header-tools .btn-slot {
    pointer-events: auto !important;
}

/* Push Quick Access (Save, Print, ...) to the right of the "View" tab */
.hedset {
    display: flex !important;
    align-items: center !important;
    margin-left: 450px !important; /* Generous space for localized tabs */
}

/* Title text: perfectly centered using flex-grow and counter-margin */
#id-box-doc-name {
    flex-grow: 1 !important;
    text-align: center !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding-right: 450px !important; /* Offset the left margin to center perfectly */
    color: var(--text-normal) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* 5. Right tools */
#box-header-tools, .box-header-tools, .box-header .extra {
    display: flex !important;
    align-items: center !important;
    height: 38px !important;
    margin-right: 15px !important;
    pointer-events: auto !important;
}

/* Swap User and Search icons */
/* Force the container to actually display as flex to honor order */
#box-header-tools {
    display: flex !important;
}
#slot-btn-search, .btn-search {
    order: -2 !important;
}
#slot-btn-user, .btn-user {
    order: -1 !important;
}
</style>"""

script = """<script id="nuclear_ui_v4">
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
                tabs[i].style.display = "none";
                tabs[i].style.visibility = "hidden";
            }
        }
    }, 1000);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Nuclear Safe Script V4 deployed")
