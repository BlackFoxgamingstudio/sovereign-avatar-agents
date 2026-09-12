#!/usr/bin/env python3
"""
CLI entrypoint for sovereign-avatar-agents
Author: Russell Alan Powers
Domain: AI Persona Microservices & Incident Response
"""
import sys
import json
import argparse
from pathlib import Path

# Ensure src is importable
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SRC_DIR.parent))

from src.core import CoreEngine

def main():
    parser = argparse.ArgumentParser(
        description="Sovereign Avatar Agents: AI Persona Microservices & Autonomous Incident Response"
    )
    parser.add_argument("--health", action="store_true", help="Perform service health check")
    parser.add_argument("--list-personas", action="store_true", help="List registered AI personas")
    parser.add_argument("--persona", type=str, default="SentinelSRE", help="Selected persona (SentinelSRE, ChefPro, NovaPro, FacilitySentinel)")
    parser.add_argument("--chat", type=str, help="Send dialogue message to selected persona")
    parser.add_argument("--diagnose-incident", action="store_true", help="Diagnose edge telemetry incident payload")
    parser.add_argument("--inspect-edge", action="store_true", help="Query live edge telemetry from sovereign-rpi-telemetry (:8770)")
    parser.add_argument("--edge-url", type=str, default="http://127.0.0.1:8770", help="URL of sovereign-rpi-telemetry daemon")
    parser.add_argument("--exec", type=str, help="Execute specific domain feature")
    parser.add_argument("--payload", type=str, default="{}", help="JSON payload string")
    parser.add_argument("--format", type=str, choices=["json", "text"], default="json", help="Output format")
    args = parser.parse_args()

    engine = CoreEngine()

    if args.health:
        health = engine.health_check()
        print(json.dumps(health, indent=2))
        sys.exit(0)

    if args.list_personas:
        personas = engine.list_personas()
        if args.format == "json":
            print(json.dumps(personas, indent=2))
        else:
            print("=== REGISTERED SOVEREIGN AI PERSONAS ===")
            for p in personas:
                print(f"[{p['id']}] {p['name']} ({p['role']})")
                print(f"  Expertise: {', '.join(p['expertise'])}")
                print(f"  Description: {p['description']}\n")
        sys.exit(0)

    if args.inspect_edge:
        res = engine.query_edge_telemetry(args.edge_url)
        print(json.dumps(res, indent=2))
        sys.exit(0)

    if args.diagnose_incident:
        try:
            payload = json.loads(args.payload)
        except Exception:
            payload = {}
        # If no payload provided, generate realistic thermal spike test case
        if not payload or not payload.get("hardware"):
            payload = {
                "node_id": "sbb-edge-blackloin45-GODISBLACK.local",
                "hardware": {
                    "cpu_temp_celsius": 86.4,
                    "cpu_usage_percent": 95.0,
                    "ram_usage_percent": 94.2,
                    "disk_usage_percent": 98.5
                },
                "alerts": [
                    {"severity": "CRITICAL", "code": "ERR_THERMAL_RUNAWAY", "message": "CPU Temp: 86.4°C"}
                ]
            }
        diagnosis = engine.diagnose_iot_incident(payload)
        from dataclasses import asdict
        out = asdict(diagnosis)
        if args.format == "json":
            print(json.dumps(out, indent=2))
        else:
            print(f"=== SRE INCIDENT DIAGNOSIS: {out['incident_id']} ===")
            print(f"Target Node: {out['target_node']} | Severity: {out['severity']}")
            print(f"Root Cause:  {out['root_cause']}")
            print("Remediation Directives:")
            for d in out['remediation_directives']:
                print(f"  - {d}")
        sys.exit(0)

    if args.chat:
        turn = engine.chat_turn(args.persona, args.chat)
        if args.format == "json":
            print(json.dumps(turn, indent=2))
        else:
            print(f"[{turn['persona']}]: {turn['response']}")
        sys.exit(0)

    if args.exec:
        try:
            p = json.loads(args.payload)
        except Exception:
            p = {"raw": args.payload}
        res = engine.execute_feature(args.exec, p)
        print(json.dumps(res, indent=2))
        sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()
