import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Clear out our old attempted fetch injection
text = re.sub(r'<script>\s*setTimeout.*?Sending DOM.*?</script>', '', text, flags=re.DOTALL)

# Inject an extremely visible physical text dump onto the screen momentarily 
# so we can guarantee it runs without CSP blocking fetch calls.
# Or better yet, we trigger an automatic file download which modern CEF usually allows!

script = """<script id="dom_dumper_local">
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var str = document.documentElement.outerHTML;
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style.display = "none";
        var blob = new Blob([str], {type: "text/plain"});
        var url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = "onlyoffice_dom_dump.txt";
        a.click();
        window.URL.revokeObjectURL(url);
    }, 7000); // Wait 7 seconds for the whole ExtJS UI to fully compile
});
</script>"""

if 'dom_dumper_local' not in text:
    text = text.replace('</body>', script + '\n</body>')
    with codecs.open(html_path, 'w', 'utf8') as f:
        f.write(text)
    print("Auto-download script cleanly injected.")
