#!/usr/bin/env python3
"""
Unit & Integration Test Suite for Sovereign Avatar Agents (sovereign-avatar-agents)
Runs with both pytest and python3 test_solution.py (zero dependencies).
"""
import sys
import json
import unittest
import subprocess
from pathlib import Path
from dataclasses import asdict

SOLUTION_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOLUTION_ROOT))

from src.core import CoreEngine

class TestAvatarAgents(unittest.TestCase):
    def setUp(self):
        self.engine = CoreEngine()

    def test_01_engine_initialization_and_health(self):
        """Verifies engine health and default persona registrations."""
        health = self.engine.health_check()
        self.assertEqual(health["status"], "HEALTHY")
        self.assertEqual(health["service"], "sovereign-avatar-agents")
        self.assertEqual(health["domain"], "AI Persona Microservices")
        self.assertGreaterEqual(health["personas_loaded"], 4)
        self.assertIn("SentinelSRE", health["active_personas"])
        self.assertIn("ChefPro", health["active_personas"])

    def test_02_persona_catalog_integrity(self):
        """Ensures all persona profiles have required fields and expertise."""
        personas = self.engine.list_personas()
        self.assertGreaterEqual(len(personas), 4)
        for p in personas:
            self.assertTrue(p["name"])
            self.assertTrue(p["role"])
            self.assertTrue(p["system_prompt"])
            self.assertGreaterEqual(len(p["expertise"]), 1)

    def test_03_thermal_incident_diagnosis(self):
        """Verifies that a high CPU temperature payload from rpi-telemetry triggers SRE mitigation."""
        telemetry = {
            "node_id": "rpi-edge-test-01",
            "hardware": {
                "cpu_temp_celsius": 86.5,
                "ram_usage_percent": 45.0,
                "disk_usage_percent": 40.0
            },
            "alerts": [
                {"code": "ERR_THERMAL_RUNAWAY", "severity": "CRITICAL"}
            ]
        }
        diagnosis = self.engine.diagnose_iot_incident(telemetry)
        self.assertEqual(diagnosis.severity, "CRITICAL")
        self.assertEqual(diagnosis.persona_responder, "SentinelSRE")
        self.assertIn("86.5°C", diagnosis.root_cause)
        
        # Check that fan or frequency scaling directive was generated
        directives = " ".join(diagnosis.remediation_directives)
        self.assertIn("powersave", directives)
        self.assertIn("gpio", directives)

    def test_04_memory_incident_diagnosis(self):
        """Verifies that an OOM risk payload triggers page cache clear directives."""
        telemetry = {
            "node_id": "rpi-edge-test-02",
            "hardware": {
                "cpu_temp_celsius": 45.0,
                "ram_usage_percent": 95.2,
                "disk_usage_percent": 30.0
            }
        }
        diagnosis = self.engine.diagnose_iot_incident(telemetry)
        self.assertEqual(diagnosis.severity, "CRITICAL")
        self.assertIn("OOM", diagnosis.root_cause)
        directives = " ".join(diagnosis.remediation_directives)
        self.assertIn("drop_caches", directives)

    def test_05_optimal_telemetry_diagnosis(self):
        """Verifies that healthy edge metrics evaluate to OPTIMAL state."""
        telemetry = {
            "node_id": "rpi-edge-optimal",
            "hardware": {
                "cpu_temp_celsius": 44.0,
                "ram_usage_percent": 35.0,
                "disk_usage_percent": 42.0
            }
        }
        diagnosis = self.engine.diagnose_iot_incident(telemetry)
        self.assertEqual(diagnosis.severity, "OPTIMAL")
        self.assertIn("safe operational boundaries", diagnosis.root_cause)

    def test_06_episodic_dialogue_memory(self):
        """Verifies conversational memory accumulation across dialogue turns."""
        session = "test_session_42"
        res1 = self.engine.chat_turn("SentinelSRE", "Check thermal status", session)
        res2 = self.engine.chat_turn("SentinelSRE", "What about RAM limit?", session)
        self.assertEqual(res1["turn_count"], 2)
        self.assertEqual(res2["turn_count"], 4)
        self.assertIn("82°C", res1["response"])
        self.assertIn("92%", res2["response"])

    def test_07_idempotent_feature_execution(self):
        """Verifies that feature execution returns consistent SHA-256 tokens."""
        payload = {"persona": "SentinelSRE", "prompt": "Status check"}
        res1 = self.engine.execute_feature("diagnose_incident", payload)
        res2 = self.engine.execute_feature("diagnose_incident", payload)
        self.assertEqual(res1["status"], "SUCCESS")
        self.assertEqual(res1["idempotency_token"], res2["idempotency_token"])

    def test_08_cli_execution(self):
        """Verifies CLI execution via subprocess."""
        cli_path = SOLUTION_ROOT / "src" / "cli.py"
        res = subprocess.run([sys.executable, str(cli_path), "--health"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["status"], "HEALTHY")

    def test_09_storage_critical_diagnosis(self):
        """Verifies storage critical threshold generates docker/journalctl cleanup directives."""
        telemetry = {
            "node_id": "rpi-storage-critical",
            "hardware": {"cpu_temp_celsius": 45.0, "ram_usage_percent": 50.0, "disk_usage_percent": 96.2},
            "alerts": [{"code": "ERR_DISK_FULL", "severity": "CRITICAL", "message": "Storage 96.2% full"}]
        }
        diagnosis = self.engine.diagnose_iot_incident(telemetry)
        self.assertEqual(diagnosis.severity, "CRITICAL")
        self.assertIn("journalctl --vacuum-size=100M", diagnosis.remediation_directives)
        self.assertIn("docker system prune -f || true", diagnosis.remediation_directives)

    def test_10_cross_solution_query_fallback(self):
        """Verifies query_edge_telemetry handles unreachable endpoints gracefully with deterministic fallback."""
        res = self.engine.query_edge_telemetry(endpoint="http://127.0.0.1:9999")
        self.assertEqual(res["status"], "FALLBACK_SIMULATED")
        self.assertIn("ai_diagnosis", res)

if __name__ == "__main__":
    unittest.main(verbosity=2)
