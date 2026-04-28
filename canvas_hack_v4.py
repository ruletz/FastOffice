import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Remove any old canvas hijack
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
            if (sl === '#ff0000' || sl === 'red') {
                var x0 = this._spPts[0], y0 = this._spPts[1];
                var x1 = this._spPts[2], y1 = this._spPts[3];
                if (Math.abs(y1 - y0) < 2 && (x1 - x0) > 2) {
                    // Horizontal red line detected! Replace with wave.
                    var dx = x1 - x0;
                    var wl = 3.5, amp = 1.2;
                    var waves = Math.round(dx / wl);
                    if (waves > 0) {
                        var step = dx / waves;
                        var yy = (y0 + y1) / 2 + 1;
                        // Draw wave on a fresh path, use RAW calls only
                        RAW_beginPath.call(this);
                        RAW_moveTo.call(this, x0, yy);
                        for (var i = 0; i < waves; i++) {
                            var bx = x0 + i * step;
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

print("Canvas hijack V4 injected (fixed recursion bug)")
