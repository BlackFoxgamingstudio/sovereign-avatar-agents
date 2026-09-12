#!/usr/bin/env python3
"""
Standalone Microservice Webhook Adapter for sovereign-avatar-agents
Author: Russell Alan Powers
Port: 8785

Exposes RESTful endpoints for n8n workflow integration and cross-solution orchestration:
- GET  /health, /healthz : Service status, uptime, registered personas
- GET  /api/v1/personas  : Metadata catalog of all active persona matrices
- GET  /api/v1/edge-vitals : Queries sovereign-rpi-telemetry (:8770) and returns AI diagnosis
- POST /api/v1/diagnose-incident : Ingests telemetry alerts and emits SentinelSRE mitigation playbook
- POST /api/v1/chat : Stateful conversational turns with episodic memory
- POST /api/v1/execute : Generic idempotent feature dispatcher
"""

import sys
import os
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from dataclasses import asdict

SOLUTION_ROOT = Path(__file__).resolve().parent.parent
if str(SOLUTION_ROOT) not in sys.path:
    sys.path.insert(0, str(SOLUTION_ROOT))

from src.core import CoreEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [AvatarAdapter] %(message)s")
logger = logging.getLogger("AvatarAdapter")

engine = CoreEngine()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class WebhookHandler(BaseHTTPRequestHandler):
    server_version = "SBB-AvatarAgents/1.0.0"

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        try:
            return json.loads(raw)
        except Exception as e:
            logger.warning(f"Failed to parse JSON body: {e}")
            return {"raw": raw}

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        if path in ("", "/health", "/healthz"):
            self._send_json(200, engine.health_check())
        elif path == "/api/v1/personas":
            self._send_json(200, {"personas": engine.list_personas()})
        elif path == "/api/v1/edge-vitals":
            # Direct cross-solution query to sovereign-rpi-telemetry
            res = engine.query_edge_telemetry("http://127.0.0.1:8770")
            self._send_json(200, res)
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": self.path})

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")
        data = self._read_json_body()

        if path in ("/api/v1/diagnose-incident", "/diagnose"):
            # Handles incident telemetry payload from sovereign-rpi-telemetry or n8n
            telemetry = data.get("payload", data)
            diagnosis = engine.diagnose_iot_incident(telemetry)
            self._send_json(200, {
                "status": "SUCCESS",
                "diagnosis": asdict(diagnosis)
            })

        elif path in ("/api/v1/chat", "/chat"):
            persona = data.get("persona", "SentinelSRE")
            message = data.get("message") or data.get("prompt") or "Status check"
            session_id = data.get("session_id", "web_session_01")
            turn = engine.chat_turn(persona, message, session_id)
            self._send_json(200, {
                "status": "SUCCESS",
                "turn": turn
            })

        elif path in ("/api/v1/execute", "/execute", "/"):
            action = data.get("action", "diagnose_incident")
            payload = data.get("payload", data)
            res = engine.execute_feature(action, payload)
            self._send_json(200, res)

        else:
            self._send_json(404, {"error": "POST endpoint not found", "path": self.path})

    def log_message(self, fmt, *args):
        # Suppress verbose standard HTTP server console spam unless error
        pass

def run(port: int = 8785):
    server = ThreadedHTTPServer(("0.0.0.0", port), WebhookHandler)
    logger.info(f"Sovereign Avatar Agents Microservice listening on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down microservice server...")
        server.server_close()

if __name__ == "__main__":
    port = int(os.environ.get("SBB_AVATAR_PORT", 8785))
    run(port)
