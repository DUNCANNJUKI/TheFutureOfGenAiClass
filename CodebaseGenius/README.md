# Codebase Genius

🧠 **An AI-Powered, Multi-Agent System for Automatic Documentation Generation**

## Overview

Codebase Genius is an intelligent documentation system that automatically analyzes any software repository and generates comprehensive, high-quality documentation using a multi-agent AI architecture built with **byLLM** (JAC Language) and **Streamlit**.

The system employs multiple specialized AI agents working in concert:
- **Code Analyzer Agent** - Understands code structure, functions, and dependencies
- **Documentation Generator Agent** - Creates comprehensive documentation
- **Code Reviewer Agent** - Identifies issues and suggests improvements
- **Orchestrator** - Routes tasks to appropriate agents

## Features

✨ **Core Capabilities**
- 🔍 Automatic code analysis and structure extraction
- 📚 Intelligent documentation generation (README, API docs, Architecture guides)
- ✅ Code quality review and recommendations
- 💬 Interactive chat interface with AI insights
- 🎯 Multi-language support (Python, JavaScript, TypeScript, Java, C++, Go, Rust, etc.)
- 📊 Comprehensive metrics and statistics
- 🔗 Dependency mapping and analysis

## System Architecture

### Backend (byLLM + JAC)

```
┌─────────────────────────────────────────────────────────┐
│                   Codebase Genius Backend                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Analyzer   │  │  Doc Gen     │  │  Reviewer    │  │
│  │   Agent      │  │   Agent      │  │  Agent       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                 │                  │           │
│         └─────────────────┼──────────────────┘           │
│                           │                              │
│                    ┌──────▼──────┐                       │
│                    │ Orchestrator │                       │
│                    │   (Router)   │                       │
│                    └──────┬──────┘                       │
│                           │                              │
│         ┌─────────────────┼─────────────────┐            │
│         │                 │                 │            │
│    ┌────▼─────┐   ┌──────▼──────┐   ┌─────▼────┐       │
│    │  Graph   │   │   Memory    │   │ Sessions │       │
│    │ Database │   │   Manager   │   │ Manager  │       │
│    └──────────┘   └─────────────┘   └──────────┘       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Frontend (Streamlit)

```
┌─────────────────────────────────────────────────────┐
│            Codebase Genius UI                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │  Repository  │  │    Code      │  │ Generate  │ │
│  │   Upload     │  │   Analysis   │  │   Docs    │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  Code        │  │    Chat      │                │
│  │  Review      │  │   Interface  │                │
│  └──────────────┘  └──────────────┘                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- API key for LLM provider (OpenAI or Google Gemini)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd CodebaseGenius/BE
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Start the JAC server:**
   ```bash
   jac serve main.jac
   ```

   The server will start at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd CodebaseGenius/FE
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

   The UI will open at `http://localhost:8501`

## Usage Guide

### Step 1: Upload Repository

1. Open the **Repository Upload** tab
2. Provide either:
   - Local path to your repository
   - Git repository URL
3. Configure project metadata (name, version, language, description)
4. Click **Load Repository**

### Step 2: Analyze Code

1. Go to **Code Analysis** tab
2. Run the following agents:
   - **Structure Analyzer** - Maps code organization
   - **Complexity Analyzer** - Evaluates code complexity
   - **Dependency Analyzer** - Maps dependencies
3. Review the analysis results

### Step 3: Generate Documentation

1. Navigate to **Generate Docs** tab
2. Choose documentation types:
   - **API Documentation** - Function/method reference
   - **Architecture Guide** - System design overview
   - **README** - Project introduction
   - **Contributing Guide** - Development guidelines
   - **CHANGELOG** - Version history
3. Preview and customize
4. Export documentation

### Step 4: Code Review

1. Open **Code Review** tab
2. Run multiple reviewers:
   - **Quality Analyzer** - Code smell detection
   - **Security Reviewer** - Vulnerability assessment
   - **Performance Analyzer** - Optimization suggestions
3. View detailed recommendations

### Step 5: Chat Interface

1. Go to **Chat with Genius** tab
2. Ask questions about your codebase:
   - "How should I optimize the database queries?"
   - "What's the architecture of this project?"
   - "Are there any security concerns?"
3. Get AI-powered insights in real-time

## Agent Details

### Code Analyzer Agent

Analyzes code structure and extracts information:

**Capabilities:**
- Identifies functions, classes, and methods
- Maps module/package structure
- Extracts imports and dependencies
- Measures lines of code
- Identifies design patterns

**Output:**
- Code structure report
- Function inventory
- Dependency graph
- Import analysis

