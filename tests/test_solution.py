#!/usr/bin/env python3
"""
Unit & Integration Test Suite for sovereign-avatar-agents
Runs with both pytest and python3 test_solution.py (zero dependencies).
"""
import sys
import json
import unittest
from pathlib import Path

SOLUTION_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOLUTION_ROOT))

from src.core import CoreEngine

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.engine = CoreEngine()

    def test_01_engine_initialization(self):
        health = self.engine.health_check()
        self.assertEqual(health["status"], "HEALTHY")
        self.assertEqual(health["service"], "sovereign-avatar-agents")
        self.assertEqual(health["domain"], "AI Persona Microservices")

    def test_02_feature_execution_success(self):
        res = self.engine.execute_feature("sync_data", {"item_id": 42})
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["feature"], "sync_data")
        self.assertIn("idempotency_token", res)

    def test_03_idempotency_token_consistency(self):
        payload = {"key": "test_value", "number": 100}
        res1 = self.engine.execute_feature("calculate_hash", payload)
        res2 = self.engine.execute_feature("calculate_hash", payload)
        self.assertEqual(res1["idempotency_token"], res2["idempotency_token"])

    def test_04_payload_integrity(self):
        payload = {"zone": "Alpha", "sensor": "temp_01", "reading": 23.4}
        res = self.engine.execute_feature("record_metric", payload)
        self.assertEqual(res["result"]["input_data"]["reading"], 23.4)

if __name__ == "__main__":
    unittest.main(verbosity=2)
