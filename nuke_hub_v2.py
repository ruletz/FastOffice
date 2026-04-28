import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Make sure we clean up the previous scripts so they don't fight
text = re.sub(r'<style id="nuclear-hub-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-hub-js.*?">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-hub-style-v2">
/* Hide the text in the startup window header */
.logo { display: none !important; visibility: hidden !important; }
.logo-text, .title-text, .app-name, #idx-about-appname, #idx-about-version, .box-copyright, span[class*='logo-text'] { display: none !important; }
.box-ver .ver-logo { width: 32px !important; overflow: hidden !important; }

/* Brutally force hide the Clouds */
#idx-btn-clouds { display: none !important; visibility: hidden !important; }
a[tooltip*="cloud" i], a[tooltip*="Cloud" i] { display: none !important; pointer-events: none !important; position: absolute; left:-9999px; }
li[id*="cloud" i], button[id*="cloud" i] { display: none !important; }
</style>"""

script = """<script id="nuclear-hub-js-v2">
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        var clouds = document.getElementById("idx-btn-clouds");
        if (clouds) {
            clouds.style.display = "none";
            clouds.remove();
        }
        
        // Attack the labels since ONLYOFFICE dynamically generates elements
        var labels = document.querySelectorAll("label, span, a, button, div, li");
        for(var i=0; i<labels.length; i++) {
            var txt = (labels[i].innerText || labels[i].textContent || "").toLowerCase();
            if(txt === "onlyoffice" || txt === "onlyoffice docs" || txt === "desktop editors") {
                labels[i].style.display = "none";
            }
            if(txt.includes("cloud") || txt.includes("clouds") || txt.includes("connect to cloud") || txt.includes("desktop editors")) {
                labels[i].style.display = "none";
                if (labels[i].parentNode) {
                    labels[i].parentNode.style.display = "none";
                }
            }
        }
    }, 100); // Fast interval
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Hub Nuke V2 Deployed on index.html")
