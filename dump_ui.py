import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index_loader.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Let's write a script that dumps out the EXACT HTML of the rendered tab bar right now 
# and saves it locally so we can read it directly!

script = """
<script id="debug_dumper">
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var tabsContainer = document.querySelector(".toolbar-tabs-container ul") || document.querySelector(".toolbar-tabs");
        var rightMenu = document.querySelector(".right-menu") || document.querySelector(".top-panel-right");
        var topBar = document.querySelector(".box-header") || document.querySelector(".main-header");
        
        var dump = "";
        if (topBar) {
            dump += "=== TOP BAR ===\\n" + topBar.innerHTML + "\\n\\n";
        }
        if (tabsContainer) {
            dump += "=== TABS ===\\n" + tabsUl.innerHTML + "\\n\\n";
        }
        if (rightMenu) {
            dump += "=== RIGHT MENU ===\\n" + rightMenu.innerHTML + "\\n\\n";
        }
        
        // Make a download to save locally
        if (dump !== "") {
            var blob = new Blob([dump], {type: "text/plain"});
            var a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "ui_dump.txt";
            a.click();
        }
    }, 12000); 
});
</script>
"""

# inject to html
text = text.replace('</body>', script + '\n</body>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Dumper script injected.")
