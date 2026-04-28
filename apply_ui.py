import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index_loader.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Strip any previous logic
text = re.sub(r'<style>/\* 1\. HIDE UNWANTED TABS.*?</script>', '', text, flags=re.DOTALL)

script_to_inject = """
<style>
/* 1. HIDE EVERYTHING REQUESTED BY USER */
li[data-id="collaboration"],
#toolbar-tab-collaboration,
li[data-id="protection"],
#toolbar-tab-protection,
li[data-id="plugins"],
#toolbar-tab-plugins,
li[data-id="chat"],
li[data-id*="ai"],
.btn-clouds, #idx-btn-clouds, #right-menu-clouds, button[id*='cloud'],
.mode-switcher, #right-menu-mode {
    display: none !important;
}

/* 2. COMPLETELY HIDE THE TOP BAR */
.main-header, .box-header, #box-header {
    display: none !important;
    height: 0px !important;
    min-height: 0px !important;
    overflow: hidden !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 3. RECOVER THE LOST SPACE IN THE UI */
.main-panel, #mainpnl {
    top: 40px !important;
}

/* 4. ALIGN THE TABS TO ENABLE OUR INJECTIONS */
.toolbar-tabs-container ul {
    display: flex !important;
    align-items: center !important;
}
/* Style our newly moved Save/Undo/Redo to look flush with Tabs */
.toolbar-tabs-container .header-tools {
    display: flex !important;
    align-items: center !important;
    padding-left: 15px;
    padding-right: 15px;
}
.toolbar-tabs-container .header-title {
    display: flex !important;
    align-items: center !important;
    padding-left: 15px;
    padding-right: 15px;
    font-weight: 500;
    max-width: 300px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}
</style>

<script>
document.addEventListener("DOMContentLoaded", function() {
    var checkUI = setInterval(function() {
        var topBar = document.querySelector(".box-header") || document.querySelector(".main-header");
        var tabsUl = document.querySelector(".toolbar-tabs-container ul") || document.querySelector(".toolbar-tabs");
        
        if (tabsUl && topBar) {
            clearInterval(checkUI); // We found the rendered UI!

            // The Save, Undo, Redo block
            var tools = topBar.querySelector(".header-tools") || document.querySelector(".header-left");
            // The document Title box
            var title = topBar.querySelector(".header-title") || topBar.querySelector("#document-title");

            // Find the "View" tab
            var viewTab = false;
            var allTabs = tabsUl.querySelectorAll("li");
            for (var i = 0; i < allTabs.length; i++) {
                if (allTabs[i].getAttribute("data-id") === "view" || (allTabs[i].id && allTabs[i].id.indexOf("view") > -1)) {
                    viewTab = allTabs[i];
                    break;
                }
            }

            // Insert tools -> title right after the View tab
            if (viewTab && viewTab.nextSibling) {
                // Insert Save/Undo right after 'View'
                tabsUl.insertBefore(tools, viewTab.nextSibling);
                // Insert Title right after Save/Undo
                tabsUl.insertBefore(title, tools.nextSibling);
            } else {
                // If 'View' not found, just append
                tabsUl.appendChild(tools);
                tabsUl.appendChild(title);
            }
            
            // Delete the rest of the top bar container natively
            topBar.remove();
        }
    }, 100);
    
    // Stop trying after 10 seconds just in case
    setTimeout(function() { clearInterval(checkUI); }, 10000);
});
</script>
"""

# Now inject it back just above </head>
text = text.replace("</head>", script_to_inject + "\n</head>")

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("UI Rebuilder applied elegantly.")
