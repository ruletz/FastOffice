import codecs

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'
with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

script = """<script id="canvas_hijack">
window._onlyoffice_spell_points = [];
!function() {
    var rawMoveTo = CanvasRenderingContext2D.prototype.moveTo;
    var rawLineTo = CanvasRenderingContext2D.prototype.lineTo;
    var rawStroke = CanvasRenderingContext2D.prototype.stroke;
    var rawBeginPath = CanvasRenderingContext2D.prototype.beginPath;
    
    // Polyfill for drawing wavy lines!
    CanvasRenderingContext2D.prototype.drawWavyLine = function(x1, y1, x2, y2) {
        var wavelength = 3;
        var amplitude = 1.5;
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
        this._currentPathPts = [];
        return rawBeginPath.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.moveTo = function(x, y) {
        if (this._currentPathPts) this._currentPathPts.push({t: 'M', x: x, y: y});
        return rawMoveTo.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.lineTo = function(x, y) {
        if (this._currentPathPts) this._currentPathPts.push({t: 'L', x: x, y: y});
        return rawLineTo.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.stroke = function() {
        if (this.strokeStyle && (this.strokeStyle.toLowerCase() === '#ff0000' || this.strokeStyle.toLowerCase() === 'red' || this.strokeStyle.toLowerCase().indexOf('ff0000') !== -1) && this._currentPathPts && this._currentPathPts.length === 2) {
            var p1 = this._currentPathPts[0];
            var p2 = this._currentPathPts[1];
            if (p1.y === p2.y && p2.x > p1.x && (p2.x - p1.x) > 2) {
                // IT IS A HORIZONTAL RED LINE! Probably Spell Check!
                // Intercept and draw wavy instead!
                this.save();
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

if 'canvas_hijack' not in text:
    text = text.replace('</head>', script + '\n</head>')
    with codecs.open(html_path, 'w', 'utf8') as f:
        f.write(text)
    print("Script injected!")
else:
    print("Script already injected.")
