import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Revert back the destructive script completely
text = re.sub(r'<style id="nuclear-hub-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-hub-js.*?">.*?</script>', '', text, flags=re.DOTALL)

# Inject safe CSS ONLY for Clouds and Logo Text
style = """<style id="nuclear-hub-style-v3">
/* Hide specific Cloud elements visually without modifying DOM */
.btn-clouds, #idx-btn-clouds, [tooltip*="cloud" i], [tooltip*="Cloud" i] { 
    display: none !important; 
    visibility: hidden !important; 
    opacity: 0 !important; 
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide logo text in the hub */
.logo-text, .title-text, .app-name, #idx-about-appname, span[class*='logo-text'] { 
    display: none !important; 
    width: 0 !important;
    margin: 0 !important;
}
</style>"""

script = """<script id="nuclear-hub-js-v3">
// Purely to safely find any leftover text without crashing ExtJS
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        var targets = document.querySelectorAll("li, button, div.tab");
        for(var i=0; i<targets.length; i++) {
            var el = targets[i];
            var txt = (el.innerText || el.textContent || "").toLowerCase();
            // ExtJS dies if we touch its core labels too aggressively, so just apply CSS
            if (txt.includes("cloud") || txt.includes("clouds")) {
                el.style.display = "none";
                el.style.visibility = "hidden";
                el.style.opacity = "0";
            }
        }
    }, 1500); // Check slow enough to not bog down UI thread
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')
    
with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Reverted to Safe Hub V3")
