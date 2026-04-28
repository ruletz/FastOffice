import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<style id="nuclear-hub-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-hub-js.*?">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="dom_dumper_hub">.*?</script>', '', text, flags=re.DOTALL)

# Extremely safe Hub hiding script
style = """<style id="nuclear-hub-style-v4">
/* Hide clouds by targeting exact data-types used by ExtJS menu items */
li.menu-item[data-type="clouds"],
li.menu-item[data-type="cloud"],
a[tooltip*="Cloud" i], 
a.btn-clouds,
.cloud-icon,
svg.cloud-icon,
#idx-btn-clouds {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    pointer-events: none !important;
}

/* Hide all Logos */
.logo-text, .title-text, .app-name, #idx-about-appname, span[class*='logo-text'] { 
    display: none !important; 
    width: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
}
</style>"""

script = """<script id="nuclear-hub-js-v4">
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        var items = document.querySelectorAll("li.menu-item, div.menu-item");
        for(var i=0; i<items.length; i++) {
            var txt = (items[i].innerText || items[i].textContent || "").toLowerCase().trim();
            // Just apply CSS classes safely, never use .remove()
            if (txt === "clouds" || txt === "connect to cloud") {
                items[i].style.display = "none";
                items[i].style.pointerEvents = "none";
                items[i].style.height = "0px";
                items[i].style.overflow = "hidden";
            }
        }
    }, 1000);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Reverted to Safe Hub V4")
