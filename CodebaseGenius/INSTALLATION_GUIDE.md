# Code Master v2.0 - Installation & Setup Guide

**Version:** 2.0.0  
**Last Updated:** 2024  
**Status:** ✅ Production Ready

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (Recommended)](#quick-start-recommended)
3. [Manual Installation](#manual-installation)
4. [Verification & Testing](#verification--testing)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Configuration](#advanced-configuration)

---

## System Requirements

### Hardware
- **CPU:** Modern processor (2+ cores recommended)
- **RAM:** 4GB minimum, 8GB+ recommended
- **Disk Space:** 2GB free space (1GB for system, 1GB for analysis cache)
- **Internet:** Required (for GitHub access)

### Software

#### Windows
- ✓ Windows 7/8/10/11
- ✓ PowerShell 5.0+ (comes with Windows)
- ✓ Python 3.10+ (installation instructions below)

#### macOS
- ✓ macOS 10.13+
- ✓ Zsh or Bash shell
- ✓ Python 3.10+ (via Homebrew)

#### Linux
- ✓ Ubuntu 18.04+, Debian 10+, Fedora 30+, etc.
- ✓ Bash shell
- ✓ Python 3.10+ (apt/yum/pacman)

---

## Quick Start (Recommended)

### Windows Users

#### Step 1: Download/Clone Repository

**Option A: Git Clone (Recommended)**
```powershell
git clone https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass.git
cd TheFutureOfGenAiClass\CodebaseGenius
```

**Option B: Download ZIP**
1. Visit GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Open PowerShell in `CodebaseGenius` folder

#### Step 2: Run the Launcher

**Method 1: Double-Click (Easiest)**
1. Navigate to `CodebaseGenius` folder
2. Find `START_SYSTEM_V2.bat`
3. **Double-click it**
4. Wait 10-15 seconds
5. Browser opens automatically to `http://localhost:8502`

**Method 2: Command Line**
```powershell
cd CodebaseGenius
.\START_SYSTEM_V2.bat
```

#### Step 3: Use the Application

1. **Enter Repository URL**
   - Example: `https://github.com/torvalds/linux`
   - Click "Analyze Repository"

2. **Wait for Analysis**
   - Progress shown in real-time
   - Typically 5-30 seconds

3. **Explore Results**
   - View documentation
   - Ask chatbot questions
   - Check APIs & dependencies
   - Download reports

### macOS Users

#### Step 1: Install Python

```bash
# If using Homebrew
brew install python3.10

# Verify
python3 --version  # Should show 3.10+
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass.git
cd TheFutureOfGenAiClass/CodebaseGenius
```

#### Step 3: Create Startup Script

```bash
cat > START_SYSTEM_V2.sh << 'EOF'
#!/bin/bash

# Set colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Code Master v2.0 - System Launcher   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"

# Check Python
echo "[*] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found!"
    echo "Install via: brew install python3"
    exit 1
fi

# Create venv
if [ ! -d "BE/venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv BE/venv
fi

# Activate and install
echo "[*] Activating virtual environment..."
source BE/venv/bin/activate

echo "[*] Installing dependencies..."
pip install -q fastapi uvicorn requests streamlit

# Start backend
echo "[*] Starting backend..."
cd BE
python3 -m uvicorn server_v2:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend
echo "[*] Starting frontend..."
cd FE
python3 -m streamlit run code_master_v2.py --server.port 8502 &
FRONTEND_PID=$!
cd ..

sleep 2

# Open browser
echo "[*] Opening browser..."
open http://localhost:8502

echo -e "${GREEN}✓ System started successfully!${NC}"
echo "Frontend: http://localhost:8502"
echo "Backend: http://localhost:8001"
echo "Press Ctrl+C to stop all services"

wait
EOF

chmod +x START_SYSTEM_V2.sh
```

#### Step 4: Run

```bash
./START_SYSTEM_V2.sh
```

### Linux Users

#### Step 1: Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.10 python3-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.10 python3-pip
```

**Arch:**
```bash
sudo pacman -S python
```

#### Step 2: Clone & Setup

```bash
git clone https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass.git
cd TheFutureOfGenAiClass/CodebaseGenius
```

#### Step 3: Create and Run Script

```bash
chmod +x START_SYSTEM_V2.sh
./START_SYSTEM_V2.sh
```

(Same script as macOS in Step 3)

---

## Manual Installation

### For Advanced Users

If the automatic script doesn't work or you prefer manual setup:

#### Step 1: Create Virtual Environment

**Windows:**
```powershell
cd CodebaseGenius\BE
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
cd CodebaseGenius/BE
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Start Backend

**Windows:**
```powershell
python -m uvicorn server_v2:app --host 0.0.0.0 --port 8001
```

**macOS/Linux:**
```bash
python3 -m uvicorn server_v2:app --host 0.0.0.0 --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

#### Step 4: In New Terminal - Start Frontend

**Navigate to FE folder:**

**Windows:**
```powershell
cd ..\FE
..\BE\venv\Scripts\Activate.ps1
streamlit run code_master_v2.py --server.port 8502
```

**macOS/Linux:**
```bash
cd ../FE
source ../BE/venv/bin/activate
streamlit run code_master_v2.py --server.port 8502
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8502
```

#### Step 5: Open Browser

Visit: `http://localhost:8502`

---

## Verification & Testing

### Verify Backend is Running

**In browser or curl:**
```bash
curl http://localhost:8001/health

# Should return:
# {"status":"healthy","timestamp":"2024-11-14T..."}
```

### Verify Frontend is Running

Visit: `http://localhost:8502`

Should see:
- Code Master logo
- Input field for repository URL
- Feature cards
- Tab navigation

### Test Full Pipeline

1. **Enter test repository:**
   ```
   https://github.com/torvalds/linux
   ```

2. **Click "Analyze"**
   - Wait 10-30 seconds
   - See progress messages

3. **View results:**
   - Check Documentation tab
   - Try asking chatbot: "What's the main purpose?"
   - View APIs tab
   - Try downloading as HTML

4. **Verify features:**
   - ✓ Chatbot responds
   - ✓ APIs listed
   - ✓ Download works
   - ✓ Multiple tabs work

### Check Port Availability

**Windows:**
```powershell
netstat -ano | findstr :8001
netstat -ano | findstr :8502
```

**macOS/Linux:**
```bash
lsof -i :8001
lsof -i :8502
```

If ports show in use:
```powershell
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

---

## Troubleshooting

### Problem: "Python not found"

**Solution:**
```powershell
# Verify Python installation
python --version

# Should show: Python 3.10.x or higher

# If not installed:
# Download from https://www.python.org/
# Make sure to check "Add Python to PATH"
```

### Problem: "Port 8001 already in use"

**Windows:**
```powershell
# Find what's using the port
netstat -ano | findstr :8001

# Kill the process
taskkill /PID <PID> /F

# Try again
START_SYSTEM_V2.bat
```

**macOS/Linux:**
```bash
lsof -i :8001
kill -9 <PID>
```

### Problem: "ModuleNotFoundError"

**Solution:**
```bash
cd CodebaseGenius/BE

# Activate venv
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### Problem: "Connection refused" (8001)

**Solution:**
1. Check backend window - see any errors?
2. Make sure it's running on port 8001
3. Try manually starting backend:
   ```bash
   cd CodebaseGenius/BE
   python -m uvicorn server_v2:app --host 0.0.0.0 --port 8001
   ```
4. Check for firewall blocking

### Problem: "Streamlit not found"

**Solution:**
```bash
pip install streamlit==1.51.0
```

### Problem: "Browser didn't auto-open"

**Solution:**
1. Manually open: `http://localhost:8502`
2. Try different browser
3. Check if popup was blocked
4. Restart system and try again

### Problem: "Analysis hangs or is very slow"

**Solutions:**
1. Check internet connection (needs GitHub access)
2. Try smaller repository first
3. Check backend window for errors
4. Increase timeout in advanced settings
5. Check system resources (RAM, CPU, disk)

### Problem: "Error downloading file"

**Solution:**
1. Check internet connection
2. Verify repository URL is valid
3. Try analyzing different repo
4. Check browser download settings
5. Try different export format

---

## Advanced Configuration

### Environment Variables

Create `CodebaseGenius/.env` file:

```bash
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001
BACKEND_RELOAD=true

# Frontend Configuration
FRONTEND_PORT=8502

# Analysis Settings
MAX_FILES=100
MAX_FILE_SIZE_MB=5

# Optional: LLM Configuration (for enhanced features)
OPENAI_API_KEY=sk_...
GEMINI_API_KEY=...
```

### Modify Port Numbers

**Backend (different port):**
```bash
python -m uvicorn server_v2:app --port 8001
```

**Frontend (different port):**
```bash
streamlit run code_master_v2.py --server.port 8502
```

### Enable Debug Mode

**Backend:**
```bash
# Already has logging enabled
# Check console output
```

**Frontend:**
```bash
streamlit run code_master_v2.py --logger.level=debug
```

### Configure Logging

Add to `BE/server_v2.py`:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Use Different Python Environment

**Conda users:**
```bash
conda create -n codemaster python=3.10
conda activate codemaster
pip install -r requirements.txt
```

**Poetry users:**
```bash
poetry install
poetry run python -m uvicorn server_v2:app --port 8001
```

---

## Performance Tuning

### Improve Speed

1. **Increase max files carefully:**
   ```python
   # In analysis settings
   max_files = 200  # Default: 100
   ```

2. **Use caching:**
   - System auto-caches recent analyses
   - Repeated analysis of same repo is instant

3. **Optimize system:**
   - Close other applications
   - Ensure good internet connection
   - Use SSD for temp files

### Reduce Memory Usage

1. **Limit concurrent analyses:**
   ```bash
   # Process one at a time
   ```

2. **Smaller max file size:**
   ```bash
   MAX_FILE_SIZE_MB=1  # Default: 5
   ```

3. **Clear cache periodically:**
   - Restart application
   - Automatic cleanup on shutdown

---

## Docker Setup (Optional)

For containerized deployment:

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001 8502

CMD ["bash", "-c", "python -m uvicorn server_v2:app --host 0.0.0.0 --port 8001 & streamlit run code_master_v2.py --server.port 8502"]
```

Build and run:
```bash
docker build -t codemaster:v2 .
docker run -p 8001:8001 -p 8502:8502 codemaster:v2
```

---

## Getting Help

| Issue | Resource |
|-------|----------|
| Installation | [README.md](./README.md) |
| Features | [FEATURES_V2.md](./FEATURES_V2.md) |
| API Usage | [API_REFERENCE.md](./API_REFERENCE.md) |
| Troubleshooting | [Troubleshooting Section](#troubleshooting) |
| Report Bug | [GitHub Issues](https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass/issues) |
| Ask Question | [GitHub Discussions](https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass/discussions) |

---

## Next Steps

After successful installation:

1. ✅ Run through [Quick Test](#verification--testing)
2. ✅ Read [FEATURES_V2.md](./FEATURES_V2.md)
3. ✅ Try analyzing your own repository
4. ✅ Explore chatbot features
5. ✅ Download documentation in different formats
6. ✅ Share feedback

---

## Uninstallation

### Windows

```powershell
# Stop services (close terminal windows)
# Navigate to installation folder
cd CodebaseGenius
Remove-Item -Recurse -Force BE\venv
Remove-Item -Recurse -Force FE\venv
```

### macOS/Linux

```bash
cd CodebaseGenius
rm -rf BE/venv
rm -rf FE/venv
```

---

**Made with ❤️ by Duncan N. for Developers (2024-2026)**

*For the latest version and updates, visit: https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass*
