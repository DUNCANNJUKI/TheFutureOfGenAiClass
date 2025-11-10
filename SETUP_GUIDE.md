# The Code Master - System Setup & Installation Guide

> Comprehensive guide to setting up and running The Code Master system locally

**© 2024-2025 | Developed by Duncan N. for Developers**

---

## 📋 Table of Contents

1. [Quick Start (2 minutes)](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Running the System](#running-the-system)
6. [Troubleshooting](#troubleshooting)
7. [Development Setup](#development-setup)

---

## 🚀 Quick Start

### For Windows Users (Recommended)

```bash
# 1. Navigate to the project directory
cd TheFutureOfGenAiClass

# 2. Double-click START_SYSTEM.bat
# The system will:
# - Check internet connection
# - Verify Python installation
# - Create/activate virtual environment
# - Install all dependencies
# - Start frontend on port 8502

# 3. Open your browser to:
# http://localhost:8502
```

### For Linux/Mac Users

```bash
# 1. Navigate to the project directory
cd TheFutureOfGenAiClass

# 2. Make START_SYSTEM.sh executable
chmod +x START_SYSTEM.sh

# 3. Run the starter script
./START_SYSTEM.sh

# 4. Open your browser to:
# http://localhost:8502
```

---

## 📦 System Requirements

### Minimum Requirements

| Component | Version | Details |
|-----------|---------|---------|
| Python | 3.10+ | From https://www.python.org/downloads/ |
| pip | Latest | Comes with Python |
| Internet | Required | For GitHub integration and API calls |
| RAM | 4 GB | Minimum for smooth operation |
| Disk Space | 2 GB | For dependencies and cache |
| Browser | Modern | Chrome, Firefox, Safari, Edge |

### Optional Requirements

| Component | Purpose |
|-----------|---------|
| OpenAI API Key | Enable LLM-powered features |
| Git | For version control |
| JAC/Jaseci | For full backend support |

### Supported Operating Systems

- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, CentOS, Debian)
- ✅ WSL 2 (Windows Subsystem for Linux)

---

## 📥 Installation Guide

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass.git

# Navigate to project
cd TheFutureOfGenAiClass
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip
```

### Step 4: Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd CodebaseGenius/FE

# Install requirements
pip install -r requirements.txt

# Return to project root
cd ../..
```

### Step 5: Install Backend Dependencies (Optional)

```bash
# Navigate to backend directory
cd CodebaseGenius/BE

# Install requirements
pip install -r requirements.txt

# Return to project root
cd ../..
```

### Step 6: Configure Environment

```bash
# Copy environment template
copy .env.example .env          # Windows
cp .env.example .env            # Linux/Mac

# Edit .env with your settings
# - Add OpenAI API key (optional)
# - Configure ports if needed
# - Set system preferences
```

---

## 🔧 Configuration

### Environment Variables (.env)

Create `.env` file in the project root:

```env
# OpenAI API Configuration (optional)
OPENAI_API_KEY=your-api-key-here

# System Configuration
FRONTEND_PORT=8502
BACKEND_PORT=8001
API_ENDPOINT=http://localhost:8001

# Code Analysis Settings
MAX_FILES_TO_ANALYZE=20
MAX_FILE_SIZE_MB=5
IGNORE_PATTERNS=.git,node_modules,__pycache__,.venv

# Documentation Settings
INCLUDE_API_REFERENCE=true
INCLUDE_ARCHITECTURE=true
INCLUDE_CONTRIBUTING=true

# Logging
LOG_LEVEL=INFO
DEBUG=false
```

### Streamlit Configuration

Edit `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0D47A1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f7fa"
textColor = "#333333"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[logger]
level = "info"
```

---

## 🎯 Running the System

### Method 1: Using Starter Script (Recommended)

#### Windows

```bash
# Simply double-click
START_SYSTEM.bat

# Or run from command line
START_SYSTEM.bat
```

The script will:
1. ✅ Check internet connection
2. ✅ Verify Python installation
3. ✅ Create virtual environment
4. ✅ Install dependencies
5. ✅ Start frontend server

#### Linux/Mac

```bash
# Make script executable
chmod +x START_SYSTEM.sh

# Run the script
./START_SYSTEM.sh
```

### Method 2: Manual Startup

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Navigate to frontend
cd CodebaseGenius/FE

# Start Streamlit
streamlit run code_master.py --server.port 8502

# Application will open at:
# http://localhost:8502
```

### Method 3: Backend + Frontend

```bash
# Terminal 1: Start Backend (optional)
cd CodebaseGenius/BE
source venv/bin/activate
jac serve main.jac

# Terminal 2: Start Frontend
cd CodebaseGenius/FE
source venv/bin/activate
streamlit run code_master.py --server.port 8502
```

---

## 🌐 Accessing the System

Once started, access The Code Master at:

```
Frontend:     http://localhost:8502
Backend:      http://localhost:8001 (if running)
Network:      http://<your-ip>:8502
```

### First Time Usage

1. **Open the frontend** in your browser
2. **Review the sidebar** for system status
3. **Go to "🚀 Generate Docs" tab**
4. **Paste a GitHub URL** to get started
5. **Click "✓ Validate"** to process

---

## 🐛 Troubleshooting

### Issue: "Python not found"

**Solution:**
```bash
# Windows: Add Python to PATH or reinstall with "Add Python to PATH" checked
# Install from: https://www.python.org/downloads/

# Verify installation:
python --version
```

### Issue: "Port already in use"

**Solution:**
```bash
# Windows: Change port in start command
streamlit run code_master.py --server.port 8503

# Find process using port:
# Windows: netstat -ano | findstr :8502
# Linux/Mac: lsof -i :8502

# Kill process and restart
```

### Issue: "Streamlit app not opening"

**Solution:**
```bash
# Check if app is running
# Should see: "You can now view your Streamlit app in your browser"

# Open manually:
# http://localhost:8502

# Enable error details:
streamlit run code_master.py --logger.level=debug
```

### Issue: "Backend connection failed"

**Solution:**
```bash
# System works in demo mode without backend
# Backend is optional for frontend to function

# If you need backend:
cd CodebaseGenius/BE
python -m pip install jaseci jac-cloud -U

# Start backend separately:
jac serve main.jac
```

### Issue: "No internet connection"

**Solution:**
```bash
# The starter script will detect this and offer:
# - Continue in offline mode (frontend works)
# - Exit and connect to internet

# For full functionality, connect to internet for:
# - GitHub repository access
# - OpenAI API calls
# - Package downloads
```

### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or reinstall all fresh:
pip uninstall streamlit requests python-dotenv -y
pip install -r requirements.txt

# Check installed packages:
pip list
```

### Issue: "Virtual environment not activating"

**Solution:**
```bash
# Windows - Try different activation
venv\Scripts\activate.bat
# or
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Recreate venv if needed:
python -m venv venv --clear
```

---

## 👨‍💻 Development Setup

### For Contributors

```bash
# 1. Clone repository
git clone https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass.git
cd TheFutureOfGenAiClass

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Set up development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 4. Install dev dependencies
cd CodebaseGenius/FE
pip install -r requirements.txt
# Add dev tools if needed:
# pip install pytest black flake8 mypy

# 5. Make your changes

# 6. Test
streamlit run code_master.py

# 7. Commit and push
git add .
git commit -m "feat: Your feature description"
git push origin feature/your-feature-name
```

### Running Tests

```bash
# Run Streamlit in test mode
streamlit run code_master.py --logger.level=debug

# Run backend tests (if available)
cd CodebaseGenius/BE
python -m pytest tests/
```

### Code Quality

```bash
# Format code with Black
black CodebaseGenius/FE/code_master.py

# Check with flake8
flake8 CodebaseGenius/FE/code_master.py

# Type checking with mypy
mypy CodebaseGenius/FE/code_master.py
```

---

## 📖 Additional Resources

- **Documentation**: See [CODE_MASTER_README.md](./CODE_MASTER_README.md)
- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **API Reference**: See [API_REFERENCE.md](./API_REFERENCE.md)
- **Project Summary**: See [PROJECT_COMPLETION_SUMMARY.md](./PROJECT_COMPLETION_SUMMARY.md)

---

## 📞 Support & Help

- **GitHub Issues**: [Report a bug](https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass/issues)
- **GitHub Discussions**: [Ask a question](https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass/discussions)
- **Developer**: [Duncan N. on GitHub](https://github.com/DUNCANNJUKI)

---

## 📝 Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | Nov 2025 | Initial release with Streamlit frontend & JAC backend |

---

## ✅ Checklist Before Running

- [ ] Python 3.10+ installed
- [ ] Internet connection available
- [ ] Project cloned/downloaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured (optional)
- [ ] Port 8502 available
- [ ] Browser ready to open

---

**The Code Master is ready to transform your repositories into professional documentation!**

*For questions or issues, please visit our [GitHub repository](https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass)*

---

© 2024-2025 | Developed by Duncan N. for Developers | MIT License
