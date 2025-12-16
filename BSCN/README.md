# B-Smart Career Navigator (BSCN)

Lightweight graph-first career recommendation scaffold. Built with deterministic Python walkers (JAC-compatible) and a FastAPI orchestrator plus a Streamlit frontend for demos.

Quick start (recommended)

1. Create/activate the virtual environment `venv_bscn` in the `BSCN` folder and install requirements:

```powershell
cd "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\BSCN"
python -m venv venv_bscn
.\venv_bscn\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m pip install -r frontend\requirements.txt
```

2. Use the launcher to start backend and frontend (creates two windows and opens the browser):

```powershell
call START_BSMART.bat
```

3. Open `http://127.0.0.1:8502` in your browser if it does not open automatically.

Notes
- The frontend calls `/extract` to convert free text into structured JSON, and `/recommend` to run deterministic graph walkers and return a strict recommendation JSON.
- Sensitive system prompts are moved to `secure/` and not tracked.

If anything fails, check the backend logs (uvicorn window) for errors and ensure `venv_bscn` is activated before installing packages.

Development
- Core orchestrator: `backend/app.py`
- Extractor: `backend/llm_extract.py`
- Deterministic walkers and graph: `backend/walkers.py`, `backend/sample_graph.py`
- Frontend: `frontend/streamlit_app.py`

If you want the spaCy NER model, install it into `venv_bscn`:

```powershell
.\venv_bscn\Scripts\Activate.ps1
python -m pip install spacy
python -m spacy download en_core_web_sm
```
