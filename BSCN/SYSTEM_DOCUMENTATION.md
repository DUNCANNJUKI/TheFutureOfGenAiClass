# B‑Smart Career Navigator (BSCN) — System Documentation

## Overview
- **Purpose:** BSCN is a graph‑first career recommendation prototype. It accepts a resume or free text, extracts structured profile data (id, name, skills, interests, location), and runs deterministic graph walkers to produce an explainable recommendation (recommended role, missing skills, learning plan, alternatives).
- **Design principles:** deterministic scoring (no black‑box LLM decisions), LLMs allowed only for structured extraction, strict JSON output validated against `schema/output_schema.json`.

## Components
- **Backend (FastAPI):** `backend/app.py` — exposes `/extract` and `/recommend`. Uses `backend/walkers.py`, `backend/sample_graph.py`, and `backend/llm_extract.py`.
- **Frontend (Streamlit):** `frontend/streamlit_app.py` — colorful UI, accepts `.pdf`/`.docx` uploads or pasted text, auto calls `/extract` and posts to `/recommend`.
- **JAC assets:** `jac/` folder contains ontology and walker skeletons for portability to a JAC runtime. Python walkers provide a deterministic fallback.
 - **JAC assets:** `jac/` folder contains ontology and walker skeletons for portability to a JAC runtime. Python walkers provide a deterministic fallback.
  
## JAC and byLLM integration
- Location of JAC artifacts (in the repo):
  - `BSCN/jac/ontology.jac` — domain ontology used by walker translations.
  - `BSCN/jac/walkers.jac` — human-editable walker skeletons (source for a JAC runtime).
  - `BSCN/jac/walkers_runnable.jac` — a runnable translation of the walkers for a JAC runtime.
  - `BSCN/jac/run_jac_fallback.py` — a Python bridge that runs the Python deterministic walkers as a functional equivalent of the JAC pipeline.

- How the backend uses JAC and the Python fallback:
  - The preferred production flow is to compile/translate the JAC walkers and run them with a JAC runtime. If such a runtime is available and wired into the backend, the backend can call the JAC runtime instead of the Python fallback.
  - In this repository the backend orchestrator (`BSCN/backend/app.py`) imports `backend/sample_graph.py` and `backend/walkers.py` and uses the Python walkers directly. This is intentional: it provides a deterministic, runnable fallback when a JAC runtime is not installed on the host.
  - For local testing the helper `BSCN/jac/run_jac_fallback.py` calls the same Python walkers and returns JSON conforming to `schema/output_schema.json` so that the rest of the pipeline is identical whether JAC or fallback is used.

- Where to plug a real JAC runtime:
  - Replace calls to the Python runners in `backend/app.py` (or add a runtime switch) to invoke the JAC runtime API/CLI and parse its JSON output.
  - Example integration points: `backend/app.py` (recommend orchestration) and `backend/llm_extract.py` (if you add walker-driven extraction flows).

- byLLM / LLM provider adapters and where they live:
  - Extraction is implemented in `BSCN/backend/llm_extract.py`. This module supports three modes:
    1. Provider adapter mode: when `LLM_PROVIDER` and `LLM_API_KEY` environment variables are set (e.g. `openai`, `gpt`, `claude`), the module will attempt to call the provider through a minimal, optional adapter region in `llm_extract.py` and expect a JSON-only response. This is where a byLLM adapter can be added.
    2. spaCy mode: if spaCy is installed the module uses `spacy_extract()` (PhraseMatcher + NER) for higher-precision extraction.
    3. Heuristic fallback: when no provider or spaCy model is available, `heuristic_extract()` runs lightweight pattern matching.

- How to add a byLLM adapter:
  - Implement an adapter function in `BSCN/backend/llm_extract.py` (or a separate `backend/adapters/byllm_adapter.py`) that calls the byLLM SDK/CLI, passes a careful prompt asking only for JSON (fields: `id`, `name`, `skills`, `interests`, `location`) and parses the JSON output. Set `LLM_PROVIDER=byllm` and provide `LLM_API_KEY` (if required) in your environment or `streamlit` secrets.
  - Ensure adapter calls are robust to non-JSON outputs (wrap with try/except and fall back to the heuristic) and that API keys are never committed to git.

## Notes on env vars used by extraction
- `LLM_PROVIDER` — optional; values: `openai`, `gpt`, `claude`, `byllm` (lowercase). If unset, no remote LLM is called.
- `LLM_API_KEY` — provider API key used by adapters.
- `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE` — may need unsetting if `pip` install fails due to custom CA configuration.

These additions should make it clear where the JAC assets live, how the Python fallback is used, and where a byLLM adapter would be wired in.
- **Schema:** `schema/output_schema.json` — strict JSON Schema for the recommendation output.

## Installation
1. Create a virtual environment in the `BSCN` folder and install dependencies:

