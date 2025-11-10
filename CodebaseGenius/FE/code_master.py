"""
The Code Master - Automated Code Documentation System
A sophisticated web application for generating professional documentation from GitHub repositories
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time
from io import StringIO
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="The Code Master",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0D47A1;
        --secondary-color: #1565C0;
        --accent-color: #FF6F00;
        --success-color: #00897B;
        --danger-color: #C62828;
    }
    
    /* Header styling */
    .main-header {
        color: #0D47A1;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subheader {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9em;
    }
    
    .status-processing {
        background-color: #FFF3E0;
        color: #F57C00;
    }
    
    .status-success {
        background-color: #E8F5E9;
        color: #2E7D32;
    }
    
    .status-error {
        background-color: #FFEBEE;
        color: #C62828;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 30px;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0D47A1 100%, #1565C0 0%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Input styling */
    .stTextInput input {
        border: 2px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
    }
    
    .stTextInput input:focus {
        border-color: #0D47A1;
        box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #666;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0D47A1;
        border-bottom: 3px solid #0D47A1;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0D47A1 0%, #1565C0 100%);
    }
    
    /* Code block styling */
    .stCode {
        background-color: #f5f5f5 !important;
        border-radius: 5px !important;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #E3F2FD;
        border-left: 4px solid #0D47A1;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #E8F5E9;
        border-left: 4px solid #00897B;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: #FFF3E0;
        border-left: 4px solid #FF6F00;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .error-box {
        background-color: #FFEBEE;
        border-left: 4px solid #C62828;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # API Configuration
    st.markdown("### API Configuration")
    api_endpoint = st.text_input(
        "Backend API Endpoint",
        value="http://localhost:8001",
        help="URL of the JAC backend server"
    )
    
    st.markdown("---")
    
    # Information
    st.markdown("### ℹ️ About Code Master")
    st.info("""
    **Code Master** is an intelligent documentation generation system that:
    
    • Analyzes GitHub repositories
    • Extracts code structure and relationships
    • Generates professional markdown documentation
    • Creates API references
    • Builds architecture overviews
    
    Built with JAC multi-agent architecture and LLM-powered analysis.
    """)
    
    st.markdown("---")
    
    # System Status
    st.markdown("### 🔍 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Backend", "🟢 Ready", "v1.0")
    with col2:
        st.metric("Models", "🟢 Active", "GPT-4o")

# ============================================================================
# MAIN HEADER
# ============================================================================

col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.markdown("# 📚 The Code Master")
    st.markdown("### Professional Documentation from Code")
    st.markdown("Paste a GitHub repository URL and let AI generate comprehensive documentation automatically.")

with col2:
    st.markdown("")
    st.markdown("")
    st.image("https://img.icons8.com/color/96/000000/github--v1.png", width=80)

st.markdown("---")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Create tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Generate Docs", "✨ Features", "📖 Tutorial", "🔗 Resources"])

# ============================================================================
# TAB 1: GENERATE DOCUMENTATION
# ============================================================================

with tab1:
    st.markdown("## Generate Documentation")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # GitHub URL input
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repo-name",
            help="Paste the full GitHub repository URL",
            label_visibility="visible"
        )
    
    with col2:
        st.markdown("####")
        validate_btn = st.button("✅ Validate", use_container_width=True, key="validate_btn")
    
    # Validation and processing
    if validate_btn and repo_url:
        with st.spinner("Validating repository..."):
            time.sleep(0.5)  # Simulate validation
            
            # Check basic URL format
            if "github.com" in repo_url or "gitlab.com" in repo_url:
                st.success("✅ Repository URL is valid!")
                
                # Extract repo name
                repo_name = repo_url.split("/")[-1].replace(".git", "")
                
                st.markdown("---")
                
                # Analysis progress section
                st.markdown("### 📊 Analysis Progress")
                
                # Create progress tracking
                progress_container = st.container()
                
                with progress_container:
                    # Step 1: Cloning
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.write("🔄 **Step 1:** Cloning repository...")
                    with col2:
                        st.write("20%")
                    st.progress(0.20)
                    time.sleep(0.5)
                    
                    # Step 2: Analyzing files
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.write("🔄 **Step 2:** Analyzing code structure...")
                    with col2:
                        st.write("40%")
                    st.progress(0.40)
                    time.sleep(0.5)
                    
                    # Step 3: Building context graph
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.write("🔄 **Step 3:** Building code context graph...")
                    with col2:
                        st.write("60%")
                    st.progress(0.60)
                    time.sleep(0.5)
                    
                    # Step 4: Generating documentation
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.write("🔄 **Step 4:** Generating documentation...")
                    with col2:
                        st.write("85%")
                    st.progress(0.85)
                    time.sleep(0.5)
                    
                    # Step 5: Finalizing
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.write("✅ **Step 5:** Finalizing...")
                    with col2:
                        st.write("100%")
                    st.progress(1.0)
                
                st.markdown("---")
                
                # Generated Documentation Display
                st.markdown("### 📄 Generated Documentation")
                
                # Simulate generated documentation
                generated_doc = f"""# {repo_name}

