import codecs

sdk_path = 'c:/Projects/OnlyOffice/app/editors/sdkjs/word/sdk-all.js'
with codecs.open(sdk_path, 'r', 'utf8') as f:
    text = f.read()

# Append a prototype override at the very end of the file
# This will override whatever DrawSpellingLine was defined earlier (even if obfuscated)
# because CGraphics inherits from CGraphicsBase, and the real class is CGraphics

override = """

;(function(){
    // Override DrawSpellingLine to draw wavy/squiggly lines
    // Find CGraphics prototype by looking for drawHorLine on the prototype chain
    var _origDrawSpellingLine;
    
    // We need to find the CGraphics constructor. It's the one that has m_oContext.
    // The easiest way: override on the prototype of any object that has DrawSpellingLine
    // We'll monkey-patch it at the AscCommon level
    
    function drawWavyLine(ctx, x0, y0, x1) {
        var dx = x1 - x0;
        if (dx <= 0) return;
        
        var wavelength = 3.5;
        var amplitude = 1.0;
        var waves = Math.round(dx / wavelength);
        if (waves <= 0) return;
        
        var wl = dx / waves;
        ctx.moveTo(x0, y0);
        for (var i = 0; i < waves; i++) {
            var cp1x = x0 + (i * wl + wl / 4);
            var cp1y = y0 + amplitude;
            var cp2x = x0 + (i * wl + wl * 3 / 4);
            var cp2y = y0 - amplitude;
            var ep_x = x0 + (i * wl + wl);
            var ep_y = y0;
            ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, ep_x, ep_y);
        }
    }
    
    // Override at window load time to find the actual prototype
    var _origSetTimeout = window.setTimeout;
    var _patched = false;
    
    // Use a MutationObserver to detect when the editor canvas appears, then patch
    function tryPatch() {
        if (_patched) return;
        
        // Look for any object whose prototype has DrawSpellingLine defined
        // In the compiled code, CGraphics extends CGraphicsBase
        // CGraphicsBase is in AscCommon namespace
        if (typeof AscCommon !== 'undefined') {
            // Find all prototypes that have DrawSpellingLine
            var keys = Object.keys(AscCommon);
            for (var i = 0; i < keys.length; i++) {
                var obj = AscCommon[keys[i]];
                if (obj && obj.prototype && obj.prototype.DrawSpellingLine) {
                    var origFn = obj.prototype.DrawSpellingLine;
                    obj.prototype.DrawSpellingLine = function(y0, x0, x1, w) {
                        if (this.m_oContext && !Asc.editor.isViewMode) {
                            var ctx = this.m_oContext;
                            var _m = this.m_oFullTransform;
                            if (!_m) {
                                // fallback
                                origFn.call(this, y0, x0, x1, w);
                                return;
                            }
                            var px0 = (_m.TransformPointX(x0, y0) >> 0) + 0.5;
                            var px1 = (_m.TransformPointX(x1, y0) >> 0) + 0.5;
                            var py = (_m.TransformPointY(x0, y0) >> 0) + 0.5 + 1.0;
                            
                            var dxPx = px1 - px0;
                            if (dxPx <= 0) return;
                            
                            var bIsInt = this.m_bIntegerGrid;
                            if (!bIsInt) this.SetIntegerGrid(true);
                            
                            ctx.setTransform(1,0,0,1,0,0);
                            ctx.lineWidth = 1;
                            ctx.beginPath();
                            drawWavyLine(ctx, px0, py, px1);
                            ctx.stroke();
                            ctx.beginPath();
                            
                            if (!bIsInt) this.SetIntegerGrid(false);
                        } else {
                            origFn.call(this, y0, x0, x1, w);
                        }
                    };
                    _patched = true;
                    console.log('[Squiggly] Patched DrawSpellingLine on', keys[i]);
                }
            }
        }
        
        if (!_patched) {
            _origSetTimeout(tryPatch, 500);
        }
    }
    
    // Start trying to patch after a delay
    _origSetTimeout(tryPatch, 100);
})();
"""

if 'drawWavyLine' not in text:
    text += override
    with codecs.open(sdk_path, 'w', 'utf8') as f:
        f.write(text)
    print("Squiggly override appended to sdk-all.js")
else:
    print("Already patched")

# Also patch sdk-all-min.js  
min_path = 'c:/Projects/OnlyOffice/app/editors/sdkjs/word/sdk-all-min.js'
with codecs.open(min_path, 'r', 'utf8') as f:
    min_text = f.read()

if 'drawWavyLine' not in min_text:
    min_text += override
    with codecs.open(min_path, 'w', 'utf8') as f:
        f.write(min_text)
    print("Squiggly override appended to sdk-all-min.js")
else:
    print("Min already patched")
