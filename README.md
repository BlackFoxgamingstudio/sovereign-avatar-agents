# Sovereign Avatar Agents (`sovereign-avatar-agents`)

[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](pyproject.toml)
[![Tests](https://img.shields.io/badge/pytest-10%20passed%20100%25-brightgreen.svg)](tests/test_solution.py)
[![n8n Integration](https://img.shields.io/badge/n8n-workflow_active-orange.svg)](n8n/workflow.json)
[![Cross-Solution Integration](https://img.shields.io/badge/SBB-Mutual%20Ecosystem%20Integrated-purple.svg)](n8n/workflow.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Autonomous AI Persona Microservices & SRE Self-Healing Engine**: Manages stateful conversational agents with distinct personality matrices (`SentinelSRE`, `ChefPro`, `NovaPro`, `FacilitySentinel`), episodic memory buffers, and real-time diagnostic response streams. Fully integrated into the Sovereign Biz Box ecosystem with closed-loop autonomous IoT incident diagnosis and automated remediation.

---

## 1. Architectural Blueprint & Mutual Ecosystem Integration

`sovereign-avatar-agents` operates both as an independent standalone Python package and as an autonomous microservice component in the **Sovereign Biz Box (SBB)** platform. It establishes a closed-loop autonomous self-healing ecosystem with **Solution 01 (`sovereign-rpi-telemetry`)**:

```
 ┌──────────────────────────────────────┐          IoT Vitals Spike (>82°C / >92% RAM)
 │  Solution 01: sovereign-rpi-telemetry│ ─────────────────────────────────────────────┐
 │       (Port 8770 Daemon)             │                                              │
 └──────────────────────────────────────┘                                              ▼
                    │                                                     ┌───────────────────────────┐
                    │ Heartbeat & Incident Audit                          │     n8n Event Engine      │
                    ▼                                                     │   (Port 5678 Webhooks)    │
 ┌──────────────────────────────────────┐                                 └───────────────────────────┘
 │       SBB Vault REST Bridge          │                                              │
 │            (Port 8766)               │                                              │ /webhook/avatar-agents
 │   Writes: facility_telemetry_v2.db   │                                              ▼
 └──────────────────────────────────────┘                                 ┌───────────────────────────┐
                    ▲                                                     │  Solution 02:             │
                    │ Publishes SRE Playbook Directive                    │  sovereign-avatar-agents  │
                    └──────────────────────────────────────────────────── │       (Port 8785)         │
                                                                          └───────────────────────────┘
                                                                                       │
                                                                                       ▼
                                                                          ┌───────────────────────────┐
                                                                          │  Sentinel SRE Persona     │
                                                                          │  - Linux sysfs mitigation │
                                                                          │  - GPIO fan trigger       │
                                                                          │  - Cache drop directives  │
                                                                          └───────────────────────────┘
```

### The Closed-Loop Flow:
1. **Detection**: `sovereign-rpi-telemetry` detects hardware anomalies (e.g. thermal trip at 86.4°C or physical RAM at 94.2%).
2. **Cascaded Dispatch**: Solution 01's n8n workflow routes the anomaly event directly to Solution 02's inbound webhook (`POST http://127.0.0.1:5678/webhook/avatar-agents`).
3. **AI Persona Diagnosis**: The `SentinelSRE` avatar agent analyzes root cause and synthesizes exact Linux kernel commands (`scaling_governor=powersave`, GPIO 18 fan trigger, `/proc/sys/vm/drop_caches`).
4. **Audit Immutability**: The remediation directive is published to the SBB Vault REST Bridge (`http://127.0.0.1:8766/api/webhook/audit`) and persisted in `facility_telemetry_v2.db`.
5. **Bidirectional Inspection**: Solution 02 can also query Solution 01 on demand via `GET http://127.0.0.1:8785/api/v1/edge-vitals` to inspect edge vitals and assess system stability.

---

## 2. Active AI Persona Matrices

| Persona | Role | Core Expertise | System Behavior |
| :--- | :--- | :--- | :--- |
| **`SentinelSRE`** | Edge Infrastructure & Hardware SRE | Linux sysfs, Thermal Throttling, cgroups, GPIO | Low-temperature (0.2), deterministic hardware mitigation and incident playbooks |
| **`ChefPro`** | Executive Culinary Director & Kitchen AI | Recipe Scaling, HACCP Compliance, Food Cost Margins | High-temperature (0.7), recipe formulations, commercial kitchen workflows |
| **`NovaPro`** | Principal Systems Architect | Distributed Systems, Clean Architecture, REST Contracts | Medium-temperature (0.4), API design, idempotency validation |
| **`FacilitySentinel`**| Thermodynamic Operations Lead | Industrial HVAC, Sensor Telemetry, Power Microgrids | Analytical (0.3), ASHRAE compliance, building management vitals |

---

## 3. Installation & Quickstart

```bash
# Clone repository
git clone https://github.com/BlackFoxgamingstudio/sovereign-avatar-agents.git
cd sovereign-avatar-agents

# Install in editable mode (Zero external dependencies)
pip install -e .

# Verify health status via CLI
python3 src/cli.py --health
```

---

## 4. CLI Usage Reference

```bash
# Check service health
python3 src/cli.py --health

# List all registered personas
python3 src/cli.py --list-personas

# Chat with SentinelSRE
python3 src/cli.py --persona SentinelSRE --chat "What are the failover procedures when CPU temperature trips 82C?"

# Chat with ChefPro
python3 src/cli.py --persona ChefPro --chat "How do we balance cold-holding HACCP compliance during dinner rush?"

# Run automated incident diagnosis on a thermal spike
python3 src/cli.py --diagnose-incident

# Query live edge vitals from sovereign-rpi-telemetry (Port 8770)
python3 src/cli.py --inspect-edge --edge-url http://127.0.0.1:8770
```

---

## 5. REST API & Webhook Microservice Reference (Port 8785)

The standalone microservice daemon listens on port **8785**:

```bash
python3 n8n/webhook_adapter.py
```

### Endpoints:
- `GET /health` or `GET /healthz`: Service status, loaded personas, uptime.
- `GET /api/v1/personas`: Full catalog of persona definitions, system prompts, and expertise tags.
- `GET /api/v1/edge-vitals`: Queries live telemetry from Solution 01 (`http://127.0.0.1:8770/telemetry/health`) and synthesizes an AI assessment.
- `POST /api/v1/diagnose-incident`: Ingests an incident payload and emits an `IncidentDiagnosis` with root cause and remediation commands.
- `POST /api/v1/chat`: Executes an episodic dialogue turn with a persona (`{"persona": "SentinelSRE", "message": "..."}`).
- `POST /api/v1/execute`: Deterministic feature dispatcher with SHA-256 idempotency token generation.

---

## 6. n8n Automation & Verification Steps

### Pre-Configured Access Credentials:
- **n8n Web UI**: `http://127.0.0.1:5678`
- **Email / Username**: `russell@sovereignbizbox.io`
- **Password**: `SovereignBizBox2026!`
- **Workspace**: `Sovereign Biz Box Command Center`

### Active Live Workflows:
1. **Solution 01**: `SBB Solution 01: Raspberry Pi IoT Telemetry & Alert Dispatcher` (ID: `y4yX2pvYKTgDeu6o`)
2. **Solution 02**: `SBB Solution 02: Sovereign AI Avatar Agents & SRE Autonomous Healer` (ID: `k9xW1mZ8Qp2Vb4L0`)

### Verification Commands:

```bash
# 1. Test Solution 02 chat webhook via n8n
curl -X POST http://127.0.0.1:5678/webhook/avatar-agents \
  -H "Content-Type: application/json" \
  -d '{"persona": "SentinelSRE", "message": "Confirm edge telemetry connection"}'

# 2. Trigger cross-solution incident cascade (Solution 01 -> Solution 02)
curl -X POST http://127.0.0.1:5678/webhook/rpi-telemetry \
  -H "Content-Type: application/json" \
  -d '{"thermal_spike": true}'

# 3. Verify audit record in facility_telemetry_v2.db
python3 -c "import sqlite3; conn = sqlite3.connect('databases/facility_telemetry_v2.db'); cursor = conn.cursor(); cursor.execute('SELECT id, event_name, source, details FROM n8n_automation_telemetry ORDER BY id DESC LIMIT 2'); print(cursor.fetchall())"
```

---

## 7. Automated Test Suite

This repository includes a 100% passing test suite runnable via `pytest` or `python3` (zero dependencies):

```bash
# Run tests with pytest
pytest tests/test_solution.py -v

# Run tests directly with Python standard library
python3 tests/test_solution.py
```

### Test Coverage (10/10 Passed):
1. `test_01_engine_initialization_and_health`: Validates microservice health check and domain metadata.
2. `test_02_persona_catalog_integrity`: Ensures all persona matrices have system prompts and expertise tags.
3. `test_03_thermal_incident_diagnosis`: Verifies thermal runaway generates Linux kernel `powersave` and GPIO fan directives.
4. `test_04_memory_incident_diagnosis`: Verifies high RAM triggers `/proc/sys/vm/drop_caches`.
5. `test_05_optimal_telemetry_diagnosis`: Validates optimal baseline telemetry assessment.
6. `test_06_episodic_dialogue_memory`: Verifies conversational state accumulation across dialogue turns.
7. `test_07_idempotent_feature_execution`: Confirms consistent SHA-256 idempotency token generation.
8. `test_08_cli_execution`: Subprocess integration test of CLI entrypoint.
9. `test_09_storage_critical_diagnosis`: Verifies root volume critical triggers journalctl vacuum and Docker pruning.
10. `test_10_cross_solution_query_fallback`: Validates deterministic fallback during edge communication interruptions.

---

## 8. Principal Engineer Technical Defense

> **60-Second Interview Pitch**:
> "Sovereign Avatar Agents proves how autonomous AI personas can operate beyond simple chat widgets. By coupling specialized personas with real-time IoT telemetry pipelines, SentinelSRE autonomously monitors edge nodes, diagnoses thermal runaways, and dispatches precise kernel-level remediation commands before hardware damage occurs—all while preserving audit immutability in an SQLite ledger through n8n orchestration."