```powershell
cd "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\BSCN"
python -m venv venv_bscn
.\venv_bscn\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m pip install -r frontend\requirements.txt
```

2. (Optional) For improved extraction using spaCy NER:

```powershell
.\venv_bscn\Scripts\Activate.ps1
python -m pip install spacy
python -m spacy download en_core_web_sm
```

## Running the system
- Preferred: use the launcher `START_BSMART.bat` from the `BSCN` folder. It will open two windows (backend + frontend) and open the browser to the frontend.
- Manual (for logs):

```powershell
cd "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\BSCN"
.\venv_bscn\Scripts\Activate.ps1
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8002
python -m streamlit run frontend\streamlit_app.py --server.port 8502
```

## Endpoints
- POST `/extract` — input: {
  "raw_text": "..."
}

Response example (200):

```json
{
  "id": "person:extracted",
  "name": "Duncan Njuki",
  "skills": ["python","sql","etl"],
  "interests": ["data engineering","cloud"],
  "location": "Nairobi"
}
```

- POST `/recommend` — input: the JSON returned by `/extract` (fields `id`, `name`, `skills`, `interests`, `location`)

Response example (200):

```json
{
  "recommended_role": "Data Engineer",
  "confidence_score": 0.61,
  "why_this_role": ["Role aligns with skills: python, sql, etl"],
  "missing_skills": ["cloud"],
  "learning_plan": [
    {"course_id":"course:cloud1","title":"Intro to Cloud","teaches":"cloud"}
  ],
  "time_estimate_months": 3,
  "cost_estimate": 200,
  "alternative_paths": [{"role":"Software Engineer"}]
}
```

Notes on outputs:
- All numeric scores are deterministic and reproducible given the same input and graph.
- `learning_plan` is an array of course objects with `course_id`, `title`, and `teaches` (skill id or name).

## Frontend usage
1. Open `http://127.0.0.1:8502`.
2. Paste your resume text or upload a `.pdf` / `.docx`.
3. If `Auto-extract` is enabled the frontend will call `/extract` when the text changes and populate the Extracted Profile panel.
4. Click `Run Recommendation` to call `/recommend` and view the formatted recommendation on the right.

## Expected behavior and edge cases
- If the uploaded file fails text extraction (complex PDF or encrypted DOCX), the frontend will show an error; try converting to plain text and paste.
- If spaCy model is not installed, the system falls back to `heuristic_extract` which uses pattern matching — results will be coarser but still valid JSON.
- CORS: the backend includes CORS middleware for localhost origins used by Streamlit; if you run the frontend on a different host/port, add that origin to the backend CORS allowlist.

## Troubleshooting
- TLS CA errors during `pip` install: ensure environment variables `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, or `CURL_CA_BUNDLE` are not pointing to invalid paths. Unset them before `pip install` if necessary.
- If `START_BSMART.bat` doesn't open windows, run the commands manually to inspect logs.
- If `/recommend` returns a schema validation error, inspect backend logs; the output must match `schema/output_schema.json`.

## Testing (smoke tests)
- Quick extract + recommend test (PowerShell):

```powershell
$json='{"raw_text":"Name: Duncan Njuki\nLocation: Nairobi\nSkills: Python, SQL, ETL\nInterests: data engineering, cloud"}'
Invoke-RestMethod -Uri 'http://127.0.0.1:8002/extract' -Method Post -Body $json -ContentType 'application/json' | ConvertTo-Json -Depth 5
```

If the above returns a JSON profile, then:

```powershell
$profile = Invoke-RestMethod -Uri 'http://127.0.0.1:8002/extract' -Method Post -Body $json -ContentType 'application/json'
Invoke-RestMethod -Uri 'http://127.0.0.1:8002/recommend' -Method Post -Body ($profile | ConvertTo-Json) -ContentType 'application/json' | ConvertTo-Json -Depth 5
```

## File map (key files)
- `BSCN/backend/app.py` — orchestrator, endpoints
- `BSCN/backend/llm_extract.py` — extraction bridge: spaCy optional + heuristic fallback
- `BSCN/backend/walkers.py` — deterministic graph walkers (profile analyzer, scoring, learning plan)
- `BSCN/backend/sample_graph.py` — sample graph used by fallback
- `BSCN/frontend/streamlit_app.py` — user interface (upload, extract, recommend)
- `BSCN/schema/output_schema.json` — strict schema for recommendation output
- `BSCN/jac/` — JAC ontology and walker skeletons
- `BSCN/START_BSMART.bat` — launcher

## Security & Privacy
- The system is a local prototype. Do not upload sensitive PII unless you understand retention and local file handling.
- System prompts and sensitive data are stored in `secure/` and are excluded from git.

## Credits
- Developed by Duncan Njuki, GenAI student, Open University of Kenya (OUK).

---
*If you want, I can also generate a compact API reference file, add example cURL calls, or publish this documentation to a `docs/` folder.*
