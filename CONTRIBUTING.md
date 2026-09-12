# Contributing to Sovereign Avatar Agents (`sovereign-avatar-agents`)

Thank you for your interest in contributing to `sovereign-avatar-agents`! We welcome contributions from developers worldwide.

---

## 1. Development Standards & Philosophy

1. **Zero Mandatory Runtime Dependencies**: The core persona engine and microservice must remain executable using only the Python standard library.
2. **Deterministic Idempotency**: All feature executions must generate SHA-256 tokens from canonical JSON payloads to prevent duplicate side effects.
3. **Episodic Memory Management**: Conversational state must be tracked cleanly per session ID without leaking memory across requests.
4. **100% Test Coverage**: All bug fixes and features must include unit and integration tests passing via both `pytest` and pure `python3 tests/test_solution.py`.

---

## 2. Setting Up Your Development Environment

```bash
# 1. Fork & clone the repository
git clone https://github.com/BlackFoxgamingstudio/sovereign-avatar-agents.git
cd sovereign-avatar-agents

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in editable development mode
pip install -e .

# 4. Run tests
pytest tests/test_solution.py -v
```

---

## 3. Pull Request Process

1. Create a feature branch from `main`: `git checkout -b feat/my-new-persona`.
2. Follow Conventional Commits format (`feat:`, `fix:`, `docs:`, `refactor:`, `ci:`).
3. Ensure all tests pass locally across Python 3.10+.
4. Submit your PR using the provided pull request template.