### Documentation Generator Agent

Creates comprehensive project documentation:

**Capabilities:**
- Generates API documentation
- Creates usage examples
- Builds architecture guides
- Compiles comprehensive README
- Produces contributing guidelines

**Output:**
- README.md
- API_REFERENCE.md
- ARCHITECTURE.md
- CONTRIBUTING.md
- CHANGELOG.md

### Code Reviewer Agent

Reviews code for quality and improvements:

**Capabilities:**
- Detects code smells
- Identifies security issues
- Suggests optimizations
- Checks best practices
- Proposes refactoring

**Output:**
- Quality report
- Security findings
- Performance recommendations
- Best practice checklist

## API Reference

### Main Endpoints

#### Create Documentation Session
```http
POST /walker/codebase_genius
Content-Type: application/json

{
  "action": "analyze",
  "message": "Project Name",
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
}
```

#### Analyze Files
```http
POST /walker/analyze_files
Content-Type: application/json

{
  "file_nodes": ["node_id_1", "node_id_2"]
}
```

#### Generate Documentation
```http
POST /walker/generate_documentation
Content-Type: application/json

{
  "project_id": "project_node_id"
}
```

#### Review Code
```http
POST /walker/review_code
Content-Type: application/json

{
  "project_id": "project_node_id"
}
```

#### Get Projects
```http
GET /walker/get_projects
```

#### Get Sessions
```http
GET /walker/get_sessions
```

## Configuration

### Environment Variables (.env)

```env
# LLM Configuration
OPENAI_API_KEY=sk_...
# GEMINI_API_KEY=...

# Repository Analysis
MAX_FILES_TO_ANALYZE=100
MAX_FILE_SIZE_MB=5
IGNORE_PATTERNS=node_modules,__pycache__,.git,dist,build,.venv,venv

# Documentation Output
DOCS_OUTPUT_FORMAT=markdown
DOCS_INCLUDE_EXAMPLES=true
DOCS_INCLUDE_ARCHITECTURE=true
```

### Supported Languages

- ✅ Python
- ✅ JavaScript/TypeScript
- ✅ Java
- ✅ C/C++
- ✅ Go
- ✅ Rust
- ✅ Ruby
- ✅ PHP
- ✅ C#
- ✅ Swift
- ✅ Kotlin
- ✅ SQL
- ✅ Jac
- ✅ Markdown

## Project Structure

```
CodebaseGenius/
├── BE/                          # Backend (byLLM + JAC)
│   ├── main.jac                # Main orchestration logic
│   ├── utils.jac               # Utility functions
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   └── README.md                # Backend documentation
│
├── FE/                          # Frontend (Streamlit)
│   ├── app.py                  # Main Streamlit application
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Frontend documentation
│
└── README.md                    # This file
```

## Advanced Usage

### Custom Agents

To create custom analysis agents, extend the agent system:

```jac
node CustomAnalyzer {
    def analyze_custom(code: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    can execute with custom_analysis entry {
        // Custom analysis logic
        report { "result": "..." };
    }
}
```

### Batch Processing

Process multiple repositories:

```python
repositories = [
    "https://github.com/user/repo1",
    "https://github.com/user/repo2",
    "https://github.com/user/repo3"
]

for repo in repositories:
    # Load and analyze
    # Generate documentation
```

### Export Formats

- 📄 Markdown (default)
- 🌐 HTML
- 📕 PDF
- 📋 JSON

## Performance Tips

1. **Limit file size** - Set `MAX_FILE_SIZE_MB` to skip large files
2. **Use caching** - Enable documentation caching for frequent repos
3. **Batch analysis** - Process multiple files concurrently
4. **Optimize prompts** - Use semantic tokens efficiently

## Troubleshooting

### Issue: "Connection refused" error

**Solution:** Ensure JAC server is running:
```bash
jac serve main.jac
```

### Issue: API key errors

**Solution:** Verify your `.env` file contains valid API keys:
```bash
cat .env | grep API_KEY
```

### Issue: Missing documentation

**Solution:** Check that code files are properly loaded:
1. Verify file paths are correct
2. Ensure files are within size limits
3. Check language is supported

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

- 📖 [Documentation](https://github.com/...)
- 🐛 [Issue Tracker](https://github.com/...)
- 💬 [Discussions](https://github.com/...)

## Related Projects

- [byLLM Documentation](https://github.com/jaseci-labs/byLLM)
- [JAC Language](https://jaseci.org/)
- [Task Manager Example](https://github.com/jaseci-labs/Agentic-AI/task_manager)

---

**Built with ❤️ using byLLM & JAC**
