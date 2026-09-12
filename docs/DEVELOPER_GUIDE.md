# Developer Guide: Sovereign Avatar Agents (`sovereign-avatar-agents`)

Welcome to the developer manual for `sovereign-avatar-agents` (`PKG-007`). This guide explains how to develop, test, configure, and extend AI persona microservices within the Sovereign Biz Box ecosystem.

---

## 1. Quickstart & Local Setup

### Prerequisites
- Python 3.10+ (Standard library only; zero mandatory third-party dependencies)
- Git
- Optional: Docker & Docker Compose
- Optional: n8n 1.0+ for visual event orchestration

### Installation
```bash
# Clone the repository
git clone https://github.com/BlackFoxgamingstudio/sovereign-avatar-agents.git
cd sovereign-avatar-agents

# Copy environment configuration template
cp .env.example .env

# Install in editable development mode
pip install -e .

# Run test suite
pytest tests/test_solution.py -v
```

---

## 2. Variables & Configuration Matrix

| Variable Name | Default | Type | Description |
| :--- | :--- | :--- | :--- |
| `SBB_AVATAR_PORT` | `8785` | Integer | Microservice HTTP listener port |
| `SBB_AVATAR_HOST` | `0.0.0.0` | String | Network interface binding address |
| `SBB_ENVIRONMENT` | `development` | String | Environment tier (`development`, `staging`, `production`) |
| `SBB_DEFAULT_AI_PERSONA`| `SentinelSRE`| String | Default fallback persona for interactive sessions |
| `SBB_AI_TEMPERATURE` | `0.2` | Float | Default synthesis temperature |
| `SBB_MAX_MEMORY_TURNS` | `50` | Integer | Maximum episodic dialogue buffer turns |
| `SBB_RPI_TELEMETRY_URL` | `http://127.0.0.1:8770` | String | Live edge sensor daemon endpoint |
| `SBB_VAULT_BRIDGE_URL` | `http://127.0.0.1:8766` | String | SBB Vault Bridge REST endpoint for audit events |
| `SBB_N8N_BASE_URL` | `http://127.0.0.1:5678` | String | n8n workflow engine base URL |
| `SBB_AUTONOMOUS_HEALING_ENABLED` | `true` | Boolean | Enables automatic remediation directives |

---

## 3. How to Extend: Registering a New AI Persona

The persona engine in `src/core.py` is configured via `PersonaProfile` dataclasses.

### Step-by-Step Tutorial: Adding a Security & Cryptography Persona (`CipherSentinel`)
1. Open `src/core.py`.
2. Locate the `_load_default_personas()` method.
3. Add the new persona definition:
```python
"CipherSentinel": PersonaProfile(
    id="persona-security-005",
    name="Cipher Sentinel",
    role="Zero-Trust Security & Cryptographic Key Operations Lead",
    description="Specialized in TLS certificates, SSH bastion auditing, and token rotation.",
    system_prompt="You are Cipher Sentinel, a zero-trust infrastructure security architect. You verify certificate expiry, audit open ports, and enforce least-privilege cgroup policies.",
    expertise=["Zero Trust", "mTLS", "cgroups", "Linux Capabilities", "SSH Auditing"],
    temperature=0.1
)
```
4. Add persona-specific response dispatching in `chat_turn()`.
5. Run the test suite:
```bash
pytest tests/test_solution.py -v
```

---

## 4. REST API Reference (Port 8785)

### `GET /health` / `GET /healthz`
Returns microservice health and loaded personas.
```json
{
  "status": "HEALTHY",
  "service": "sovereign-avatar-agents",
  "domain": "AI Persona Microservices",
  "personas_loaded": 4,
  "active_personas": ["SentinelSRE", "ChefPro", "NovaPro", "FacilitySentinel"]
}
```

### `GET /api/v1/personas`
Returns complete catalog of persona matrices and expertise tags.

### `GET /api/v1/edge-vitals`
Queries live telemetry from Solution 01 (`:8770`) and generates real-time AI diagnosis.

### `POST /api/v1/diagnose-incident`
Input:
```json
{
  "node_id": "edge-01",
  "hardware": {"cpu_temp_celsius": 86.4, "ram_usage_percent": 94.2},
  "alerts": [{"code": "ERR_THERMAL_RUNAWAY", "severity": "CRITICAL"}]
}
```
Output:
```json
{
  "status": "SUCCESS",
  "diagnosis": {
    "incident_id": "INC-c3d4ff8983b9",
    "severity": "CRITICAL",
    "persona_responder": "SentinelSRE",
    "root_cause": "CPU Junction temperature (86.4°C) exceeds thermal trip limit (82.0°C)...",
    "remediation_directives": [
      "echo 'powersave' | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor",
      "gpio -g write 18 1  # Trigger auxiliary cooling fan",
      "sync; echo 3 | sudo tee /proc/sys/vm/drop_caches"
    ]
  }
}
```

### `POST /api/v1/chat`
Stateful conversational turn:
```json
{
  "persona": "SentinelSRE",
  "message": "Explain the failover policy for CPU spikes",
  "session_id": "dev_session_01"
}
```

---

## 5. Deployment Options

### Option A: Standalone Python Microservice
```bash
python3 n8n/webhook_adapter.py
```

### Option B: Linux systemd Service
```bash
sudo cp templates/systemd/sbb-avatar-agents.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sbb-avatar-agents
```

### Option C: Docker Compose
```bash
docker compose up -d
```
