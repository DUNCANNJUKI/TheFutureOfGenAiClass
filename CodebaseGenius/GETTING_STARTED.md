# Getting Started with Codebase Genius

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Navigate to projects directory
cd c:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\CodebaseGenius

# Setup backend
cd BE
python -m venv venv
venv\Scripts\activate  # On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure LLM

Create `.env` file:

```bash
cp .env.example .env
# Edit .env with your API key
```

**Option A: OpenAI**
```env
OPENAI_API_KEY=sk_...your_key_here...
```

**Option B: Google Gemini**
```env
GEMINI_API_KEY=...your_key_here...
```

### 3. Start Backend

```bash
# In BE directory
jac serve main.jac
```

You should see:
```
Starting JAC server on localhost:8000
Ready to accept requests
```

### 4. Setup Frontend

In a new terminal:

```bash
# Navigate to FE directory
cd CodebaseGenius/FE
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py
```

Opens automatically at: `http://localhost:8501`

## Basic Workflow

### Step 1: Upload Repository

1. Open Streamlit UI → **Repository Upload** tab
2. Paste path to repository:
   ```
   c:\path\to\your\project
   ```
3. Or Git URL:
   ```
   https://github.com/user/repo.git
   ```
4. Fill in project details
5. Click **Load Repository**

### Step 2: Analyze Code

1. Go to **Code Analysis** tab
2. Click one of:
   - 🔍 Run Structure Analysis
   - 🚀 Run Complexity Analysis
   - 🔗 Run Dependency Analysis
3. Wait for completion (progress bar)
4. View results in metrics

### Step 3: Generate Documentation

1. Go to **Generate Docs** tab
2. Select documentation types:
   - 📖 API Documentation
   - 🏗️ Architecture Guide
   - 📖 README
   - 🔧 Contributing Guide
3. Preview the generated docs
4. Download/export as needed

### Step 4: Code Review

1. Go to **Code Review** tab
2. Run reviews:
   - 🔍 Quality Check
   - 🔐 Security Review
   - ⚡ Performance Check
3. Review findings and recommendations

### Step 5: Chat Interface

1. Go to **Chat with Genius** tab
2. Ask questions like:
   - "How should I optimize the database?"
   - "What's the project architecture?"
   - "Are there security issues?"
3. Get AI-powered responses

## Testing with Sample Repository

### Using WasteTracker (Already in workspace)

```bash
# Backend already running, just upload:
c:\xampp\htdocs\GenAIClass\TheFutureOfGenAiClass\WasteTracker
```

This will analyze:
- Django configuration
- REST API endpoints
- Database models
- Views and serializers

### Create Sample Project

```bash
# Create test repo
mkdir test_project
cd test_project

# Create Python files
cat > main.py << 'EOF'
"""Main application module."""
import os

def process_data(data: dict) -> dict:
    """Process input data."""
    return {"result": data}

class DataProcessor:
    """Handles data processing operations."""
    
    def __init__(self, name: str):
        self.name = name
    
    def run(self):
        """Execute processing."""
        pass
EOF

# Add to Codebase Genius
cd ../CodebaseGenius/FE
# Upload test_project path
```

## Configuration Guide

### Backend Settings (.env)

```env
# LLM Provider (choose one)
OPENAI_API_KEY=sk_...
# GEMINI_API_KEY=...

# Model Selection
# Default: gpt-4o (for OpenAI)
# Options: gpt-4o, gpt-4-turbo, gpt-3.5-turbo

# Repository Analysis
MAX_FILES_TO_ANALYZE=100      # Limit number of files
MAX_FILE_SIZE_MB=5            # Skip large files
IGNORE_PATTERNS=node_modules,__pycache__,.git,dist,build

# Documentation
DOCS_OUTPUT_FORMAT=markdown   # markdown, html, pdf
DOCS_INCLUDE_EXAMPLES=true
DOCS_INCLUDE_ARCHITECTURE=true
```

### Frontend Settings (in app.py)

```python
BASE_URL = "http://localhost:8000"  # JAC server address

# LLM Settings (UI configurable)
llm_provider = st.selectbox("Provider", ["OpenAI", "Gemini"])
max_files = st.slider("Max Files", 10, 500, 100)
max_file_size = st.slider("Max Size (MB)", 1, 50, 5)
```

## Common Use Cases

### Case 1: Document Existing Project

```
1. Load repository
2. Run full analysis
3. Generate comprehensive docs
4. Export README + API reference
```

### Case 2: Code Review Before Release

```
1. Load repository
2. Run code review analysis
3. Review findings
4. Fix issues
5. Re-analyze
```

### Case 3: Understand New Codebase

