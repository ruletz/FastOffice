import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<script id="canvas_hijack">.*?</script>\s*', '', text, flags=re.DOTALL)

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
        addLog('V11 DEBUGGER LOADED');
    });

    var lastRedStroke = 0;

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
        if (s && this._spPts && this._spPts.length > 0) {
            var sl = String(s).toLowerCase();
            var isRed = false;
            if (sl.indexOf('ff0000') >= 0 || sl.indexOf('ff4444') >= 0 || sl.indexOf('ef4444') >= 0 || sl.indexOf('red') >= 0 || sl.indexOf('255, 0, 0') >= 0 || sl.indexOf('239, 68, 68') >= 0) {
                isRed = true;
            }
            
            if (isRed) {
                var now = Date.now();
                if (now - lastRedStroke > 1000) {
                    addLog('--- NEW RED STROKE SESSION ---');
                }
                lastRedStroke = now;
                
                var pts = this._spPts;
                var dash = this.getLineDash ? this.getLineDash() : 'none';
                addLog('RED: pts=' + pts.length + ' dash=[' + dash + '] col=' + sl);
                
                if (pts.length >= 4) {
                    var x0 = pts[0], y0 = pts[1];
                    var x1 = pts[pts.length - 2], y1 = pts[pts.length - 1];
                    addLog('  y0=' + Math.round(y0) + ' y1=' + Math.round(y1) + ' dx=' + Math.round(x1-x0));
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

print("Canvas hijack V11 injected (Deep Debugger)")
