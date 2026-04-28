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
            if (sl === '#ff0000' || sl === 'red') {
                var x0 = this._spPts[0], y0 = this._spPts[1];
                var x1 = this._spPts[2], y1 = this._spPts[3];
                
                if (Math.abs(y1 - y0) < 3 && Math.abs(x1 - x0) > 0.5) {
                    // Each tiny dash segment: offset Y by a sine wave based on X position
                    // All segments share the same frequency, creating a continuous wave
                    var freq = 0.9; // radians per pixel
                    var amp = 1.5;  // pixels amplitude
                    var midY = (y0 + y1) / 2;
                    var newY0 = midY + Math.sin(x0 * freq) * amp;
                    var newY1 = midY + Math.sin(x1 * freq) * amp;
                    
                    RAW_beginPath.call(this);
                    RAW_moveTo.call(this, x0, newY0);
                    RAW_lineTo.call(this, x1, newY1);
                    RAW_stroke.call(this);
                    RAW_beginPath.call(this);
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

print("Canvas hijack V8 injected (sine-offset dashes)")