```
1. Load project
2. Run structure analysis
3. Chat: "Give me architecture overview"
4. Chat: "What are main components?"
5. Chat: "How should I contribute?"
```

### Case 4: Batch Documentation

```
# Create script
repos = [
    "https://github.com/user/repo1",
    "https://github.com/user/repo2"
]

for repo in repos:
    # Upload and generate docs
    # Export results
```

## API Usage Examples

### Using cURL

#### Analyze Repository

```bash
curl -X POST http://localhost:8000/walker/codebase_genius \
  -H "Content-Type: application/json" \
  -d '{
    "action": "analyze",
    "message": "MyProject",
    "project_path": "/path/to/repo",
    "files_data": [
      {
        "path": "src/main.py",
        "name": "main.py",
        "ext": "py",
        "content": "...",
        "loc": 150
      }
    ]
  }'
```

#### Generate Documentation

```bash
curl -X POST http://localhost:8000/walker/generate_documentation \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "node_id_from_analysis"
  }'
```

#### Code Review

```bash
curl -X POST http://localhost:8000/walker/review_code \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "node_id_from_analysis"
  }'
```

#### Get All Projects

```bash
curl http://localhost:8000/walker/get_projects
```

#### Get Sessions

```bash
curl http://localhost:8000/walker/get_sessions
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Analyze
response = requests.post(
    f"{BASE_URL}/walker/codebase_genius",
    json={
        "action": "analyze",
        "message": "MyProject",
        "project_path": "/path/to/repo",
        "files_data": [...]
    }
)
print(response.json())

# Generate docs
response = requests.post(
    f"{BASE_URL}/walker/generate_documentation",
    json={"project_id": "..."}
)
print(response.json())
```

## Troubleshooting

### Issue: "Cannot connect to backend"

**Check 1:** JAC server running?
```bash
# Should see "Ready to accept requests"
jac serve main.jac
```

**Check 2:** Correct URL?
```bash
# Verify in FE/app.py:
BASE_URL = "http://localhost:8000"
```

**Check 3:** Port available?
```bash
# Check port 8000 is free
netstat -an | grep 8000
```

### Issue: "API key invalid"

**Solution:** Verify .env file
```bash
cat .env
# Should show valid OPENAI_API_KEY or GEMINI_API_KEY
```

Test key:
```python
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("OPENAI_API_KEY"))  # Should print key, not None
```

### Issue: "File not found" errors

**Check paths:** Use absolute paths
```
Wrong: ./my_project
Right: /full/path/to/my_project
      or C:\full\path\to\my_project
```

### Issue: "Out of memory"

**Solution:** Reduce file limits
```env
MAX_FILES_TO_ANALYZE=50
MAX_FILE_SIZE_MB=2
```

### Issue: "Slow analysis"

**Solution:** Configure for speed
```env
# Reduce scope
MAX_FILES_TO_ANALYZE=25
DOCS_INCLUDE_ARCHITECTURE=false

# Use faster model
OPENAI_MODEL=gpt-3.5-turbo
```

## Performance Tips

1. **Limit Analysis Scope**
   - Set `MAX_FILES_TO_ANALYZE` to project size
   - Use `IGNORE_PATTERNS` for large directories

2. **Use Caching**
   - Analyses are cached by file hash
   - Re-running same project is instant

3. **Optimize Model Selection**
   - `gpt-3.5-turbo` - Fast, cheap
   - `gpt-4o` - Better quality, slower
   - Choose based on needs

4. **Batch Processing**
   - Process multiple repos in sequence
   - Use background jobs for large projects

## Advanced Configuration

### Custom Agent Prompts

Edit agent semantics in `main.jac`:

```jac
sem CodeAnalyzer.analyze_code_structure = """
Custom prompt here...
Focus on specific aspects...
""";
```

### Custom Ignore Patterns

```env
IGNORE_PATTERNS=node_modules,__pycache__,.git,dist,build,.venv,venv,*.min.js,*.lock
```

### Multiple LLM Models

Modify in `main.jac`:

```jac
# Change default model
glob llm = Model(model_name="gpt-4-turbo", verbose=False);
```

## Next Steps

1. ✅ Complete quick start
2. 📖 Read full [README.md](README.md)
3. 🏗️ Review [ARCHITECTURE.md](ARCHITECTURE.md)
4. 🔧 Customize for your needs
5. 🚀 Deploy to production

## Getting Help

- 📖 Check documentation in repo
- 🐛 Review error messages
- 💬 Check FAQ section
- 📧 Reach out with issues

## Additional Resources

- [byLLM Documentation](https://github.com/jaseci-labs/byLLM)
- [JAC Language Guide](https://jaseci.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Task Manager Example](https://github.com/jaseci-labs/Agentic-AI)

---

**Happy documenting! 🚀**
