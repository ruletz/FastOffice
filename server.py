from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            with open('c:/Projects/OnlyOffice/dumped_DOM.html', 'w', encoding='utf-8') as f:
                f.write(body)
            print("DOM dumped successfully to dumped_DOM.html")
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            print("Error in POST:", e)
            traceback.print_exc()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} {format%args}")

httpd = HTTPServer(('127.0.0.1', 8888), SimpleHTTPRequestHandler)
print("Listening on port 8888...")
httpd.serve_forever()
