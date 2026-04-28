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
        if (s && this._spPts && this._spPts.length === 4) {
            var sl = String(s).toLowerCase();
            // Browsers often normalize to rgb or rgba
            var isRed = false;
            if (sl === '#ff0000' || sl === 'red') isRed = true;
            else if (sl.indexOf('rgb(255, 0, 0)') >= 0 || sl.indexOf('rgba(255, 0, 0') >= 0 || sl.indexOf('239, 68, 68') >= 0) isRed = true;
            // Also check drawing's spellcheck color rgb(239, 68, 68) or #EF4444 which we saw earlier!
            if (sl === '#ef4444') isRed = true;
            
            if (isRed) {
                var x0 = this._spPts[0], y0 = this._spPts[1];
                var x1 = this._spPts[2], y1 = this._spPts[3];
                var dx = x1 - x0;
                
                // Allow drawing wavy if line is mostly horizontal
                if (Math.abs(y1 - y0) < 3 && Math.abs(dx) > 1) {
                    var yy = (y0 + y1) / 2 + 1;
                    var wl = 3.5, amp = 1.0;
                    var adx = Math.abs(dx);
                    var waves = Math.max(1, Math.round(adx / wl));
                    var step = adx / waves;
                    var startX = Math.min(x0, x1);
                    
                    var oldDash = [];
                    if (this.getLineDash) oldDash = this.getLineDash();
                    if (this.setLineDash) this.setLineDash([]);
                    
                    RAW_beginPath.call(this);
                    RAW_moveTo.call(this, startX, yy);
                    for (var j = 0; j < waves; j++) {
                        var bx = startX + j * step;
                        this.bezierCurveTo(
                            bx + step * 0.25, yy + amp,
                            bx + step * 0.75, yy - amp,
                            bx + step, yy
                        );
                    }
                    RAW_stroke.call(this);
                    RAW_beginPath.call(this);
                    
                    if (this.setLineDash) this.setLineDash(oldDash);
                    
                    this._spPts = [];
                    return;
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

print("Canvas hijack V10 injected")
