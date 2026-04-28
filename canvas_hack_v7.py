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

    // Accumulate red horizontal dashes per canvas, then flush as one wave
    var pendingWaves = new WeakMap();

    function flushWave(ctx) {
        var pw = pendingWaves.get(ctx);
        if (!pw || pw.segments.length === 0) return;
        
        var segs = pw.segments;
        var minX = segs[0].x0, maxX = segs[0].x1;
        var sumY = 0, count = 0;
        for (var i = 0; i < segs.length; i++) {
            if (segs[i].x0 < minX) minX = segs[i].x0;
            if (segs[i].x1 > maxX) maxX = segs[i].x1;
            sumY += segs[i].y;
            count++;
        }
        var yy = sumY / count;
        var spanX = maxX - minX;
        
        if (spanX > 4) {
            var wl = 3.5, amp = 1.2;
            var waves = Math.max(1, Math.round(spanX / wl));
            var step = spanX / waves;
            
            ctx.save();
            ctx.setTransform(1,0,0,1,0,0);
            ctx.strokeStyle = '#ff0000';
            ctx.lineWidth = pw.lineW || 1;
            RAW_beginPath.call(ctx);
            RAW_moveTo.call(ctx, minX, yy);
            for (var j = 0; j < waves; j++) {
                var bx = minX + j * step;
                ctx.bezierCurveTo(
                    bx + step * 0.25, yy + amp,
                    bx + step * 0.75, yy - amp,
                    bx + step, yy
                );
            }
            RAW_stroke.call(ctx);
            RAW_beginPath.call(ctx);
            ctx.restore();
        }
        
        pw.segments = [];
        pw.timer = null;
    }

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
                    // Suppress the original dash, accumulate for wave
                    if (!pendingWaves.has(this)) {
                        pendingWaves.set(this, { segments: [], timer: null, lineW: 1 });
                    }
                    var pw = pendingWaves.get(this);
                    pw.segments.push({ x0: Math.min(x0,x1), x1: Math.max(x0,x1), y: (y0+y1)/2 });
                    pw.lineW = this.lineWidth;
                    
                    // Schedule flush via microtask (fires after all sync dashes are drawn)
                    if (!pw.timer) {
                        var self = this;
                        pw.timer = Promise.resolve().then(function() { flushWave(self); });
                    }
                    
                    // Don't draw the original dash
                    this._spPts = [];
                    RAW_beginPath.call(this);
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

print("Canvas hijack V7 injected (batch accumulation)")
