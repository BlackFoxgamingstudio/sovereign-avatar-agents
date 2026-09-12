#!/usr/bin/env python3
"""
Standalone Microservice Webhook Adapter for sovereign-avatar-agents
Author: Russell Alan Powers
Port: 8785

Exposes RESTful endpoints, OpenAPI 3.1, and Swagger UI:
- GET  /health, /healthz : Service status, uptime, registered personas
- GET  /openapi.json     : Machine-readable OpenAPI 3.1 specification
- GET  /docs             : Interactive browser-based Swagger UI
- GET  /api/v1/personas  : Metadata catalog of all active persona matrices
- GET  /api/v1/edge-vitals : Queries sovereign-rpi-telemetry (:8770) and returns AI diagnosis
- POST /api/v1/diagnose-incident : Ingests telemetry alerts and emits SentinelSRE mitigation playbook
- POST /api/v1/chat : Stateful conversational turns with episodic memory
- POST /api/v1/execute : Generic idempotent feature dispatcher
"""

import sys
import os
import json
import signal
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from dataclasses import asdict

SOLUTION_ROOT = Path(__file__).resolve().parent.parent
if str(SOLUTION_ROOT) not in sys.path:
    sys.path.insert(0, str(SOLUTION_ROOT))

from src.core import CoreEngine

PORT = int(os.environ.get("SBB_AVATAR_PORT", 8785))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [AvatarAdapter] %(message)s")
logger = logging.getLogger("AvatarAdapter")

engine = CoreEngine()

OPENAPI_SPEC = {
    "openapi": "3.1.0",
    "info": {
        "title": "SBB Solution 02: Sovereign AI Avatar Agents & SRE Autonomous Healer API",
        "description": "Multi-persona AI microservice framework featuring SentinelSRE, ChefPro, NovaPro, and FacilitySentinel with closed-loop incident mitigation.",
        "version": "1.0.0",
        "contact": {"name": "Russell Alan Powers", "email": "russell@sovereignbizbox.io"}
    },
    "servers": [{"url": f"http://127.0.0.1:{PORT}", "description": "Local Avatar Daemon"}],
    "paths": {
        "/health": {
            "get": {
                "summary": "Service Health & Persona Inventory",
                "responses": {"200": {"description": "Service health"}}
            }
        },
        "/api/v1/personas": {
            "get": {
                "summary": "List All Registered AI Personas",
                "responses": {"200": {"description": "Persona catalog"}}
            }
        },
        "/api/v1/edge-vitals": {
            "get": {
                "summary": "Pull Live Edge Telemetry & Synthesize AI Diagnosis",
                "responses": {"200": {"description": "Live edge assessment"}}
            }
        },
        "/api/v1/diagnose-incident": {
            "post": {
                "summary": "Diagnose Hardware Anomaly & Emit SRE Playbook Directives",
                "requestBody": {
                    "content": {"application/json": {"schema": {"type": "object"}}}
                },
                "responses": {"200": {"description": "Incident diagnosis and directives"}}
            }
        },
        "/api/v1/chat": {
            "post": {
                "summary": "Execute Stateful Dialogue Turn with Persona",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "persona": {"type": "string", "example": "SentinelSRE"},
                                    "message": {"type": "string", "example": "Check thermal limits"},
                                    "session_id": {"type": "string", "example": "session_01"}
                                }
                            }
                        }
                    }
                },
                "responses": {"200": {"description": "Conversational turn response"}}
            }
        },
        "/api/v1/execute": {
            "post": {
                "summary": "Generic Idempotent Feature Dispatcher",
                "responses": {"200": {"description": "Execution result with SHA-256 token"}}
            }
        }
    }
}

SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SBB Solution 02 - Avatar Agents API</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
  <style>
    body { margin: 0; padding: 0; background: #fafafa; }
    .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: '/openapi.json',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis]
      });
    };
  </script>
</body>
</html>
"""

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class WebhookHandler(BaseHTTPRequestHandler):
    server_version = "SBB-AvatarAgents/1.0.0"

    def _set_cors_headers(self, content_type="application/json; charset=utf-8"):
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, X-Correlation-ID")
        corr_id = self.headers.get("X-Correlation-ID")
        if corr_id:
            self.send_header("X-Correlation-ID", corr_id)

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header("Content-Length", str(len(body)))
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
            res = engine.health_check()
            res["docs_url"] = f"http://127.0.0.1:{PORT}/docs"
            self._send_json(200, res)
        elif path == "/openapi.json":
            self._send_json(200, OPENAPI_SPEC)
        elif path in ("/docs", "/swagger"):
            self.send_response(200)
            self._set_cors_headers(content_type="text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(SWAGGER_UI_HTML.encode("utf-8"))
        elif path == "/api/v1/personas":
            self._send_json(200, {"personas": engine.list_personas()})
        elif path == "/api/v1/edge-vitals":
            res = engine.query_edge_telemetry("http://127.0.0.1:8770")
            self._send_json(200, res)
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": self.path})

    def do_POST(self):
        auth_header = self.headers.get("X-SBB-Auth")
        if auth_header != os.environ.get("SBB_SHARED_SECRET", "sbb_local_dev_secret_2026"):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return

        path = self.path.split("?")[0].rstrip("/")
        data = self._read_json_body()

        if path in ("/api/v1/diagnose-incident", "/diagnose"):
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
        pass

def run(port: int = 8785):
    server = ThreadedHTTPServer(("0.0.0.0", port), WebhookHandler)
    logger.info(f"Sovereign Avatar Agents Microservice listening on http://127.0.0.1:{port}")
    logger.info(f"Interactive Swagger UI: http://127.0.0.1:{port}/docs")

    def handle_signal(sig, frame):
        logger.info(f"Signal {sig} received. Initiating graceful shutdown...")
        server.server_close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        server.serve_forever()
    except Exception as e:
        logger.info(f"Server shutting down: {e}")
    finally:
        server.server_close()

if __name__ == "__main__":
    run(PORT)
