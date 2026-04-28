import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<script id="canvas_hijack">.*?</script>\s*', '', text, flags=re.DOTALL)

# This version logs to a visible div AND does the wave replacement
script = """<script id="canvas_hijack">
!function() {
    var RAW_beginPath = CanvasRenderingContext2D.prototype.beginPath;
    var RAW_moveTo = CanvasRenderingContext2D.prototype.moveTo;
    var RAW_lineTo = CanvasRenderingContext2D.prototype.lineTo;
    var RAW_stroke = CanvasRenderingContext2D.prototype.stroke;

    var logDiv;
    var logReady = false;
    var logQ = [];
    function addLog(msg) {
        if (!logReady) { logQ.push(msg); return; }
        if (logDiv.childNodes.length > 20) logDiv.removeChild(logDiv.firstChild);
        var d = document.createElement('div');
        d.textContent = msg;
        logDiv.appendChild(d);
    }
    document.addEventListener('DOMContentLoaded', function() {
        logDiv = document.createElement('div');
        logDiv.style.cssText = 'position:fixed;z-index:999999;top:100px;right:10px;background:rgba(0,0,0,0.85);color:#0f0;padding:8px;width:350px;height:400px;overflow:hidden;pointer-events:none;font:11px monospace';
        document.body.appendChild(logDiv);
        logReady = true;
        logQ.forEach(addLog);
        addLog('V5 LOADED OK');
    });

    CanvasRenderingContext2D.prototype.beginPath = function() {
        this._spPts = [];
        return RAW_beginPath.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.moveTo = function(x, y) {
        if (this._spPts) this._spPts.push(x, y);
        return RAW_moveTo.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.lineTo = function(x, y) {
        if (this._spPts) this._spPts.push(x, y);
        return RAW_lineTo.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.stroke = function() {
        var s = this.strokeStyle;
        var sl = s ? String(s).toLowerCase() : '';
        var isRed = (sl === '#ff0000' || sl === 'red');
        var pts = this._spPts;
        
        if (isRed && pts && pts.length > 0) {
            addLog('RED stroke pts=' + pts.length + ' style=' + sl);
            
            if (pts.length > 4) {
                var minX = 999999, maxX = -999999, minY = 999999, maxY = -999999;
                for (var i = 0; i < pts.length; i += 2) {
                    if (pts[i] < minX) minX = pts[i];
                    if (pts[i] > maxX) maxX = pts[i];
                    if (pts[i+1] < minY) minY = pts[i+1];
                    if (pts[i+1] > maxY) maxY = pts[i+1];
                }
                var spanX = maxX - minX, spanY = maxY - minY;
                addLog('  bbox X=' + Math.round(spanX) + ' Y=' + Math.round(spanY));
                
                if (spanX > 4 && spanY < 4) {
                    var yy = (minY + maxY) / 2;
                    var wl = 3.5, amp = 1.2;
                    var waves = Math.round(spanX / wl);
                    if (waves > 0) {
                        var step = spanX / waves;
                        RAW_beginPath.call(this);
                        RAW_moveTo.call(this, minX, yy);
                        for (var j = 0; j < waves; j++) {
                            var bx = minX + j * step;
                            this.bezierCurveTo(
                                bx + step * 0.25, yy + amp,
                                bx + step * 0.75, yy - amp,
                                bx + step, yy
                            );
                        }
                        RAW_stroke.call(this);
                        RAW_beginPath.call(this);
                        this._spPts = [];
                        addLog('  WAVE DRAWN!');
                        return;
                    }
                }
            }
        }
        
        this._spPts = [];
        return RAW_stroke.apply(this, arguments);
    };
}();
</script>"""

text = text.replace('</head>', script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Canvas hijack V5-DEBUG injected")
