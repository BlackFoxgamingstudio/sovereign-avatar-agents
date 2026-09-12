#!/usr/bin/env python3
"""
CLI entrypoint for sovereign-avatar-agents
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
    parser = argparse.ArgumentParser(description="Autonomous AI persona microservices framework. Manages stateful conversational agents with distinct personality matrices (Chef Pro, Nova Pro, Butterfly Pro), episodic memory buffers, and low-latency WebSocket dialogue streams.")
    parser.add_argument("--health", action="store_true", help="Perform service health check")
    parser.add_argument("--exec", type=str, default="default_action", help="Execute specific domain feature")
    parser.add_argument("--payload", type=str, default="{}", help="JSON payload string")
    parser.add_argument("--format", type=str, choices=["json", "text"], default="json", help="Output format")
    args = parser.parse_args()

    engine = CoreEngine()

    if args.health:
        health = engine.health_check()
        print(json.dumps(health, indent=2))
        sys.exit(0)

    try:
        p = json.loads(args.payload)
    except Exception:
        p = {"raw": args.payload}

    res = engine.execute_feature(args.exec, p)
    if args.format == "json":
        print(json.dumps(res, indent=2))
    else:
        print(f"Status: {res['status']} | Token: {res['idempotency_token']}")
        print(res['result']['message'])

if __name__ == "__main__":
    main()
