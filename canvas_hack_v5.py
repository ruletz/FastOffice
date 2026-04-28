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
        if (s && this._spPts && this._spPts.length > 4) {
            var sl = String(s).toLowerCase();
            if (sl === '#ff0000' || sl === 'red') {
                var pts = this._spPts;
                var minX = 999999, maxX = -999999;
                var minY = 999999, maxY = -999999;
                for (var i = 0; i < pts.length; i += 2) {
                    var px = pts[i], py = pts[i+1];
                    if (px < minX) minX = px;
                    if (px > maxX) maxX = px;
                    if (py < minY) minY = py;
                    if (py > maxY) maxY = py;
                }
                var spanX = maxX - minX;
                var spanY = maxY - minY;
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

print("Canvas hijack V5 injected")
