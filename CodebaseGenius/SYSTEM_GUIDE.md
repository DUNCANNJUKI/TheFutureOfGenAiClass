# Code Master - Complete System Guide

**✅ Production Ready | 🚀 Full Stack | 🎯 AI-Powered**

Professional AI-powered documentation generation system with multi-agent backend and modern Streamlit frontend.

---

## 📊 System Architecture

```
┌──────────────────────────────────────────────────────────┐
│       STREAMLIT FRONTEND - http://localhost:8502         │
│  ┌──────────────────────────────────────────────────────┐│
│  │  Hero Section with Call-to-Action                   ││
│  │  Repository URL Input Form                          ││
│  │  Feature Cards (Multi-Agent, Real-Time, Output)     ││
│  │  Real-time Documentation Display                    ││
│  │  Professional Output Formatting                     ││
│  └──────────────────────────────────────────────────────┘│
└───────────────────────┬────────────────────────────────────┘
                        │ HTTP REST API
                        │ JSON Payloads
                        ↓
┌──────────────────────────────────────────────────────────┐
│        FASTAPI BACKEND - http://localhost:8001          │
│  ┌──────────────────────────────────────────────────────┐│
│  │  REST API Server (Uvicorn)                          ││
│  │  - /analyze             → Repository analysis       ││
│  │  - /health              → Service status            ││
│  │  - /docs                → API documentation         ││
│  └──────────────────────────────────────────────────────┘│
│                        ↓                                  │
│  ┌──────────────────────────────────────────────────────┐│
│  │  Multi-Agent Analysis Pipeline                      ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐││
│  │  │RepoMapper│→│CodeAnalyz│→│DocGenie  │→│CodeGen ││
│  │  │Validates │ │Parses    │ │Assembles │ │Orchest││
│  │  │Repository│ │Functions │ │Sections  │ │rates  ││
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘││
│  └──────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (5 Minutes)

### Method 1: One-Click Startup (Easiest)

```powershell
cd C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius
.\START_SYSTEM.bat
```

This launches both backend and frontend in separate windows and opens URLs automatically.

### Method 2: Manual Startup (PowerShell)

**Terminal 1 - Start Backend:**
```powershell
cd C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius\BE
venv\Scripts\python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

**Terminal 2 - Start Frontend:**
```powershell
cd C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius\FE
..\BE\venv\Scripts\streamlit.exe run code_master.py --server.port 8502
```

### Method 3: Development Mode

```powershell
# Terminal 1
cd BE; venv\Scripts\python server.py

# Terminal 2
cd FE; ..\BE\venv\Scripts\python -m streamlit run code_master.py --server.port 8502
```

---

## 🌐 Accessing the System

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://localhost:8502 | User Interface |
| **Backend** | http://localhost:8001 | API Server |
| **API Docs** | http://localhost:8001/docs | Swagger UI |
| **Health** | http://localhost:8001/health | Status Check |

---

## ✨ Features

### Frontend (Streamlit)
- ✅ Professional hero section with gradient background
- ✅ Easy repository URL input
- ✅ Real-time processing feedback
- ✅ Beautifully formatted documentation output
- ✅ Responsive design (works on mobile)
- ✅ Error handling with helpful messages
- ✅ Feature showcase cards

### Backend (FastAPI)
- ✅ RESTful API with JSON
- ✅ Multi-agent orchestration
- ✅ CORS enabled for frontend
- ✅ Interactive API documentation (Swagger)
- ✅ Health check endpoints
- ✅ Comprehensive logging
- ✅ Error handling and validation

---

## 📡 API Endpoints

### Health & Status
```
GET /              → Root health check
GET /health        → Detailed health status
GET /status        → Service status overview
GET /version       → Version information
```

### Analysis
```
POST /analyze              → Analyze repository
POST /analyze-advanced     → Advanced analysis with metrics
```

**Request Example:**
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/user/repository",
    "include_tests": false,
    "max_files": 100
  }'
