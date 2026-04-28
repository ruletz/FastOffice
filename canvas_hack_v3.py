import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# remove old hijack
text = re.sub(r'<script id="canvas_hijack">.*?</script>', '', text, flags=re.DOTALL)

script = """<script id="canvas_hijack">
window._onlyoffice_spell_points = [];
!function() {
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
        if (s.indexOf('#ff0000') !== -1) return true;
        if (s.indexOf('255, 0, 0') !== -1) return true;
        if (s === 'red') return true;
        return false;
    }

    // Capture explicit stroke
    CanvasRenderingContext2D.prototype.stroke = function() {
        if (isSpellRed(this.strokeStyle) && this._myPath && this._myPath.length > 2) {
            
            var minX = 999999, maxX = -999999;
            var minY = 999999, maxY = -999999;
            
            for(var i=0; i<this._myPath.length; i++) {
                var p = this._myPath[i];
                if (p.x < minX) minX = p.x;
                if (p.x > maxX) maxX = p.x;
                if (p.y < minY) minY = p.y;
                if (p.y > maxY) maxY = p.y;
            }

            // If the path consists of many dot segments, they will be mostly horizontally aligned
            if (Math.abs(maxY - minY) <= 3 && (maxX - minX) > 4) {
                var avgY = (minY + maxY) / 2;
                var originalStroke = this.strokeStyle;
                
                this.save();
                this.strokeStyle = originalStroke;
                this.lineWidth = 1;
                this.setLineDash([]);
                
                // We wipe the engine's dotted path and draw our own wavy one
                this.drawWavyLine(minX, avgY, maxX, avgY);
                
                // Stroke the wave!
                rawStroke.call(this);
                this.restore();
                
                // Clear the path so the engine doesn't draw its dots if it calls fill or something
                this._myPath = [];
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

print("Canvas hijack V3 injected")
