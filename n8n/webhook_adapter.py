#!/usr/bin/env python3
"""
Standalone Microservice Webhook Adapter for sovereign-avatar-agents
Listens on port 8785 and translates n8n requests into deterministic engine executions.
"""
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

SOLUTION_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOLUTION_ROOT))

from src.core import CoreEngine

engine = CoreEngine()

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(engine.health_check()).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {"raw": body}

        action = data.get("action", "default_action")
        payload = data.get("payload", data)
        res = engine.execute_feature(action, payload)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(res).encode("utf-8"))

    def log_message(self, format, *args):
        pass

def run():
    server = HTTPServer(("0.0.0.0", 8785), WebhookHandler)
    print(f"[Sovereign Avatar Agents] Webhook Adapter listening on http://0.0.0.0:8785")
    server.serve_forever()

if __name__ == "__main__":
    run()
