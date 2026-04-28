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
    var RAW_bezierCurveTo = CanvasRenderingContext2D.prototype.bezierCurveTo;
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
            if (sl === '#ff0000') {
                var x0 = this._spPts[0], y0 = this._spPts[1];
                var x1 = this._spPts[2], y1 = this._spPts[3];
                var dx = x1 - x0;
                
                if (Math.abs(y1 - y0) < 3 && Math.abs(dx) > 5) {
                    var wl = 4.0, amp = 1.5;
                    var adx = Math.abs(dx);
                    var waves = Math.max(1, Math.round(adx / wl));
                    var step = dx / waves;
                    
                    RAW_beginPath.call(this);
                    RAW_moveTo.call(this, x0, y0);
                    
                    var bIsInt;
                    if (this.canvas && this.canvas.id) {
                        // OnlyOffice sets integer grid internally, making bezier useless
                        // The engine is rounding coordinates to integers!
                        // Let's draw real lines instead of bezier curves to make a zigzag!
                    }
                    
                    // We will draw a zigzag using RAW_lineTo because bezier might be getting stripped or failed
                    for (var j = 0; j < waves; j++) {
                        var bx = x0 + j * step;
                        RAW_lineTo.call(this, bx + step * 0.25, y0 + amp);
                        RAW_lineTo.call(this, bx + step * 0.75, y0 - amp);
                        RAW_lineTo.call(this, bx + step, y0);
                    }
                    
                    RAW_stroke.call(this);
                    RAW_beginPath.call(this); // flush
                    
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

print("Canvas hijack V13 injected (ZigZag RAW_lineTo)")