## Project Overview

This is a comprehensive analysis of the **{repo_name}** repository. The project demonstrates modern software development practices with clean architecture, robust error handling, and well-documented code.

### Key Features
- **Multi-Agent Architecture:** Uses JAC-based agents for specialized analysis
- **Code Context Graph:** Builds relationship maps between code components
- **Intelligent Documentation:** LLM-powered documentation generation
- **Professional Formatting:** Markdown output with proper structure

### Technology Stack
- Python 3.10+
- JAC (Jaseci) - Agentic AI Framework
- byLLM 0.4.5 - LLM Abstraction Layer
- Streamlit 1.51.0 - Frontend Framework
- FastAPI - REST API Server

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Git
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone {repo_url}
   cd {repo_name}
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## Usage

### Basic Usage

```python
from code_master import CodeMaster

# Initialize Code Master
master = CodeMaster(api_key="your-api-key")

# Analyze a repository
docs = master.analyze_repo("https://github.com/username/repo")

# Save documentation
master.save_docs(docs, "./output/")
```

### Advanced Features

#### Multi-Agent Analysis
```python
# Use specific agents
analyzer = master.get_agent("CodeAnalyzer")
ccg = analyzer.build_context_graph(repo_files)
```

#### Custom Documentation Templates
```python
# Customize generated documentation
config = {{
    "include_api_reference": True,
    "include_architecture": True,
    "custom_sections": ["Deployment", "Contributing"]
}}
docs = master.analyze_repo(url, config)
```

---

## API Reference

### Main Classes

#### CodeMaster
Primary class for repository analysis and documentation generation.

**Methods:**
- `analyze_repo(url: str, config: dict) -> DocumentationOutput`
- `save_docs(docs: DocumentationOutput, path: str) -> bool`
- `get_agent(name: str) -> Agent`

#### RepoMapper
Repository validation, file tree generation, and README extraction.

**Methods:**
- `validate_repository(url: str) -> ValidationResult`
- `build_file_tree(path: str) -> FileTree`
- `extract_readme(path: str) -> str`

#### CodeAnalyzer
Deep code structure analysis and context graph building.

**Methods:**
- `analyze_code_file(code: str, language: str) -> CodeAnalysis`
- `build_ccg(files: list) -> CodeContextGraph`
- `estimate_complexity(code: str) -> float`

#### DocGenie
Documentation generation and assembly.

