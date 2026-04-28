import base64
import os
import re

wasm_file = 'c:/Projects/OnlyOffice/fast_ooxml_rust/pkg/fast_ooxml_rust_bg.wasm'
js_glue = 'c:/Projects/OnlyOffice/fast_ooxml_rust/pkg/fast_ooxml_rust.js'

with open(wasm_file, 'rb') as f:
    wasm_b64 = base64.b64encode(f.read()).decode('utf-8')

with open(js_glue, 'r', encoding='utf-8') as f:
    js_content = f.read()

# We need to replace the ES module export system for browser injection since we are injecting plain JS tags
# the wasm-bindgen glue does `export default function init...`
# We patch it for pure global execution
js_content = js_content.replace('export default function __wbg_init', 'async function __wbg_init')
js_content = js_content.replace('export function add', 'function add')
js_content = js_content.replace('export function process_string', 'function process_string')
js_content = re.sub(r'^export .*', '', js_content, flags=re.MULTILINE)

js_inject = f"""
<script id="fast_rust_engine">
{js_content}

const target_ooxml_wasm = '{wasm_b64}';
const wasmArrayBuffer = Uint8Array.from(atob(target_ooxml_wasm), c => c.charCodeAt(0)).buffer;

async function BootRust() {{
    const module = await WebAssembly.compile(wasmArrayBuffer);
    await __wbg_init(module);
    window.RustEngine = {{
        add: function(a, b) {{ return add(a, b); }},
        process_text: function(txt) {{ return process_string(txt); }},
        is_ready: true
    }};
    console.log('[RUST] Engine Booted with wasm-pack glue! Test: 5+7=', window.RustEngine.add(5, 7));
}}

BootRust();
</script>
"""

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Strip any old engine
html = re.sub(r'<script id="fast_rust_engine">.*?</script>', '', html, flags=re.DOTALL)

if '</body>' in html:
    html = html.replace('</body>', js_inject + '\\n</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Rust Engine V1 injected into index.html!')
