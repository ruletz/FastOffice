import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# I am removing any past debug/fetch scripts to be clean
text = re.sub(r'<script id="dom_dumper_local">.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<script>\s*setTimeout.*?Sending DOM.*?</script>', '', text, flags=re.DOTALL)

script = """<script id="dom_dumper_local">
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var str = document.documentElement.outerHTML;
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
        ta.style.boxShadow = "0 0 20px rgba(0,0,0,0.5)";
        ta.style.fontFamily = "monospace";
        ta.style.fontSize = "12px";
        ta.value = "===== COPY EVERYTHING BELOW THIS LINE =====\\n\\n" + str;
        ta.id = "DOM_DUMP_TEXTAREA";
        
        // Add a close button
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

print("Visible textarea dumper cleanly injected.")
