import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

text = re.sub(r'<script id="canvas_hijack">.*?</script>', '', text, flags=re.DOTALL)

script = """<script id="canvas_hijack">
window._onlyoffice_spell_points = [];
!function() {
    var rawFillRect = CanvasRenderingContext2D.prototype.fillRect;
    var rawStroke = CanvasRenderingContext2D.prototype.stroke;
    var rawBeginPath = CanvasRenderingContext2D.prototype.beginPath;
    var rawMoveTo = CanvasRenderingContext2D.prototype.moveTo;
    var rawLineTo = CanvasRenderingContext2D.prototype.lineTo;

    // A robust, squiggly bezier curve draw
    CanvasRenderingContext2D.prototype.drawWavyLine = function(x1, y1, x2, y2) {
        var wavelength = 3.5;
        var amplitude = 1.8;
        this.beginPath();
        var dx = x2 - x1;
        var dy = y2 - y1;
        var len = Math.sqrt(dx * dx + dy * dy);
        var waves = Math.round(len / wavelength);
        if (waves === 0) return;
        var wl = len / waves;
        var a = Math.atan2(dy, dx);
        this.moveTo(x1, y1);
        for (var i = 0; i < waves; i++) {
            var cp1x = x1 + Math.cos(a) * (i * wl + wl / 4) - Math.sin(a) * amplitude;
            var cp1y = y1 + Math.sin(a) * (i * wl + wl / 4) + Math.cos(a) * amplitude;
            var cp2x = x1 + Math.cos(a) * (i * wl + wl * 3 / 4) + Math.sin(a) * amplitude;
            var cp2y = y1 + Math.sin(a) * (i * wl + wl * 3 / 4) - Math.cos(a) * amplitude;
            var ep_x = x1 + Math.cos(a) * (i * wl + wl);
            var ep_y = y1 + Math.sin(a) * (i * wl + wl);
            
            this.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, ep_x, ep_y);
        }
    };

    CanvasRenderingContext2D.prototype.beginPath = function() {
        this._myPath = [];
        return rawBeginPath.apply(this, arguments);
    };
    
    CanvasRenderingContext2D.prototype.moveTo = function(x, y) {
        if (this._myPath) this._myPath.push({x: x, y: y});
        return rawMoveTo.apply(this, arguments);
    };
    
    CanvasRenderingContext2D.prototype.lineTo = function(x, y) {
        if (this._myPath) this._myPath.push({x: x, y: y});
        return rawLineTo.apply(this, arguments);
    };

    function isSpellRed(colorStr) {
        if (!colorStr) return false;
        var s = String(colorStr).toLowerCase();
        // #ff0000, #d12915, rgb(255, 0, 0), and dark red #d22915
        if (s.indexOf('#ff0000') !== -1) return true;
        if (s.indexOf('255, 0, 0') !== -1) return true;
        if (s.indexOf('#d1') !== -1 && s.indexOf('15') !== -1) return true; 
        if (s.indexOf('d22915') !== -1) return true;
        if (s === 'red') return true;
        return false;
    }

    // Capture ONLYOFFICE filling small red rectangles for dotted/dashed spell lines
    CanvasRenderingContext2D.prototype.fillRect = function(x, y, w, h) {
        if (isSpellRed(this.fillStyle)) {
            // A horizontal spell checker dash is usually a tiny rectangle h=1 or 2, and w > 1
            // OR if w is very tiny and it's drawing dots. We'll simply draw a subtle wave and NOT fill the rect.
            // But wait, it calls fillRect 50 times for a line. We don't want 50 tiny waves!
            // Actually, if it's a dotted line, it's better to bypass fillRect and wait. 
            // We can check if w > 5. If w is small, we just skip? 
            // Better yet, if it's explicitly drawing horizontal red rects:
            if (h <= 3 && w > 1) {
                this.save();
                this.strokeStyle = this.fillStyle;
                this.lineWidth = 1; // or h
                this.setLineDash([]); // clear dash 
                this.drawWavyLine(x, y + 1, x + w, y + 1);
                rawStroke.call(this); // draw wave
                this.restore();
                // do not call rawFillRect so it doesn't draw the rectangle
                return;
            }
        }
        return rawFillRect.apply(this, arguments);
    };

    // Capture explicit stroke
    CanvasRenderingContext2D.prototype.stroke = function() {
        if (isSpellRed(this.strokeStyle) && this._myPath && this._myPath.length >= 2) {
            var p1 = this._myPath[0];
            var p2 = this._myPath[this._myPath.length - 1]; 
            // Are they roughly on the same Y axis, and separated by X?
            if (Math.abs(p2.y - p1.y) <= 3 && Math.abs(p2.x - p1.x) >= 2) {
                var originalStroke = this.strokeStyle;
                this.save();
                this.strokeStyle = originalStroke;
                this.setLineDash([]);
                this.drawWavyLine(p1.x, p1.y + 1, p2.x, p2.y + 1);
                rawStroke.call(this);
                this.restore();
                return;
            }
        }
        return rawStroke.apply(this, arguments);
    };
}();
</script>"""

if '</head>' in text:
    text = text.replace('</head>', script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Canvas hijack V2 injected")