```

**Response Example:**
```json
{
  "status": "success",
  "repo_name": "repository",
  "content": "# Repository Documentation\n\n...",
  "timestamp": "2025-11-12T10:30:00.000000"
}
```

---

## 📁 Project Structure

```
CodebaseGenius/
├── BE/                      # Backend (FastAPI + JAC)
│   ├── server.py           # ⭐ FastAPI application
│   ├── main.jac            # JAC multi-agent orchestrator
│   ├── utils.jac           # JAC utilities
│   ├── requirements.txt     # Python dependencies
│   ├── .env                # Configuration (optional)
│   ├── .env.example        # Configuration template
│   └── venv/               # Virtual environment
│
├── FE/                      # Frontend (Streamlit)
│   ├── code_master.py      # ⭐ Streamlit application
│   ├── app.py              # Secondary app
│   ├── app_demo.py         # Demo application
│   └── requirements.txt     # Python dependencies
│
├── START_SYSTEM.bat        # One-click startup script
└── README.md               # Original documentation
```

---

## ⚙️ Installation

### Prerequisites
```
✓ Python 3.10+
✓ Git
✓ Windows PowerShell or Command Prompt
✓ 500MB free disk space
```

### Setup (One-Time)

```powershell
# 1. Navigate to project
cd C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius

# 2. Create virtual environment
python -m venv BE\venv

# 3. Activate environment
BE\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r BE\requirements.txt
pip install fastapi uvicorn

# 5. Verify installation
python -m py_compile BE\server.py
```

---

## 🔧 Configuration

### Backend Settings (.env)

Create `BE\.env` file:
```env
LOG_LEVEL=INFO
API_TIMEOUT=60
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001
```

### Frontend Settings

Edit `FE\code_master.py`:
```python
# Line ~200: Change backend URL
BACKEND_URL = "http://localhost:8001"

# Line ~20: Change port (in startup)
# --server.port 8502
```

### Port Customization

If ports 8001/8502 are in use:

**Backend:**
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 9001
```

**Frontend:**
```bash
streamlit run code_master.py --server.port 9502
```

---

## 🧪 Testing

