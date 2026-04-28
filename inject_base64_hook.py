import base64
import os
import re

wasm_file = 'c:/Projects/OnlyOffice/fast_ooxml_rust/pkg/fast_ooxml_rust_bg.wasm'
js_glue = 'c:/Projects/OnlyOffice/fast_ooxml_rust/pkg/fast_ooxml_rust.js'

with open(wasm_file, 'rb') as f:
    wasm_b64 = base64.b64encode(f.read()).decode('utf-8')

with open(js_glue, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Make wasm module init work globally
js_content = js_content.replace('export default function __wbg_init', 'async function __wbg_init')
js_content = js_content.replace('export function add', 'function add')
js_content = js_content.replace('export function process_string', 'function process_string')
js_content = js_content.replace('export function decode_base64_fast', 'function decode_base64_fast')
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
        decode_base64: function(str) {{
            // Returns a Uint8Array natively mapped from memory
            return decode_base64_fast(str); 
        }},
        is_ready: true
    }};
    console.log('[RUST] WASM Engine loaded. Hooking into AscCommon Base64...');
    
    // Safety check wait for AscCommon
    let waitInt = setInterval(function() {{
        if (window.AscCommon && window.AscCommon.Base64) {{
            clearInterval(waitInt);
            const _oldDecode = window.AscCommon.Base64.decode;
            
            // Overwrite JavaScript's incredibly slow Base64 decoder loop with Rust WASM
            window.AscCommon.Base64.decode = function(str, b, c) {{
                if (typeof str === 'string') {{
                    try {{
                        let raw = window.RustEngine.decode_base64(str);
                        if (raw.length > 0) return raw;
                    }} catch(e) {{
                        console.error("Rust Base64 Failed fallback JS", e);
                    }}
                }}
                return _oldDecode.apply(this, arguments);
            }};
            console.log('[RUST] Base64 Decoder Hooked and active!');
        }}
    }}, 50);
}}

BootRust();
</script>
"""

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<script id="fast_rust_engine">.*?</script>', '', html, flags=re.DOTALL)

if '</body>' in html:
    html = html.replace('</body>', js_inject + '\\n</body>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Rust Engine V2 (Base64 OOXML Decoder Hook) injected into index.html!')
