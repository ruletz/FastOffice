import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Clean previous scripts and dumps
text = re.sub(r'<style id="nuclear-style">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<style id="nuclear-style-v2">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui_v2">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="dom_dumper_local">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-style-v2">
/* HIDE LOADER MASK */
#loading-mask, .loadmask, .preloader, #box-loadmask { 
    display: none !important; opacity: 0 !important; visibility: hidden !important; z-index: -9999 !important; pointer-events: none !important;
}

/* HIDE TOP BAR entirely */
#app-title, .box-header, .main-header, #box-header, .header, #header, .top-panel {
    display: none !important;
    height: 0px !important;
    min-height: 0px !important;
    overflow: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* RECOVER SPACE left by app-title */
#toolbar, .toolbar, #viewport {
    top: 0px !important;
}
.main-panel, #mainpnl, .app-body {
    top: 112px !important; 
}

/* HIDE Editing, Collaboration, Plugins, Protection, AI from UI */
li[data-layout-name="toolbar-collaboration"],
li[data-layout-name="toolbar-plugins"],
li[data-layout-name="toolbar-protect"],
div[data-layout-name="header-editMode"],
#slot-btn-edit-mode,
li[data-tab="review"],
li[data-tab="plugins"],
li[data-tab="protect"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* TABS ROW AS FLEX */
.tabs ul[role="tablist"] {
    display: flex !important;
    align-items: center !important;
}

/* TOOLS & TITLE ALIGNMENT */
.custom-injected-tools {
    display: flex !important;
    align-items: center !important;
    padding: 0 15px !important;
    margin: 0 !important;
}
.custom-injected-tools .btn-slot {
    display: inline-block;
    vertical-align: middle;
}

/* ALL LOGOS */
.logo-text, .title-text, .app-name, #idx-about-appname, #idx-about-version, .box-copyright, span[class*='logo-text'] {
    display: none !important;
}
.btn-home .caption { display: none !important; }
</style>"""

script = """<script id="nuclear_ui_v2">
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        
        // 1. Hide unwanted tabs by inner text
        var tabs = document.querySelectorAll("li.ribtab, a.ribtab");
        for (var i = 0; i < tabs.length; i++) {
            var txt = (tabs[i].innerText || "").toLowerCase();
            if (txt.includes("collaboration") || txt.includes("plugin") || txt.includes("protection") || txt.startsWith("ai")) {
                tabs[i].style.display = "none";
                tabs[i].style.width = "0px";
            }
        }
        
        // 2. Move Save, Undo, Redo, and Title to the secondary toolbar if not done
        var toolbarTabs = document.querySelector(".tabs ul[role='tablist']");
        var saveBtnSlot = document.getElementById("slot-btn-dt-save");
        var undoBtnSlot = document.getElementById("slot-btn-dt-undo");
        var redoBtnSlot = document.getElementById("slot-btn-dt-redo");
        var titleSlot = document.getElementById("id-box-doc-name");
        var homeBtnSlot = document.getElementById("slot-btn-dt-home");

        if (toolbarTabs && !document.getElementById("custom-injected-tools-container")) {
            var container = document.createElement("li");
            container.id = "custom-injected-tools-container";
            container.className = "custom-injected-tools";
            
            if(homeBtnSlot) container.appendChild(homeBtnSlot);
            if(saveBtnSlot) container.appendChild(saveBtnSlot);
            if(undoBtnSlot) container.appendChild(undoBtnSlot);
            if(redoBtnSlot) container.appendChild(redoBtnSlot);
            if(titleSlot) container.appendChild(titleSlot);

            // Find literally the 'View' tab
            var insertAfterNode = null;
            for (var t = 0; t < tabs.length; t++) {
                if ((tabs[t].innerText || "").toLowerCase().trim() === "view") {
                    insertAfterNode = tabs[t].closest('li') || tabs[t];
                    break;
                }
            }

            if (insertAfterNode && insertAfterNode.parentNode === toolbarTabs && insertAfterNode.nextSibling) {
                toolbarTabs.insertBefore(container, insertAfterNode.nextSibling);
            } else {
                toolbarTabs.appendChild(container);
            }
        }
        
        // 3. Make sure top header stays dead and hidden
        var topHeader = document.getElementById("app-title") || document.querySelector(".box-header");
        if (topHeader) {
            topHeader.style.display = "none";
            topHeader.style.height = "0px";
            topHeader.style.opacity = "0";
        }
        
    }, 500);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Nuclear script v2 deployed to Document Editor main/index.html.")
