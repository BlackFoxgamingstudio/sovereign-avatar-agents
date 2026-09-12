# Standard Operating Procedure: Sovereign Avatar Agents

## 1. Service Health Verification
Run `sovereign-avatar-agents --health` to confirm the engine responds with status `HEALTHY`.

## 2. Webhook Adapter Operation
The webhook adapter listens on port `8785`:
```bash
python3 n8n/webhook_adapter.py
```
If port 8785 is occupied, check active processes:
```bash
lsof -i :8785
```

## 3. n8n Integration Testing
Send a probe POST request:
```bash
curl -X POST http://localhost:8785/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"action": "health_ping", "payload": {"test": true}}'
```
