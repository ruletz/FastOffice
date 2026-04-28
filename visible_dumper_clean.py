import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Clear out our old attempted fetch injection
text = re.sub(r'<script id="dom_dumper_local">.*?</script>', '', text, flags=re.DOTALL)

script = """<script id="dom_dumper_local">
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var clone = document.documentElement.cloneNode(true);
        var junk = clone.querySelectorAll('svg, style, script, link, meta, symbol, path, g, defs');
        for(var i=0; i<junk.length; i++) {
            if (junk[i] && junk[i].parentNode) {
                junk[i].parentNode.removeChild(junk[i]);
            }
        }
        var str = clone.outerHTML;
        
        fetch('http://127.0.0.1:8888', {
            method: 'POST',
            body: str,
            headers: {'Content-Type': 'text/plain'}
        }).then(r => console.log('Sent to server', r.status)).catch(e => console.error(e));

        var ta = document.createElement("textarea");
        ta.style.position = "fixed";
        ta.style.top = "40px";
        ta.style.left = "40px";
        ta.style.width = "calc(100vw - 80px)";
        ta.style.height = "calc(100vh - 80px)";
        ta.style.zIndex = "9999999";
        ta.style.background = "#fff";
        ta.style.color = "#000";
        ta.style.padding = "20px";
        ta.style.fontFamily = "monospace";
        ta.style.fontSize = "12px";
        ta.value = "===== HTML SAVED TO SERVER =====\\n\\n" + str.substring(0, 1000) + "...";
        ta.id = "DOM_DUMP_TEXTAREA";
        
        var closeBtn = document.createElement("button");
        closeBtn.innerText = "Close Dump";
        closeBtn.style.position = "fixed";
        closeBtn.style.top = "50px";
        closeBtn.style.right = "60px";
        closeBtn.style.zIndex = "10000000";
        closeBtn.style.padding = "10px 20px";
        closeBtn.style.background = "red";
        closeBtn.style.color = "white";
        closeBtn.style.border = "none";
        closeBtn.style.cursor = "pointer";
        closeBtn.onclick = function() {
            ta.remove();
            closeBtn.remove();
        };
        
        document.body.appendChild(ta);
        document.body.appendChild(closeBtn);
    }, 8000); 
});
</script>"""

text = text.replace('</body>', script + '\n</body>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Visible textarea dumper cleanly injected with SVG stripping.")
