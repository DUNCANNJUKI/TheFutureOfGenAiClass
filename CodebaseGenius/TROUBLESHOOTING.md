# Codebase Genius - Troubleshooting & FAQ

## Table of Contents
1. [Frequently Asked Questions](#frequently-asked-questions)
2. [Installation Issues](#installation-issues)
3. [Backend Issues](#backend-issues)
4. [Frontend Issues](#frontend-issues)
5. [API Integration Issues](#api-integration-issues)
6. [Performance Issues](#performance-issues)
7. [Deployment Issues](#deployment-issues)
8. [FAQ by User Type](#faq-by-user-type)

## Frequently Asked Questions

### General Questions

**Q: What is Codebase Genius?**

A: Codebase Genius is an AI-powered, multi-agent system that automatically analyzes, documents, and reviews source code. It uses byLLM (a framework for building agentic AI systems) with specialized agents for code analysis, documentation generation, and code reviews.

**Q: What languages are supported?**

A: Codebase Genius supports 14+ programming languages including:
- Python, JavaScript, Java, C++, C#
- Go, Rust, Ruby, PHP, Swift
- TypeScript, Kotlin, Scala, R

See `BE/utils.jac` for the complete language mapping.

**Q: Do I need an OpenAI account?**

A: Yes, for the default `gpt-4o` model. Alternatively, you can use Google Gemini API. Both require API keys with credits.

**Q: How much does it cost to run?**

A: Cost depends on:
- File count and size
- Model selected (gpt-3.5-turbo is cheaper than gpt-4o)
- Typical project: $0.50 - $5.00 per analysis

To reduce costs:
```env
# Use cheaper model
OPENAI_MODEL=gpt-3.5-turbo

# Limit files
MAX_FILES_TO_ANALYZE=50
```

**Q: Can I run it offline?**

A: Currently, no. The system requires API calls to OpenAI/Gemini. For offline operation, you'd need to integrate a local LLM (not currently supported).

**Q: What's the maximum project size?**

A: Recommended: < 1000 files
Supported: Limited by available memory and API rate limits

Configure limits:
```env
MAX_FILES_TO_ANALYZE=100
MAX_FILE_SIZE_MB=5
```

**Q: How long does analysis take?**

A: Typical times:
- Small project (< 50 files): 2-5 minutes
- Medium project (50-200 files): 5-15 minutes
- Large project (200+ files): 15+ minutes

Use `gpt-3.5-turbo` for faster analysis.

### Functionality Questions

**Q: Can I analyze multiple repositories simultaneously?**

A: Yes, process them sequentially. The system creates separate project records.

```python
for repo_path in repos:
    client.analyze_project(repo_path, files)
    time.sleep(1)  # Rate limit
```

**Q: What kind of documentation does it generate?**

A: Four types:
1. **API Documentation** - Endpoints, parameters, responses
2. **Architecture Guide** - System design, data flow, components
3. **README** - Overview, features, setup instructions
4. **Contributing Guide** - How to contribute to project

**Q: Can I export results?**

A: Yes, from the Streamlit UI you can download markdown. For API, parse the JSON response and save.

**Q: Does it work with private repositories?**

A: For local paths: yes. For GitHub private repos: clone locally first, then analyze.

```bash
git clone git@github.com:user/private-repo.git
# Then upload cloned directory
```

**Q: How accurate are the AI-generated results?**

A: Generally 85-95% accurate. Always review before using in production:
- Some suggestions may need domain knowledge
- Complex algorithms require manual verification
- Consider it as a starting point, not final result

**Q: Can I customize the AI prompts?**

A: Yes, edit the semantic instructions in `BE/main.jac`:

```jac
sem CodeAnalyzer.analyze_code_structure = """
Your custom prompt here...
""";
```

### Deployment Questions

**Q: How do I run this in production?**

A: Three options:

1. **Docker** (Recommended)
```bash
docker-compose up -d
```

2. **Kubernetes**
```bash
kubectl apply -f deployment.yaml
```

3. **Traditional**
```bash
cd BE && jac serve main.jac &
cd FE && streamlit run app.py &
```

**Q: What's the recommended hardware?**

A: Minimum:
- 2 CPU cores
- 2GB RAM
- 500MB disk

Recommended:
- 4+ CPU cores
- 4GB+ RAM
- 2GB disk

**Q: Do I need a database?**

A: No, JAC uses embedded Jarcdb. No external database required.

**Q: How do I backup results?**

A: Backup the JAC database directory:
```bash
cp -r .jac-data backup/$(date +%s)
```

### Security Questions

**Q: Is my code secure?**

A: Code is sent to OpenAI/Gemini APIs. For sensitive code:
- Use gpt-3.5-turbo for local deployment
- Implement API call logging
- Use in isolated network
- Review API provider's privacy policies

**Q: How do I authenticate API calls?**

A: Currently no built-in auth. For production:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=403)
    return credentials
```

**Q: What permissions does it need?**

A: Just read access to source files. No write permissions needed unless exporting docs.

## Installation Issues

### Issue 1: "Python version not supported"

**Symptom:**
```
Python 3.9 detected, but Python 3.10+ required
```

**Solution:**

Check Python version:
```bash
python --version
```

Install Python 3.10+:
- Windows: Download from python.org
- Mac: `brew install python@3.10`
- Linux: `apt install python3.10`

Create venv with correct version:
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Issue 2: "pip install fails"

**Symptom:**
```
ERROR: Could not install packages due to EnvironmentError
```

**Solution:**

1. Upgrade pip:
```bash
python -m pip install --upgrade pip
```

2. Use specific version constraints:
```bash
pip install byllm==0.4.5 --force-reinstall
```

3. Check network:
```bash
ping pypi.org
```

4. Use alternative index:
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple byllm
```

### Issue 3: "JAC not found"

**Symptom:**
```
jac: command not found
```

**Solution:**

Ensure venv activated:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Install JAC:
```bash
pip install jac
```

Verify:
```bash
jac --version
```

### Issue 4: "Module not found errors"

**Symptom:**
```
ModuleNotFoundError: No module named 'byllm'
```

**Solution:**

1. Check venv is active:
```bash
which python  # Should show venv path
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Install specific package:
```bash
pip install byllm==0.4.5
```

## Backend Issues

### Issue 1: "JAC server won't start"

**Symptom:**
```
Error loading main.jac
```

**Solution:**

1. Check JAC syntax:
```bash
jac check main.jac
```

2. Verify file exists:
```bash
ls -la BE/main.jac
```

3. Check for syntax errors:
```bash
# Look for red squiggly lines in editor
# Check line numbers from error message
```

4. Try verbose mode:
```bash
jac serve main.jac -v
```

### Issue 2: "Port 8000 already in use"

**Symptom:**
```
Address already in use
```

**Solution:**

**Windows:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :8000
kill -9 <PID>
```

Or change port:
```bash
jac serve main.jac --port 9000
```

### Issue 3: "Cannot connect to backend"

**Symptom:**
```
Connection refused localhost:8000
```

**Solution:**

1. Verify server running:
```bash
curl http://localhost:8000/walker/get_projects
```

2. Check if port is open:
```bash
netstat -an | grep 8000
```

3. Restart server:
```bash
# Kill old process
pkill -f "jac serve"

# Start fresh
jac serve main.jac
```

4. Check firewall:
- Windows: Open port 8000 in Windows Firewall
- Mac: Allow in System Preferences
- Linux: `sudo ufw allow 8000`

### Issue 4: "Out of memory errors"

**Symptom:**
```
MemoryError: Unable to allocate resources
```

**Solution:**

1. Reduce analysis scope:
```env
MAX_FILES_TO_ANALYZE=50
MAX_FILE_SIZE_MB=3
```

2. Process smaller batches:
```python
# Split large project
files_batch1 = files[:50]
files_batch2 = files[50:100]

client.analyze_project(path, files_batch1)
client.analyze_project(path, files_batch2)
```

3. Increase system memory:
- Add swap space (Linux)
- Close other applications
- Use lightweight model: gpt-3.5-turbo

### Issue 5: "API key invalid"

**Symptom:**
```
InvalidAPIKeyError: Invalid API key provided
```

**Solution:**

1. Check .env file:
```bash
cat .env
```

2. Verify key format:
```bash
# Should start with sk_
echo $OPENAI_API_KEY
```

3. Test key:
```python
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print(f"Key exists: {key is not None}")
print(f"Key starts correctly: {key.startswith('sk_') if key else False}")
```

4. Regenerate key:
- OpenAI dashboard → API keys → Generate new key
- Paste into .env file

## Frontend Issues

### Issue 1: "Cannot connect to backend"

**Symptom:**
```
ConnectionError: Cannot connect to http://localhost:8000
```

**Solution:**

1. Update BASE_URL in `app.py`:
```python
# In FE/app.py
BASE_URL = "http://localhost:8000"  # Local
# Or
BASE_URL = "http://backend:8000"    # Docker
```

2. Verify backend running:
```bash
curl http://localhost:8000/walker/get_projects
```

3. Check network:
```bash
ping localhost
```

### Issue 2: "Streamlit won't start"

**Symptom:**
```
ImportError: No module named 'streamlit'
```

**Solution:**

1. Install dependencies:
```bash
cd FE
pip install -r requirements.txt
```

2. Verify installation:
```bash
python -c "import streamlit; print(streamlit.__version__)"
```

3. Start with explicit Python:
```bash
python -m streamlit run app.py
```

### Issue 3: "Port 8501 in use"

**Symptom:**
```
Address already in use: 8501
```

**Solution:**

```bash
# Kill existing process
lsof -i :8501
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### Issue 4: "Slow UI response"

**Symptom:**
- UI freezes when clicking buttons
- 30+ second wait times

**Solution:**

1. Reduce file count:
```python
# In app.py
max_files = st.slider("Max files", 10, 500, 50)  # Default 50 instead of 100
```

2. Use faster model:
```env
OPENAI_MODEL=gpt-3.5-turbo
```

3. Add loading indicators:
```python
with st.spinner("Analyzing... this may take a few minutes"):
    result = requests.post(...)
```

4. Implement timeouts:
```python
response = requests.post(url, timeout=120)
```

### Issue 5: "File upload not working"

**Symptom:**
- Upload button doesn't respond
- "File too large" error

**Solution:**

1. Check Streamlit config:
```python
# .streamlit/config.toml
[client]
maxUploadSize = 200

[server]
maxUploadSize = 200
```

2. Increase limit:
```toml
maxUploadSize = 500  # MB
```

3. Or use path input instead:
```python
# In app.py, use text input for local paths
repo_path = st.text_input("Repository path")
```

## API Integration Issues

### Issue 1: "POST request fails"

**Symptom:**
```
HTTP 400: Bad Request
```

**Solution:**

1. Verify JSON format:
```python
data = {
    "action": "analyze",
    "message": "test",
    "project_path": "/path/to/project",
    "files_data": []
}

# Validate JSON
import json
json.dumps(data)
```

2. Check required fields:
```python
required = ["action", "message"]
if not all(k in data for k in required):
    raise ValueError("Missing required fields")
```

3. Print request:
```python
import json
print(json.dumps(data, indent=2))
response = requests.post(url, json=data)
```

### Issue 2: "Timeout errors"

**Symptom:**
```
TimeoutError: Request timed out after 30 seconds
```

**Solution:**

1. Increase timeout:
```python
response = requests.post(url, json=data, timeout=300)
```

2. Use async processing:
```python
# Implement polling
response = requests.post(url, json=data)
task_id = response.json()["task_id"]

# Poll for status
while True:
    status = requests.get(f"{url}/status/{task_id}")
    if status.json()["complete"]:
        break
    time.sleep(5)
```

3. Reduce scope:
```env
MAX_FILES_TO_ANALYZE=50
```

### Issue 3: "Invalid response format"

**Symptom:**
```
JSONDecodeError: Expecting value
```

**Solution:**

1. Check response status:
```python
response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Content: {response.text}")

if response.status_code != 200:
    print("Error response")
    return None

data = response.json()
```

2. Validate response:
```python
required_keys = ["data", "status", "message"]
if not all(k in data for k in required_keys):
    print("Invalid response structure")
    return None
```

## Performance Issues

### Issue: "Analysis is very slow"

**Symptom:**
- 15+ minutes for small projects
- CPU/memory maxed out

**Solution:**

**Option 1: Reduce scope**
```env
MAX_FILES_TO_ANALYZE=25
MAX_FILE_SIZE_MB=2
IGNORE_PATTERNS=node_modules,dist,build,.venv,venv
```

**Option 2: Use faster model**
```env
OPENAI_MODEL=gpt-3.5-turbo
```

**Option 3: Parallel processing**
```python
from concurrent.futures import ThreadPoolExecutor

def analyze_batch(files_batch):
    return client.analyze_project(path, files_batch)

with ThreadPoolExecutor(max_workers=3) as executor:
    batches = [files[i:i+20] for i in range(0, len(files), 20)]
    results = list(executor.map(analyze_batch, batches))
```

**Option 4: Enable caching**
```python
# Skip re-analysis of unchanged files
import hashlib

def file_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

# Only analyze if hash changed
```

### Issue: "High memory usage"

**Symptom:**
- Memory usage grows to 4GB+
- System becomes unresponsive

**Solution:**

1. Monitor memory:
```bash
# Windows
tasklist | findstr python

# Mac/Linux
ps aux | grep python
```

2. Kill processes:
```bash
pkill -f "jac serve"
```

3. Reduce batch size:
```python
# Analyze fewer files at once
batch_size = 10
```

4. Clear cache:
```bash
rm -rf .jac-data/*
```

## Deployment Issues

### Docker Issues

**Issue: "Build fails"**

```bash
# Check Dockerfile syntax
docker build -f Dockerfile .

# Check base image available
docker pull python:3.10-slim

# Build with verbose output
docker build --progress=plain .
```

**Issue: "Container crashes immediately"**

```bash
# Check logs
docker logs <container_id>

# Inspect container
docker inspect <container_id>

# Run interactively
docker run -it <image> /bin/bash
```

### Kubernetes Issues

**Issue: "Pod won't start"**

```bash
# Check pod status
kubectl describe pod <pod_name>

# Check logs
kubectl logs <pod_name>

# Check resources
kubectl top pod <pod_name>
```

**Issue: "Service unreachable"**

```bash
# Check service
kubectl get svc

# Check endpoints
kubectl get endpoints

# Port forward for testing
kubectl port-forward svc/backend 8000:8000
```

## FAQ by User Type

### For Beginners

**Q: Where do I start?**
A: Follow `GETTING_STARTED.md` → Quick Start section (5 minutes)

**Q: Why does it need an API key?**
A: Uses OpenAI/Gemini APIs to power the AI analysis. You can get a free trial key.

**Q: What if I don't have API credit?**
A: Use a free tier or alternative like Hugging Face (requires code changes)

**Q: How do I know if it's working?**
A: Both servers should show:
- Backend: "Ready to accept requests"
- Frontend: "Local URL: http://localhost:8501"

### For Developers

**Q: How do I extend the system with new agents?**
A: Add new agent node in `BE/main.jac` with:
- Node definition
- Methods with semantic instructions
- Walker function to expose it

**Q: Can I use a different LLM?**
A: Yes, modify `main.jac` line with Model initialization

**Q: How do I debug agent behavior?**
A: Add logging in JAC:
```jac
std.out("Debug: {variable}");
```

**Q: Can I customize the UI?**
A: Yes, edit `FE/app.py` - it's a standard Streamlit app

### For DevOps

**Q: What's the deployment topology?**
A: Two services:
- Backend (JAC server, stateless)
- Frontend (Streamlit, stateless)
- Both connect to embedded Jarcdb

**Q: How do I scale this?**
A: Run multiple backend instances behind load balancer

**Q: What's the backup strategy?**
A: Backup the `.jac-data` directory periodically

**Q: What monitoring metrics matter?**
A: API response time, file analysis duration, memory usage, error rate

---

## Still Having Issues?

1. **Check logs:**
   - Backend: Terminal output when running `jac serve`
   - Frontend: Terminal output when running `streamlit`

2. **Review error message:**
   - Google the exact error
   - Check GitHub issues
   - Review documentation

3. **Isolation testing:**
   - Test backend with curl
   - Test frontend locally
   - Test API integration separately

4. **Community help:**
   - JAC Community Forums
   - Streamlit Community
   - Check existing GitHub issues

5. **Detailed diagnostics:**
   ```bash
   # Create debug report
   python --version
   pip list
   curl http://localhost:8000/walker/get_projects -v
   ```

---

**Need more help?**

Check documentation in order:
1. `GETTING_STARTED.md` - Quick setup
2. `README.md` - Features and capabilities
3. `ARCHITECTURE.md` - Design details
4. `API_REFERENCE.md` - API specifics
5. `TROUBLESHOOTING.md` - This file!

**Still stuck?** Create a detailed issue with:
- Error message (full text)
- Steps to reproduce
- System info (OS, Python version, etc.)
- Relevant logs/output
