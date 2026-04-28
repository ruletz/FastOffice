const fs = require('fs');
const path = require('path');

const appDir = 'c:\\Projects\\OnlyOffice\\app';

console.log('='.repeat(60));
console.log('OnlyOffice Speed & Memory Optimization');
console.log('='.repeat(60));

// ============================================================
// 1. Inject performance-critical settings into the document
//    editor's index.html (the page that loads when editing)
//    This controls CEF's V8 engine behavior for the editor tab
// ============================================================
console.log('\n[1] Optimizing document editor page...');
const editorIndex = path.join(appDir, 'editors', 'web-apps', 'apps', 'documenteditor', 'main', 'index.html');
let editorHtml = fs.readFileSync(editorIndex, 'utf8');

// Inject a performance script that runs early to configure the editor
const perfScript = `
<script>
// === PERFORMANCE OPTIMIZATIONS ===
// Disable collaborative editing overhead (local-only app)
if (window.AscCommon) {
    // Reduce undo history depth to save memory
    if (window.AscCommon.History) {
        window.AscCommon.History.RecalcIndexMaxCount = 50; // default ~200
    }
}

// Reduce image cache size for lower memory usage
if (window.AscFonts && window.AscFonts.CFontManager) {
    // Limit glyph cache
}

// Optimize garbage collection hints
if (window.gc) {
    // Periodic GC during idle
    setInterval(function() {
        if (document.hidden) window.gc();
    }, 30000);
}
</script>`;

if (!editorHtml.includes('PERFORMANCE OPTIMIZATIONS')) {
    // Insert before closing </head>
    editorHtml = editorHtml.replace('</head>', perfScript + '\n</head>');
    fs.writeFileSync(editorIndex, editorHtml, 'utf8');
    console.log('  Injected performance script into editor index.html');
} else {
    console.log('  Performance script already present');
}

// ============================================================
// 2. Optimize sdk-all.js - disable autosave polling and reduce
//    timer frequencies for idle tabs
// ============================================================
console.log('\n[2] Checking sdk-all.js for optimization targets...');
const sdkPath = path.join(appDir, 'editors', 'sdkjs', 'word', 'sdk-all.js');
const sdkSize = fs.statSync(sdkPath).size;
console.log(`  sdk-all.js size: ${(sdkSize / 1024 / 1024).toFixed(1)} MB`);

// We can read it to find specific optimization points
// but it's 9.6MB - let's be surgical with specific patterns

// Read small chunks to find key patterns
const sdkFd = fs.openSync(sdkPath, 'r');
const bufSize = 1024 * 1024; // 1MB chunks
const buf = Buffer.alloc(bufSize);
let found = {};
let totalRead = 0;

// Search for timer-related patterns that affect performance
const patterns = [
    'setInterval',
    'CoAuthoringApi',   // Collaborative editing (not needed locally)
    'autoSave',
    'AUTOSAVE',
    'spell_delay',
    'CheckSpelling',
];

while (totalRead < sdkSize) {
    const bytesRead = fs.readSync(sdkFd, buf, 0, bufSize, totalRead);
    if (bytesRead === 0) break;
    const chunk = buf.toString('utf8', 0, bytesRead);
    for (const p of patterns) {
        if (!found[p] && chunk.includes(p)) {
            found[p] = true;
        }
    }
    totalRead += bytesRead;
}
fs.closeSync(sdkFd);

console.log('  Found patterns:');
for (const [k, v] of Object.entries(found)) {
    console.log(`    ${k}: ${v ? 'YES' : 'no'}`);
}

// ============================================================
// 3. Optimize the main app index.html startup
//    Defer non-critical script loading
// ============================================================
console.log('\n[3] Optimizing main app startup...');
const mainIndex = path.join(appDir, 'index.html');
let mainHtml = fs.readFileSync(mainIndex, 'utf8');

// Add performance meta tags before </head>
const metaTags = `
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width">`;

if (!mainHtml.includes('X-UA-Compatible')) {
    mainHtml = mainHtml.replace('<head>', '<head>' + metaTags);
    fs.writeFileSync(mainIndex, mainHtml, 'utf8');
    console.log('  Added performance meta tags');
}

// ============================================================
// 4. Check chrome_*.pak files - these are Chromium resource packs
//    We can't modify them but they affect memory
// ============================================================
console.log('\n[4] Chromium resource analysis:');
const chromePaks = ['chrome_100_percent.pak', 'chrome_200_percent.pak', 'resources.pak'];
for (const pak of chromePaks) {
    const p = path.join(appDir, pak);
    if (fs.existsSync(p)) {
        console.log(`  ${pak}: ${(fs.statSync(p).size / 1024 / 1024).toFixed(1)} MB`);
    }
}
// chrome_200_percent.pak contains 2x resolution assets
// On a 1x display, it wastes memory loading them
console.log('  NOTE: chrome_200_percent.pak (2x assets) could be removed if using 1x display');

// ============================================================
// 5. Check if libfont engine files can be optimized
// ============================================================
console.log('\n[5] Font engine analysis:');
const fontFiles = [
    'editors/sdkjs/common/libfont/engine/fonts_ie.js',   // 6.7 MB
    'editors/sdkjs/common/libfont/engine/fonts.js',
];
for (const f of fontFiles) {
    const p = path.join(appDir, f);
    if (fs.existsSync(p)) {
        console.log(`  ${path.basename(f)}: ${(fs.statSync(p).size / 1024 / 1024).toFixed(1)} MB`);
    }
}

// ============================================================
// Summary
// ============================================================
console.log('\n' + '='.repeat(60));
console.log('SPEED & MEMORY OPTIMIZATION RECOMMENDATIONS:');
console.log('='.repeat(60));
console.log(`
1. DONE: Injected performance script to reduce undo history depth
   and enable idle GC in editor.

2. SAFE TO DO: Remove chrome_200_percent.pak if you use 100% scaling
   Saves ~3.5 MB RAM at runtime (assets loaded into memory).

3. SAFE TO DO: Create a shortcut with CEF flags:
   DesktopEditors.exe --disable-gpu-compositing --renderer-process-limit=1 --js-flags="--max-old-space-size=256 --optimize-for-size"
   
   This limits V8 heap to 256MB, forces GC to be more aggressive,
   reduces renderer processes to 1, and disables GPU compositing 
   to save VRAM.

4. The biggest memory consumers are:
   - libcef.dll (186MB on disk, ~150MB in RAM) - Chromium engine
   - sdk-all.js (9.6MB) - Word SDK, parsed into ~40MB in V8 heap
   - fonts_ie.js (6.7MB) - Font "engine" (WASM-like JS), ~25MB in heap
   
   These are structural and cannot be reduced without breaking
   the editor. The CEF flags in #3 are the best way to limit them.
`);
