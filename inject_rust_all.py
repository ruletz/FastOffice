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
js_content = js_content.replace('export function decode_base64_fast', 'function decode_base64_fast')
js_content = js_content.replace('export function parse_ooxml_tags_fast', 'function parse_ooxml_tags_fast')
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
        decode_base64: function(str) {{ return decode_base64_fast(str); }},
        parse_ooxml_tags: function(str) {{ return parse_ooxml_tags_fast(str); }},
        is_ready: true
    }};
    console.log('[RUST] WASM Engine loaded on ALL EDITORS. Hooking into AscCommon Base64 and XML OOXML parsing...');
    
    // 1. Hook Base64
    let waitInt = setInterval(function() {{
        if (window.AscCommon && window.AscCommon.Base64 && !window.AscCommon.Base64.__rust_hooked) {{
            clearInterval(waitInt);
            const _oldDecode = window.AscCommon.Base64.decode;
            window.AscCommon.Base64.decode = function(str, b, c) {{
                if (typeof str === 'string') {{
                    try {{
                        let raw = window.RustEngine.decode_base64(str);
                        if (raw.length > 0) return raw;
                    }} catch(e) {{}}
                }}
                return _oldDecode.apply(this, arguments);
            }};
            window.AscCommon.Base64.__rust_hooked = true;
            console.log('[RUST] Base64 Decoder Hooked and active!');
        }}
    }}, 50);

    // 2. Hook DOMParser.parseFromString to intercept and fast-format OOXML payload in Rust
    if (!DOMParser.prototype.__rust_hooked) {{
        const _oldParse = DOMParser.prototype.parseFromString;
        DOMParser.prototype.parseFromString = function(string, type) {{
            if (type === 'text/xml' || type === 'application/xml') {{
                try {{
                    // Pre-process and accelerate OOXML regex parsing in Rust before generating DOM
                    string = window.RustEngine.parse_ooxml_tags(string);
                }} catch(e) {{
                    console.error("[RUST] XML Hook failed", e);
                }}
            }}
            return _oldParse.call(this, string, type);
        }};
        DOMParser.prototype.__rust_hooked = true;
        console.log('[RUST] OOXML Regex string parser Hooked and active!');
    }}
}}

BootRust();
</script>
"""

targets = [
    'documenteditor/main/index.html',
    'spreadsheeteditor/main/index.html',
    'presentationeditor/main/index.html'
]

app_dir = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps'

for t in targets:
    html_path = os.path.join(app_dir, t)
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        html = re.sub(r'<script id=\"fast_rust_engine\">.*?</script>', '', html, flags=re.DOTALL)

        if '</body>' in html:
            html = html.replace('</body>', js_inject + '\\n</body>')

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Rust Engine V3 injected into {t}')
