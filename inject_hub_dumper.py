import codecs

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

script = """<script id="dom_dumper_hub">
setTimeout(function(){
    fetch('http://127.0.0.1:8888', {
        method: 'POST',
        body: document.documentElement.outerHTML
    }).then(() => {
        alert("Hub DOM dumped to server!");
    }).catch(e => {
        alert("Dump failed: " + e);
    });
}, 5000);
</script>"""

if 'dom_dumper_hub' not in text:
    text = text.replace('</body>', script + '\n</body>')
    with codecs.open(html_path, 'w', 'utf8') as f:
        f.write(text)
    print("Dumper injected into Hub!")
else:
    print("Dumper already injected into Hub!")
