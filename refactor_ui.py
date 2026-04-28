import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index_loader.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Remove the old surgery script if we accidentally injected it earlier
text = re.sub(r'<script>\s*// UI SURGERY.*?</script>', '', text, flags=re.DOTALL)

script_to_inject = """
<style>
/* 1. HIDE UNWANTED TABS: Collaboration, Protection, Plugins, AI */
li[data-id="collaboration"],
li[data-id="protection"],
li[data-id="plugins"],
li[data-id*="chat"],
li[data-id*="ai"] {
    display: none !important;
}

/* 2. HIDE CLOUDS & EDITING/REVIEWING MODE */
.btn-clouds, #right-menu-clouds, button[id*='cloud'] {
    display: none !important;
}
.mode-switcher, #right-menu-mode {
    display: none !important;
}

/* 3. MERGE HEADER - WE'LL MOVE IN JS, BUT PREP CSS */
/* We don't want the original top bar wasting vertical space */
.box-header {
    height: 0px !important;
    min-height: 0px !important;
    overflow: hidden !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* Recalculate main panel spacing to recover the loss of top header */
.main-panel {
    top: 40px !important; /* Secondary toolbar is typically 40-42px tall */
}
</style>

<script>
// NATIVE UI REBUILD
document.addEventListener("DOMContentLoaded", function() {
    console.log("OnlyOffice Native UI Rebuilder Initialized");
    var observer = new MutationObserver(function(mutations, me) {
        // Wait for the heavy app.js ExtJS/Backbone engine to generate the DOM
        var titleBox = document.querySelector(".header-title"); // Where the document name is
        var headerLeft = document.querySelector(".header-left"); // Where save/undo is
        var tabsUl = document.querySelector(".toolbar-tabs");   // Where File/Home/View are
        var rightMenu = document.querySelector(".right-menu");  // Where Clouds/Mode used to be (right side of tabs)

        if (tabsUl && headerLeft && titleBox && rightMenu) {
            me.disconnect(); // UI Found, execute surgery

            // Move the Save/Undo buttons (headerLeft) into the Tabs bar
            // The user wants it "on the second [bar] after 'View'"
            
            // Re-style headerLeft so it flows in the tabs
            headerLeft.style.display = "flex";
            headerLeft.style.alignItems = "center";
            headerLeft.style.padding = "0 10px";
            
            // Re-style title horizontally
            titleBox.style.display = "flex";
            titleBox.style.alignItems = "center";
            titleBox.style.padding = "0 10px";
            titleBox.style.maxWidth = "250px";
            titleBox.style.overflow = "hidden";
            titleBox.style.whiteSpace = "nowrap";

            // Find the "View" tab to insert the new items after it
            var viewTab = tabsUl.querySelector('li[data-id="view"]');
            
            if (viewTab && viewTab.nextSibling) {
                // Insert Save/Undo block right after View tab
                tabsUl.insertBefore(headerLeft, viewTab.nextSibling);
                // Insert Title right after the Save/Undo block
                tabsUl.insertBefore(titleBox, headerLeft.nextSibling);
            } else {
                // Fallback: just append them to the end of the tabs list
                tabsUl.appendChild(headerLeft);
                tabsUl.appendChild(titleBox);
            }
            
            // To ensure the Title aligns perfectly left, we can just let it sit natively 
            // behind the tabs we inserted it at.
            console.log("OnlyOffice Native UI Refactor Complete.");
        }
    });
    
    // Watch body for UI injection
    observer.observe(document.body, { childList: true, subtree: true });
});
</script>
"""

# Now inject it back just above </head>
text = text.replace("</head>", script_to_inject + "\n</head>")

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("UI Rebuilder injected cleanly.")
