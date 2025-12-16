# B-Smart Career Navigator — Scaffold

This folder contains the production system prompt, JAC walker skeletons, a deterministic Python fallback runner, and a FastAPI orchestrator for prototyping.

Key files:
- `SYSTEM_PROMPT.md` — the strict production system prompt (must be used by orchestration layer)
- `jac/ontology.jac` — node/edge declarations for the domain model (skeleton)
- `jac/walkers.jac` — JAC walkers (skeleton/translation)
- `jac/run_jac_fallback.py` — Python bridge that runs the deterministic walkers as a JAC fallback
- `jac/run_demo.py` — CLI demo to run the fallback
- `backend/` — Python backend: graph model, walkers, orchestrator (`app.py` exposes `/recommend`)
- `schema/output_schema.json` — strict JSON schema for outputs

Developer notes:
- All career logic must be implemented in JAC walkers.
- LLMs are only allowed to parse user input into JSON and to articulate explanations based on walker output.
- Ensure all scores are deterministic and numeric per the weights in `SYSTEM_PROMPT.md`.

How to run locally (quick)

Preferred (one-step launcher):

```powershell
cd "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\B-Smart Career Navigator"
call START_BSMART.bat
```

Manual (step-by-step):

```powershell
cd "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\B-Smart Career Navigator\backend"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8002
```

To run the JAC fallback demo (from project root):

```powershell
cd "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\B-Smart Career Navigator"
python -m jac.run_demo
```

Next steps:
1. Implement the `walker` bodies in real JAC code matching your runtime primitives.
2. Add richer, localized graph data (jobs, salary bands, course pricing, regional demand).
3. Add CI tests that start the orchestrator and validate outputs against `schema/output_schema.json`.
