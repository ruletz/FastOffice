import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Clean previous scripts
text = re.sub(r'<style id="nuclear-hub-style">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear-hub-js">.*?</script>', '', text, flags=re.DOTALL)

style = """<style id="nuclear-hub-style">
/* Hide Logo */
.logo { display: none !important; visibility: hidden !important; }
.logo-text, .title-text, .app-name, #idx-about-appname, #idx-about-version, .box-copyright, span[class*='logo-text'] { display: none !important; }
.box-ver .ver-logo { width: 32px !important; overflow: hidden !important; }

/* Hide Clouds */
#idx-btn-clouds { display: none !important; visibility: hidden !important; }
a[tooltip*="cloud" i], a[tooltip*="Cloud" i] { display: none !important; }
</style>"""

script = """<script id="nuclear-hub-js">
document.addEventListener("DOMContentLoaded", function() {
    setInterval(function() {
        var clouds = document.getElementById("idx-btn-clouds");
        if (clouds) clouds.style.display = "none";
        
        var labels = document.querySelectorAll("label");
        for(var i=0; i<labels.length; i++) {
            if(labels[i].innerText && labels[i].innerText.toLowerCase().indexOf("cloud") !== -1) {
                if(labels[i].parentElement) labels[i].parentElement.style.display = "none";
            }
        }
    }, 500);
});
</script>"""

if '</head>' in text:
    text = text.replace('</head>', style + '\n' + script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Nuclear script deployed to Hub index.html.")
