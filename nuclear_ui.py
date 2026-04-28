import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index_loader.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Clear out any past scripts we injected for DOM restructuring
text = re.sub(r'<script.*?(OnlyOffice Native UI|Debug|debug_dumper).*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<style>\s*/\*\s*1\.\s*HIDE.*?</style>', '', text, flags=re.DOTALL)

script = """
<style id="custom-layout">
/* Completely nuke the visual footprint of the first/top toolbar */
.box-header, .main-header, #box-header, .header, #header {
    height: 0px !important;
    min-height: 0px !important;
    overflow: hidden !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
    display: none !important;
}

/* Recover space */
.main-panel, #mainpnl, .app-body {
    top: 40px !important;
}

/* Tab bar flex utilities for horizontal stacking */
.toolbar-tabs-container ul {
    display: flex !important;
    align-items: center !important;
}

/* Restyle original left icons (save/undo) and title so they fit inside the tab row */
.custom-header-tools {
    display: flex !important;
    align-items: center !important;
    padding: 0 15px !important;
    margin-top: 0px !important;
}
.custom-header-title {
    display: flex !important;
    align-items: center !important;
    padding: 0 15px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    max-width: 200px !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    text-overflow: ellipsis !important;
    margin-top: 0px !important;
}

/* Kill all visual logo textual elements */
.logo-text, .title-text, .app-name, #idx-about-appname, #idx-about-version, .box-copyright, span[class*='logo-text'] {
    display: none !important;
}
.box-ver .ver-logo {
    width: 32px !important;
    overflow: hidden !important;
}
</style>

<script id="nuclear_ui">
document.addEventListener("DOMContentLoaded", function() {
    console.log("Nuclear DOM UI restructuring sequence active.");
    var toolsMoved = false;

    // Run every 200ms indefinitely to defeat Backbone.js rerenders
    setInterval(function() {
        
        // -------------------------------------------------------------
        // 1. TEXT-BASED ELEMENT ASSASSINATION (Guaranteed to work regardless of class IDs)
        // -------------------------------------------------------------
        
        // Kill unwanted tabs by Inner Text (Collaboration, Plugins, Protection, AI)
        var allTabs = document.querySelectorAll("li, .tab, .x-tab");
        for (var i = 0; i < allTabs.length; i++) {
            var txt = (allTabs[i].innerText || allTabs[i].textContent || "").toLowerCase();
            if (txt.indexOf("collaboration") !== -1 || 
                txt.indexOf("plugin") !== -1 || 
                txt.indexOf("protection") !== -1 ||
                txt.indexOf("ai") === 0) {
                allTabs[i].style.display = "none";
            }
        }
        
        // Kill Cloud/Editing switchers on the right by InnerText and structural placement
        var buttons = document.querySelectorAll("button, .btn, .x-btn, .menu-item");
        for (var b = 0; b < buttons.length; b++) {
            var bTxt = (buttons[b].innerText || buttons[b].textContent || "").toLowerCase();
            if (bTxt.indexOf("editing") !== -1 || 
                bTxt.indexOf("reviewing") !== -1 || 
                bTxt.indexOf("viewing") !== -1 ||
                bTxt.indexOf("cloud") !== -1 || 
                buttons[b].id.indexOf("cloud") !== -1 ||
                buttons[b].id.indexOf("mode") !== -1) {
                buttons[b].style.display = "none";
            }
        }

        // -------------------------------------------------------------
        // 2. MIGRATE ICONS & TITLE INTO TABS BAR
        // -------------------------------------------------------------
        var tabsUl = document.querySelector(".toolbar-tabs-container ul") || document.querySelector(".toolbar-tabs");
        var tools = document.querySelector(".header-tools") || document.querySelector(".header-left");
        var titleBox = document.querySelector(".header-title") || document.querySelector("#document-title");

        if (tabsUl && tools && titleBox && !toolsMoved) {
            
            // Add spacing classes
            tools.classList.add("custom-header-tools");
            titleBox.classList.add("custom-header-title");
            
            // Un-hide if hidden by topbar css
            tools.style.display = "flex";
            titleBox.style.display = "flex";

            // Find literally the 'View' tab
            var viewNode = null;
            for (var t = 0; t < allTabs.length; t++) {
                var cText = (allTabs[t].innerText || allTabs[t].textContent || "").toLowerCase().trim();
                // ExtJS sometimes renders them inside nested Spans. Look for full strings.
                if (cText === "view") {
                    // Usually the Li is the wrapper or parent
                    viewNode = allTabs[t].closest('li'); 
                    if (!viewNode) viewNode = allTabs[t];
                    break;
                }
            }

            if (viewNode && viewNode.parentNode === tabsUl && viewNode.nextSibling) {
                // If the View tab exists, inject immediately after it
                tabsUl.insertBefore(tools, viewNode.nextSibling);
                tabsUl.insertBefore(titleBox, tools.nextSibling);
            } else {
                // Fallback: Stick them on the right edge of the tabs
                tabsUl.appendChild(tools);
                tabsUl.appendChild(titleBox);
            }
            toolsMoved = true;
        }

        // Just directly rip the entire top bar off the DOM so it cannot interfere
        var topBar = document.querySelector(".box-header") || document.querySelector(".main-header");
        if (topBar) {
            topBar.innerHTML = "";
            topBar.style.display = "none";
        }
        
    }, 200);
});
</script>
"""

# Now inject it back
if "nuclear_ui" not in text:
    text = text.replace("</head>", script + "\n</head>")
    with codecs.open(html_path, 'w', 'utf8') as f:
        f.write(text)
    print("Nuclear Text-scraping UI Rebuilder script injected.")
else:
    print("Already exists.")
