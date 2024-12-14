#!/usr/bin/env python3
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = 'localhost'
PORT = 8000
LOG_FILE = 'maze_log.csv'

class CSVRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/append_to_csv':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                line = data.get('line')
                if line:
                    # Append the line to the CSV file
                    with open(LOG_FILE, 'a', encoding='utf-8') as f:
                        f.write(line + '\n')
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status":"ok"}).encode('utf-8'))
                else:
                    self.send_error(400, "No line found in request")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
        else:
            self.send_error(404, "Not Found")

def run():
    server = HTTPServer((HOST, PORT), CSVRequestHandler)
    print(f"Serving on http://{HOST}:{PORT}")
    server.serve_forever()

if __name__ == '__main__':
    # Ensure that maze_log.csv exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("timestamp,email_hash,moves,path\n")

    run()
