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
    var logs = [];
    var isReady = false;
    var logDiv;
    
    document.addEventListener("DOMContentLoaded", function() {
        logDiv = document.createElement('div');
        logDiv.style.position = 'absolute';
        logDiv.style.zIndex = 999999;
        logDiv.style.top = '100px';
        logDiv.style.right = '10px';
        logDiv.style.background = 'rgba(0,0,0,0.8)';
        logDiv.style.color = '#00ff00';
        logDiv.style.padding = '10px';
        logDiv.style.width = '400px';
        logDiv.style.height = '500px';
        logDiv.style.overflow = 'hidden';
        logDiv.style.pointerEvents = 'none';
        logDiv.style.fontSize = '11px';
        logDiv.style.fontFamily = 'monospace';
        document.body.appendChild(logDiv);
        isReady = true;
        
        logs.forEach(function(msg) { addMsg(msg); });
    });

    function addMsg(msg) {
        if (!isReady) { logs.push(msg); return; }
        if (logDiv.childNodes.length > 35) logDiv.removeChild(logDiv.firstChild);
        var d = document.createElement('div');
        d.textContent = msg;
        logDiv.appendChild(d);
    }

    var rawFillRect = CanvasRenderingContext2D.prototype.fillRect;
    var rawStroke = CanvasRenderingContext2D.prototype.stroke;
    
    var lastMsg = '';
    var lastCount = 0;
    function logIt(msg) {
        if (msg === lastMsg) {
            lastCount++;
            if (isReady && logDiv.lastChild) {
                logDiv.lastChild.textContent = msg + ' (' + lastCount + ')';
            }
        } else {
            lastMsg = msg;
            lastCount = 1;
            addMsg(msg);
        }
    }

    function isPotentiallyRed(c) {
        if (!c) return false;
        var s = String(c).toLowerCase();
        return s.indexOf('red') > -1 || s.indexOf('ff00') > -1 || s.indexOf('d129') > -1 || s.indexOf('d229') > -1 || s.indexOf('255,') > -1 || s.indexOf('209,') > -1;
    }

    CanvasRenderingContext2D.prototype.fillRect = function(x, y, w, h) {
        if (isPotentiallyRed(this.fillStyle) && h <= 5 && w > 0) {
            logIt('fillR ' + this.fillStyle + ' x:' + Math.round(x) + ' y:' + Math.round(y) + ' w:' + Math.round(w) + ' h:' + Math.round(h));
        }
        return rawFillRect.apply(this, arguments);
    };

    CanvasRenderingContext2D.prototype.stroke = function() {
        if (isPotentiallyRed(this.strokeStyle)) {
            logIt('stroke ' + this.strokeStyle);
        }
        return rawStroke.apply(this, arguments);
    };
    
    var rawLineTo = CanvasRenderingContext2D.prototype.lineTo;
    CanvasRenderingContext2D.prototype.lineTo = function(x, y) {
        if (isPotentiallyRed(this.strokeStyle)) {
            logIt('lineTo ' + this.strokeStyle + ' x:' + Math.round(x) + ' y:' + Math.round(y));
        }
        return rawLineTo.apply(this, arguments);
    };

}();
</script>"""

if '</head>' in text:
    text = text.replace('</head>', script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("Canvas logger injected")