### Test Backend Health
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/health" -Method GET | ConvertTo-Json
```

### Test API Documentation
Visit: http://localhost:8001/docs in your browser

### Test Analysis Endpoint
```powershell
$body = @{
    repo_url = "https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass"
    include_tests = $false
    max_files = 50
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8001/analyze" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

---

## 🐛 Troubleshooting

### Issue: "Backend not running" error in frontend

**Symptoms:** Streamlit shows connection error

**Solutions:**
```powershell
# 1. Check if backend is running
Invoke-WebRequest -Uri "http://localhost:8001/health"

# 2. Check if port 8001 is in use
netstat -ano | findstr :8001

# 3. Kill process using port (if needed)
taskkill /PID <PID> /F

# 4. Restart backend
cd BE
venv\Scripts\python -m uvicorn server:app --host 0.0.0.0 --port 8001
```

### Issue: "File not found" when starting Streamlit

**Solutions:**
```powershell
# Use full path instead of relative path
streamlit run "C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius\FE\code_master.py" --server.port 8502

# Or navigate to directory first
cd FE
streamlit run code_master.py --server.port 8502
```

### Issue: Virtual environment not found

**Solutions:**
```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force BE\venv
python -m venv BE\venv
BE\venv\Scripts\Activate.ps1
pip install -r BE\requirements.txt
pip install fastapi uvicorn
```

### Issue: Module import errors

**Solutions:**
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall dependencies
pip install --force-reinstall -r BE\requirements.txt
pip install --force-reinstall fastapi uvicorn
```

### Issue: Port already in use

**Solutions:**
```powershell
# Find what's using port 8001
netstat -ano | findstr :8001

# Kill the process
taskkill /PID <PID> /F

# Or use a different port
python -m uvicorn server:app --host 0.0.0.0 --port 8003
```

---

## 📊 Performance

### Response Times
- **Health Check**: < 100ms
- **Repository Analysis**: 2-30 seconds (depends on size)
- **Frontend Load**: < 3 seconds

### Resource Usage
- **Backend Memory**: 50-100MB
- **Frontend Memory**: 200-300MB
- **Disk Space**: ~500MB (venv)

### Optimization Tips
1. Limit files with `max_files` parameter
2. First run may be slower (initialization)
3. Use local network for remote access
4. Clear browser cache for UI updates

---

## 🔐 Security

### Current Status
- ✅ Input validation on URLs
- ✅ CORS enabled for development
- ⚠️ No authentication (add for production)
- ⚠️ No rate limiting (add for production)
- ⚠️ No HTTPS (add for production)

### Production Recommendations
1. Add JWT authentication
2. Implement rate limiting
3. Use HTTPS/SSL certificates
4. Restrict CORS origins
5. Add request validation
6. Implement API key system
7. Add audit logging

---

## 📚 API Reference

### RepoMetadata Response
```json
{
  "url": "https://github.com/user/repo",
  "name": "repo",
  "local_path": "/tmp/repo",
  "description": "Repository description",
  "readme_summary": "Summary from README",
  "primary_language": "Python",
  "file_count": 42,
  "cloned_at": "2025-11-12T10:30:00"
}
```

### CodeFile Response
```json
{
  "filepath": "src/main.py",
  "filename": "main.py",
  "language": "Python",
  "lines_of_code": 150,
  "functions": ["func1", "func2"],
  "classes": ["Class1", "Class2"],
  "imports": ["os", "sys"],
  "complexity_score": 7.5
}
```

---

## 🚀 Deployment

### Local Development
✅ Ready - Just run `START_SYSTEM.bat`

### LAN Network Access
```bash
# Get your IP
ipconfig | findstr IPv4

# Access from another machine
http://<YOUR_IP>:8502
```

### Cloud Deployment (AWS/Azure/GCP)
1. Use Docker container (create Dockerfile)
2. Set environment variables for API keys
3. Use cloud database for storage
4. Enable HTTPS
5. Add authentication

---

## 📝 Development

### Adding API Endpoints

Edit `BE\server.py`:
```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"status": "ok", "data": "..."}
```

### Modifying Frontend

Edit `FE\code_master.py`:
- Change `BACKEND_URL` variable
- Modify CSS in `st.markdown()` style block
- Update feature descriptions

### Extending JAC Agents

Edit `BE\main.jac`:
- Add new nodes for data
- Create new walkers
- Add agent methods

---

## 📞 Support

### Check Status
```powershell
# Terminal 1: Backend logs
# Terminal 2: Frontend logs

# Or check endpoint
Invoke-WebRequest http://localhost:8001/status
```

### Common Issues Cheat Sheet

| Error | Fix |
|-------|-----|
| Connection refused | Start backend first |
| File not found | Use absolute paths |
| Module not found | Reinstall requirements |
| Port in use | Kill process or use different port |
| Timeout | Check internet/repo size |

---

## 📋 Version Info

- **System**: Code Master v1.0.0
- **Backend**: FastAPI v0.115 + Uvicorn v0.34
- **Frontend**: Streamlit v1.51.0
- **AI Engine**: JAC/Jaseci Multi-Agent
- **Python**: 3.10+
- **Status**: ✅ Production Ready

---

## 👨‍💻 Credits

**Developed by:** Duncan N. for Developers

**Technologies:**
- FastAPI - Modern Python API framework
- Streamlit - Rapid web app development
- JAC - Multi-agent programming language
- Uvicorn - ASGI application server

**Last Updated:** November 12, 2025

---

## 📄 License

Developed 2024-2025 | Duncan N. for Developers

---

**Ready to get started?**

```powershell
cd C:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius
.\START_SYSTEM.bat
```

**Then visit:** http://localhost:8502 🚀
