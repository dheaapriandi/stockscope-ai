"""
StockScope AI - Local Server & REST API
Runs a lightweight HTTP server serving the Web Dashboard and providing JSON API endpoints.
"""

import http.server
import json
import os
import socketserver
import urllib.parse
import webbrowser
from stockscope import analyze_topic, get_gap_table, get_brainstorm_ideas

PORT = 5055
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class StockScopeHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with API routing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API: /api/analyze
        if path == "/api/analyze":
            topic = query.get("topic", [""])[0]
            asset_type = query.get("type", ["footage"])[0]
            style = query.get("style", [""])[0]
            subject_mode = query.get("subject", [""])[0]
            timeframe = query.get("timeframe", [""])[0]

            data = analyze_topic(
                topic=topic,
                asset_type=asset_type,
                style=style,
                subject_mode=subject_mode,
                timeframe=timeframe
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # API: /api/gap-table
        if path == "/api/gap-table":
            filter_type = query.get("type", ["all"])[0]
            data = get_gap_table(filter_type)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # API: /api/brainstorm
        if path == "/api/brainstorm":
            asset_type = query.get("type", ["footage"])[0]
            data = get_brainstorm_ideas(asset_type)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # Default: Serve static files (index.html, etc.)
        return super().do_GET()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), StockScopeHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(f"🚀 StockScope AI Server running at: {url}")
        print("Membuka browser otomatis...")
        print("Tekan Ctrl + C di terminal untuk menghentikan server.")
        print("=" * 60)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dihentikan.")

if __name__ == "__main__":
    run_server()
