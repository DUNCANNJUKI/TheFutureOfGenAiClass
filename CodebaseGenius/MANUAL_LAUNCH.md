# Manual System Launch Guide

If the automatic launcher doesn't work, follow these manual steps to get the system running.

---

## Step 1: Setup Virtual Environment

### Windows
```powershell
cd CodebaseGenius\BE
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS/Linux
```bash
cd CodebaseGenius/BE
python3 -m venv venv
source venv/bin/activate
```

---

## Step 2: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install core dependencies
pip install fastapi uvicorn pydantic

# If above fails, try with explicit index
pip install --index-url https://pypi.org/simple/ fastapi uvicorn pydantic

# If still having issues, unset problematic env vars first:
# Windows (PowerShell):
$env:SSL_CERT_FILE = ""
$env:REQUESTS_CA_BUNDLE = ""
$env:CURL_CA_BUNDLE = ""
$env:PIP_CERT = ""

# Then retry pip install
pip install fastapi uvicorn pydantic
```

---

## Step 3: Start Backend Server

### Windows
```powershell
cd CodebaseGenius\BE
.\venv\Scripts\Activate.ps1
python -m uvicorn server_v2:app --host 0.0.0.0 --port 8001 --reload
```

### macOS/Linux
```bash
cd CodebaseGenius/BE
source venv/bin/activate
python -m uvicorn server_v2:app --host 0.0.0.0 --port 8001 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

---

## Step 4: In a NEW Terminal - Start Frontend

### Windows
```powershell
cd CodebaseGenius\FE
..\BE\venv\Scripts\Activate.ps1
pip install streamlit  # If not installed
streamlit run code_master_v2.py --server.port 8502
```

### macOS/Linux
```bash
cd CodebaseGenius/FE
source ../BE/venv/bin/activate
pip install streamlit  # If not installed
streamlit run code_master_v2.py --server.port 8502
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8502
```

---

## Step 5: Open Browser

Visit: **http://localhost:8502**

The Code Master interface should load. You're ready to analyze repositories!

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Ensure you're in the virtual environment
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install --upgrade pip
pip install fastapi uvicorn pydantic streamlit
```

### "Port 8001 already in use"

**Windows:**
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -i :8001
kill -9 <PID>
```

### "Error loading ASGI app"

**Solution:**
```bash
# Verify server file syntax
python -m py_compile server_v2.py

# Try running directly
python server_v2.py

# Or use server_simple as fallback
python -m uvicorn server_simple:app --host 0.0.0.0 --port 8001
```

### SSL/TLS Certificate Error

**Solution:**
```bash
# Unset problematic environment variables
# Windows (PowerShell):
$env:SSL_CERT_FILE = ""
$env:REQUESTS_CA_BUNDLE = ""
$env:CURL_CA_BUNDLE = ""
$env:PIP_CERT = ""

# macOS/Linux (Bash):
unset SSL_CERT_FILE
unset REQUESTS_CA_BUNDLE
unset CURL_CA_BUNDLE
unset PIP_CERT

# Then retry pip install
pip install fastapi uvicorn pydantic
```

### Streamlit not found

```bash
pip install streamlit
```

---

## Quick Reference

### System Ports
- Backend: **8001** (http://localhost:8001)
- Frontend: **8502** (http://localhost:8502)
- API Docs: **8001/docs** (http://localhost:8001/docs)

### Key Files
- Backend: `CodebaseGenius/BE/server_v2.py` or `server_simple.py`
- Frontend: `CodebaseGenius/FE/code_master_v2.py`
- Config: `CodebaseGenius/BE/requirements.txt`

### Virtual Environment
- **Location:** `CodebaseGenius/BE/venv/`
- **Activate (Windows):** `.\venv\Scripts\Activate.ps1`
- **Activate (macOS/Linux):** `source venv/bin/activate`
- **Deactivate:** `deactivate`

---

## System is Running!

Once both terminal windows show "startup complete" messages:
- Open browser to http://localhost:8502
- Enter a GitHub repository URL
- Click "Analyze"
- Explore the results!

---

*Code Master v2.0 | November 2025*