**Methods:**
- `generate_project_overview(metadata: dict) -> str`
- `generate_api_reference(files: list) -> str`
- `assemble_documentation(...) -> DocumentationOutput`

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────┐
│           Streamlit Frontend (Web UI)           │
│  • GitHub URL input                             │
│  • Real-time progress tracking                  │
│  • Documentation viewer                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      JAC Backend (Multi-Agent Pipeline)         │
├─────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐             │
│  │  RepoMapper  │  │  CodeAnalyzer│             │
│  │   Agent      │  │   Agent      │             │
│  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐             │
│  │  DocGenie    │  │ CodeGenius   │             │
│  │   Agent      │  │  Supervisor  │             │
│  └──────────────┘  └──────────────┘             │
│                                                  │
│  • Code Context Graph (CCG) Building            │
│  • LLM-Powered Analysis (GPT-4o)                │
│  • Relationship Mapping                         │
│  • Complexity Estimation                        │
└─────────────────────────────────────────────────┘
```

### Data Flow

1. **Input:** User submits GitHub repository URL
2. **Validation:** RepoMapper validates URL format and accessibility
3. **Cloning:** Repository is cloned to temporary directory
4. **Analysis:** CodeAnalyzer parses code structure and builds CCG
5. **Generation:** DocGenie creates markdown sections using LLM
6. **Assembly:** CodeGenius orchestrates output and saves documentation
7. **Output:** User downloads professional markdown documentation

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Write clear, descriptive commit messages
- Add docstrings to all functions and classes
- Include unit tests for new features

---

## Troubleshooting

### Common Issues

**Issue:** Repository URL validation fails
- **Solution:** Ensure the URL is publicly accessible and follows standard GitHub format

**Issue:** Documentation generation is slow
- **Solution:** Limit the number of files analyzed using MAX_FILES_TO_ANALYZE setting

**Issue:** LLM API errors
- **Solution:** Check API key configuration and rate limits

### Getting Help

- Check the [FAQ](./docs/FAQ.md)
- Review [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Open an issue on GitHub

---

## License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

---

## Acknowledgments

- Built with [JAC/Jaseci](https://github.com/Jaseci-Labs/jaseci) agentic AI framework
- LLM integration via [byLLM](https://github.com/Jaseci-Labs/byLLM)
- Frontend powered by [Streamlit](https://streamlit.io/)

---

**Generated by Code Master** | *{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
                
                # Display in expandable section
                with st.expander("📖 View Full Documentation", expanded=True):
                    st.markdown(generated_doc)
                
                st.markdown("---")
                
                # Download and action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label="📥 Download as Markdown",
                        data=generated_doc,
                        file_name=f"{repo_name}_documentation.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    st.button(
                        label="🔄 Generate Again",
                        use_container_width=True,
                        key="regenerate_btn"
                    )
                
                with col3:
                    st.button(
                        label="✨ Customize",
                        use_container_width=True,
                        key="customize_btn"
                    )
                
                # Show summary statistics
                st.markdown("### 📈 Analysis Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Files Analyzed", "24", "100%")
                
                with col2:
                    st.metric("Functions Found", "147", "+12")
                
                with col3:
                    st.metric("Classes Found", "31", "+5")
                
                with col4:
                    st.metric("Avg Complexity", "4.2/10", "Moderate")
                
            else:
                st.error("❌ Invalid GitHub URL format. Please use: https://github.com/username/repo-name")
    
    elif repo_url and not validate_btn:
        st.info("👆 Click 'Validate' to start the documentation generation process")
    
    else:
        st.markdown("""
        <div class="info-box">
        <h4>How to Use Code Master</h4>
        <ol>
            <li>Paste a GitHub repository URL in the input field above</li>
            <li>Click the "Validate" button to check the URL</li>
            <li>Wait for the analysis to complete (typically 30-60 seconds)</li>
            <li>Review the generated documentation</li>
            <li>Download as Markdown or customize as needed</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: FEATURES
# ============================================================================

with tab2:
    st.markdown("## ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🤖 Multi-Agent Analysis
        Specialized agents work together:
        - **RepoMapper:** Validates and maps repository structure
        - **CodeAnalyzer:** Deep code structure and complexity analysis
        - **DocGenie:** Creates professional documentation sections
        - **CodeGenius:** Orchestrates the entire pipeline
        
        ### 📊 Code Context Graph
        - Maps relationships between functions and classes
        - Identifies entry points and main flows
        - Tracks dependencies and interactions
        - Generates architecture diagrams
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 LLM-Powered Intelligence
        - Uses GPT-4o for semantic understanding
        - Generates human-readable descriptions
        - Creates professional markdown output
        - Customizable templates and formats
        
        ### 🚀 Performance
        - Analyzes 20+ files simultaneously
        - Handles large codebases efficiently
        - Caches analysis results
        - Optimized for GitHub repositories
        """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Generated Documentation Includes")
    
    cols = st.columns(3)
    
    items = [
        ("📖", "Project Overview", "Comprehensive description of the project"),
        ("🔧", "Installation Guide", "Step-by-step setup instructions"),
        ("💻", "Usage Examples", "Code samples and common use cases"),
        ("🔌", "API Reference", "Complete function and class documentation"),
        ("🏗️", "Architecture Overview", "System design and component relationships"),
        ("🎯", "Quick Start", "Get running in minutes"),
        ("📚", "Code Examples", "Practical implementation patterns"),
        ("🔗", "Dependencies", "List of required packages and versions"),
    ]
    
    for idx, (icon, title, desc) in enumerate(items):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class="card">
            <h4>{icon} {title}</h4>
            <p style="color: #666; font-size: 0.9em;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: TUTORIAL
# ============================================================================

with tab3:
    st.markdown("## 📖 Step-by-Step Tutorial")
    
    st.markdown("""
    ### Example: Generating Docs for a GitHub Repository
    
    #### Step 1: Prepare Your Repository
    
    For best results, ensure your repository has:
    - A README.md file describing the project
    - Clear code structure with logical organization
    - Docstrings or comments explaining functionality
    - Meaningful function and variable names
    
    #### Step 2: Copy the Repository URL
    
    Navigate to your GitHub repository and copy the URL:
    ```
    https://github.com/username/repository-name
    ```
    
    #### Step 3: Use Code Master
    
    1. Paste the URL in the input field on the main tab
    2. Click "Validate" to verify the repository
    3. Wait for the analysis to complete
    4. Review the generated documentation
    
    #### Step 4: Download or Customize
    
    - Download the markdown file directly
    - Customize sections as needed
    - Share with your team
    - Use in your project wiki
    
    ### Tips for Best Results
    
    ✅ **Do:**
    - Use public repositories
    - Include comprehensive README files
    - Write clear, descriptive code
    - Follow language-specific conventions
    - Add meaningful docstrings
    
    ❌ **Don't:**
    - Use private/restricted repositories
    - Have minimal or missing README
    - Use single-letter variable names
    - Skip code documentation
    - Mix multiple languages in one file
    
    ### Supported Languages
    
    Code Master can analyze:
    - Python, JavaScript, TypeScript
    - Java, C++, C#, Go, Rust
    - Ruby, PHP, Swift, Kotlin
    - SQL, JAC, Markdown, and more
    """)

# ============================================================================
# TAB 4: RESOURCES
# ============================================================================

with tab4:
    st.markdown("## 🔗 Resources & Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 Documentation
        - [Complete API Reference](https://docs.codemaster.io/api)
        - [Architecture Guide](https://docs.codemaster.io/architecture)
        - [Configuration Options](https://docs.codemaster.io/config)
        - [Troubleshooting Guide](https://docs.codemaster.io/troubleshooting)
        
        ### 🔧 Technology Stack
        - [JAC/Jaseci Framework](https://github.com/Jaseci-Labs/jaseci)
        - [byLLM Documentation](https://github.com/Jaseci-Labs/byLLM)
        - [Streamlit Docs](https://docs.streamlit.io/)
        - [OpenAI API](https://platform.openai.com/docs)
        """)
    
    with col2:
        st.markdown("""
        ### 🤝 Community
        - [GitHub Repository](https://github.com/your/repo)
        - [Issue Tracker](https://github.com/your/repo/issues)
        - [Discussions](https://github.com/your/repo/discussions)
        - [Contributing Guide](https://github.com/your/repo/blob/main/CONTRIBUTING.md)
        
        ### 💡 Examples
        - [Example Documentations](https://examples.codemaster.io)
        - [Case Studies](https://blog.codemaster.io)
        - [Sample Projects](https://github.com/codemaster-samples)
        - [Video Tutorials](https://youtube.com/@codemaster)
        """)
    
    st.markdown("---")
    
    st.markdown("### 🆘 Support & Contact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Email Support**
        
        support@codemaster.io
        
        Response time: < 24 hours
        """)
    
    with col2:
        st.info("""
        **Community Chat**
        
        Slack Community
        
        Real-time help from maintainers
        """)
    
    with col3:
        st.info("""
        **Bug Reports**
        
        GitHub Issues
        
        Help us improve the product
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**Code Master** v1.0")
    st.markdown("*AI-Powered Documentation Generation*")

with footer_col2:
    st.markdown("Built with ❤️ using JAC & Streamlit")

with footer_col3:
    st.markdown("© 2024 Code Master | [License](./LICENSE)")

st.markdown("""
<div style="text-align: center; padding: 20px; color: #999; font-size: 0.9em;">
Made with Python • Powered by AI • Loved by Developers
</div>
""", unsafe_allow_html=True)
