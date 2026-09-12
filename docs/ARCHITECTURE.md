# Architecture & Systems Specification: `sovereign-avatar-agents`

## 1. Architectural Philosophy

`sovereign-avatar-agents` is designed to provide autonomous AI persona capabilities decoupled from any monolithic runtime:
1. **Multi-Matrix Persona Separation**: Each persona (`SentinelSRE`, `ChefPro`, `NovaPro`, `FacilitySentinel`) operates with independent prompt matrices, temperature targets, and domain response synthesizers.
2. **Episodic Dialogue Buffering**: Dialogue state is tracked per session with deterministic turn counts, allowing stateful conversational flow without relying on heavy external vector databases for basic operational context.
3. **Deterministic Idempotency Tokens**: Every execution calculates a canonical SHA-256 token from its input payload, ensuring duplicate webhook triggers do not cause duplicate remediation executions.

---

## 2. Closed-Loop SRE Autonomous Self-Healing Pipeline

```
[IoT Edge Node] ───────────────> [n8n Automation Engine] ───────────────> [Avatar SRE Persona]
  Hardware Spike (86.4°C)          Webhook Router (:5678)                   SentinelSRE (:8785)
                                            │                                        │
                                            │                                        ▼
                                            │                              Synthesizes Shell Directives:
                                            │                              - powersave governor
                                            │                              - GPIO 18 fan trigger
                                            │                              - page cache flush
                                            │                                        │
                                            ▼                                        ▼
                                 [SBB Vault REST Bridge (:8766)] <───────────────────┘
                                                │
                                                ▼
                                 [facility_telemetry_v2.db]
                                  Immutable Audit Log
```

---

## 3. Persona Matrix Specifications

| Persona ID | Display Name | Synthesis Temperature | Primary Failure Playbook |
| :--- | :--- | :--- | :--- |
| `persona-sre-001` | Sentinel SRE | `0.2` | Thermal Runaway & OOM Mitigation (`docs/SOP.md`) |
| `persona-culinary-002`| Chef Pro | `0.7` | HACCP Cold-Holding & Recipe Cost Modeling |
| `persona-architect-003`| Nova Pro | `0.4` | Idempotency Verification & Service Mesh Boundary |
| `persona-facility-004` | Facility Sentinel | `0.3` | HVAC Loop Balancing & Microgrid Load Shedding |
