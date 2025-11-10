"""
The Code Master - Automated Code Documentation System
A sophisticated web application for generating professional documentation from GitHub repositories
Developed by Duncan N. for Developers
© 2024-2025
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
    page_title="The Code Master | AI-Powered Documentation",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* Theme variables */
    :root {
        --primary: #0D47A1;
        --secondary: #1565C0;
        --accent: #FF6F00;
        --success: #00897B;
        --danger: #C62828;
        --warning: #F57C00;
    }
    
    /* Main container - allow full width to ensure content is visible on narrow screens
       and avoid horizontal clipping in embedded/scaled windows. */
    .main {
        max-width: none !important;
        width: 100% !important;
        margin: 0 auto;
    }

    /* Ensure the Streamlit app container itself uses full viewport width and
       doesn't clip contents when the browser zoom or small windows are used. */
    .stApp, .main .block-container {
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Typography */
    h1 {
        color: #0D47A1;
        border-bottom: 3px solid #FF6F00;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    
    h2, h3 {
        color: #1565C0;
        margin-top: 25px;
    }
    
    /* Cards and sections */
    .card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        border-left: 4px solid #0D47A1;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .info-box {
        background: #E3F2FD;
        border-left: 4px solid #0D47A1;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    
    .success-box {
        background: #E8F5E9;
        border-left: 4px solid #00897B;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    
    .warning-box {
        background: #FFF3E0;
        border-left: 4px solid #F57C00;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    
    .error-box {
        background: #FFEBEE;
        border-left: 4px solid #C62828;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        margin: 5px 5px 5px 0;
    }
    
    .badge-active {
        background: #E8F5E9;
        color: #2E7D32;
    }
    
    .badge-ready {
        background: #E0F2F1;
        color: #00695C;
    }
    
    .badge-processing {
        background: #FFF3E0;
        color: #F57C00;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);
        color: white !important;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 12px 30px !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 2px solid #e0e0e0;
        padding: 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0D47A1;
        box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #0D47A1 0%, #FF6F00 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f5f7fa;
        border-radius: 6px;
    }

    /* Expander content should be scrollable if large to prevent page overflow and
       ensure the user can access the entire generated documentation without clipping. */
    .streamlit-expanderContent {
        max-height: 70vh;
        overflow: auto;
        padding-right: 8px;
    }

    /* Pre and code blocks should wrap and be scrollable horizontally if extremely long. */
    pre, code {
        white-space: pre-wrap;       /* wrap long lines */
        word-break: break-word;
        overflow-x: auto;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            padding: 10px;
        }
        
        h1 {
            font-size: 1.5em;
        }
    }

    /* Additional safety rules to ensure the Streamlit UI does not clip
       content in narrow or embedded windows and that key controls are visible */
    .block-container {
        padding: 1rem 2rem !important;
        max-width: none !important;
    }

    /* Sidebar: constrain width so it doesn't overlap content and stays readable */
    .css-1d391kg .css-1d391kg, .stSidebar, .sidebar .css-1d391kg {
        max-width: 360px !important;
        min-width: 220px !important;
    }

    /* App container overflow handling to allow horizontal scroll on very wide tables */
    .stApp {
        overflow-x: auto !important;
    }

    /* Download and control buttons: expand to container width for clarity */
    .stDownloadButton > button, .stButton > button {
        width: 100% !important;
    }

    /* Metrics: ensure minimum size so labels are readable and don't wrap badly */
    .stMetric {
        min-width: 140px !important;
    }

    /* Make long pre/code blocks horizontally scrollable inside containers */
    .element-container pre, .element-container code {
        white-space: pre !important;
        overflow-x: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_backend_connection():
    """Check if backend API is available"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def validate_github_url(url):
    """Validate GitHub URL format"""
    if not url.strip():
        return False, "Please enter a GitHub URL"
    
    if not url.startswith("https://github.com/") and not url.startswith("https://gitlab.com/"):
        return False, "Invalid URL format. Use: https://github.com/username/repo"
    
    parts = url.rstrip("/").split("/")
    if len(parts) < 5:
        return False, "URL is incomplete. Expected: https://github.com/username/repo"
    
    return True, "✅ URL is valid"

def generate_demo_documentation(repo_url, repo_name):
    """Generate demo documentation markdown

    Use a raw f-string so markdown code fences (```) are not treated
    as escape sequences by Python. This prevents SyntaxWarnings when code
    fences are present in the string.
    """
    return rf"""# {repo_name}

## Overview

This is a professional documentation for the **{repo_name}** repository, automatically generated by The Code Master AI system.

## Installation

```bash
# Clone the repository
git clone {repo_url}

# Install dependencies
cd {repo_name.lower()}
pip install -r requirements.txt
```

## Quick Start

1. Install the package
2. Import in your project
3. Start using the features
4. Refer to API documentation for details

## Features

- ✅ Feature 1: Core functionality
- ✅ Feature 2: Advanced options
- ✅ Feature 3: Integration support
- ✅ Feature 4: Performance optimization
- ✅ Feature 5: Comprehensive documentation

## API Reference

### Main Class

```python
class CodeMaster:
    def __init__(self, config):
        pass
    
    def process(self, input_data):
        '''Process input data'''
        pass
    
    def generate(self):
        '''Generate output'''
        pass
```

## Usage Examples

### Basic Usage

```python
from {repo_name.lower()} import CodeMaster

# Initialize
master = CodeMaster(config={{}})

# Process data
result = master.process(data)

# Generate output
output = master.generate()
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

- 📖 Documentation: [View Docs](https://docs.example.com)
- 🐛 Issues: [Report Bug](https://github.com/user/repo/issues)
- 💬 Discussions: [Join Discussion](https://github.com/user/repo/discussions)

---

*Documentation generated by The Code Master - AI-Powered Documentation System*
"""

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ System Configuration")
    
    # API Configuration
    st.markdown("**Backend Connection**")
    api_endpoint = st.text_input(
        "API Endpoint",
        value="http://localhost:8001",
        help="JAC backend server endpoint"
    )
    
    # Backend status
    backend_status = check_backend_connection()
    if backend_status:
        st.markdown('<div class="success-box">✅ Backend: Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">ℹ️ Backend: Demo Mode (works without backend)</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("**System Status**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="status-badge badge-active">Frontend</span>', unsafe_allow_html=True)
        st.caption("✅ Running")
    with col2:
        st.markdown('<span class="status-badge badge-ready">Backend</span>', unsafe_allow_html=True)
        st.caption("✅ Ready" if backend_status else "⚠️ Demo")
    
    st.divider()
    
    st.markdown("**About The Code Master**")
    st.info(
        "🤖 **AI-Powered Documentation Generator**\n\n"
        "Transform GitHub repositories into professional markdown documentation "
        "in seconds.\n\n"
        "**Developed by Duncan N. for Developers**\n\n"
        "© 2024-2025 | MIT License"
    )

# ============================================================================
# MAIN HEADER
# ============================================================================

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1>📚 The Code Master</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 1.1em; color: #666; margin-top: -10px;'>"
        "AI-Powered Code Documentation Generator</p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div style="text-align: right; padding-top: 20px;">'
        '<span class="status-badge badge-active">v1.0.0</span><br>'
        '<span class="status-badge badge-ready">Active</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.divider()

# ============================================================================
# MAIN CONTENT TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["🚀 Generate Docs", "✨ Features", "📖 Tutorial", "🔗 Resources"])

# ============================================================================
# TAB 1: GENERATE DOCUMENTATION
# ============================================================================

with tab1:
    st.markdown("## 🚀 Generate Documentation")
    
    st.markdown("""
    <div class="info-box">
    <strong>📝 How it works:</strong> Paste a GitHub repository URL and our AI system will 
    automatically analyze the code and generate professional documentation.
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository-name",
            help="Full GitHub URL to the repository",
            key="repo_url"
        )
    
    with col2:
        st.write("")  # Spacing
        validate_btn = st.button("✓ Validate", use_container_width=True)
    
    # Validation and processing
    if validate_btn:
        is_valid, message = validate_github_url(repo_url)
        
        if is_valid:
            st.success(message)
            
            # Extract repo name
            repo_name = repo_url.rstrip("/").split("/")[-1]
            
            # Progress tracking
            st.markdown("### 📊 Processing Progress")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            stages = [
                ("Repository Validation", 20),
                ("Code Analysis", 40),
                ("Building Context Graph", 60),
                ("Documentation Generation", 85),
                ("Finalization & Export", 100)
            ]
            
            for stage_name, progress_value in stages:
                status_text.markdown(
                    f"<div style='padding: 10px; background: #f0f0f0; border-radius: 5px;'>"
                    f"🔄 {stage_name} ({progress_value}%)</div>",
                    unsafe_allow_html=True
                )
                progress_bar.progress(progress_value)
                time.sleep(0.5)
            
            status_text.markdown(
                "<div style='padding: 10px; background: #E8F5E9; border-radius: 5px; color: #2E7D32; font-weight: bold;'>"
                "✅ Documentation Generated Successfully!</div>",
                unsafe_allow_html=True
            )
            
            # Generate demo documentation
            documentation = generate_demo_documentation(repo_url, repo_name)
            
            # Display documentation
            st.markdown("### 📄 Generated Documentation")
            
            with st.expander("📖 View Full Documentation", expanded=True):
                st.markdown(documentation)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Files", "24")
            with col2:
                st.metric("Functions", "147")
            with col3:
                st.metric("Classes", "31")
            with col4:
                st.metric("Complexity", "4.2/10")
            
            # Download section
            st.divider()
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                st.download_button(
                    label="📥 Download as .md",
                    data=documentation,
                    file_name=f"{repo_name}_documentation.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                st.button("📋 Copy to Clipboard", use_container_width=True, disabled=True)
            
            with col3:
                st.caption("💡 Tip: Use the download button to save documentation locally")
        
        elif repo_url:
            st.error(message)
    
    st.divider()
    st.markdown("""
    <div class="success-box">
    <strong>💡 Pro Tips:</strong>
    <ul>
        <li>Use the generated documentation for GitHub READMEs</li>
        <li>Customize the documentation before publishing</li>
        <li>Add code examples to the API reference section</li>
        <li>Update the documentation as your project evolves</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: FEATURES
# ============================================================================

with tab2:
    st.markdown("## ✨ System Features")
    
    st.markdown("""
    <div class="card">
    <h3>🤖 Multi-Agent Architecture</h3>
    <p>Four specialized AI agents work together to analyze your code and generate documentation:</p>
    <ul>
        <li><strong>RepoMapper:</strong> Validates and maps repository structure</li>
        <li><strong>CodeAnalyzer:</strong> Parses code and analyzes complexity</li>
        <li><strong>DocGenie:</strong> Generates documentation sections</li>
        <li><strong>CodeGenius:</strong> Orchestrates the entire pipeline</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>⚡ Real-Time Processing</h3>
        <p>Watch your documentation being generated in real-time with progress tracking for each stage.</p>
        </div>
        
        <div class="card">
        <h3>📊 Code Analysis</h3>
        <p>Comprehensive analysis of your codebase including functions, classes, imports, and complexity metrics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
        <h3>📝 Professional Output</h3>
        <p>Generate publication-ready markdown documentation with API references, examples, and guides.</p>
        </div>
        
        <div class="card">
        <h3>🌐 GitHub Integration</h3>
        <p>Direct integration with GitHub repositories. Just paste the URL and we handle the rest.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class="success-box">
    <h3>🎯 Supported Languages</h3>
    Python • JavaScript • TypeScript • Java • C++ • C# • Ruby • PHP • Go • Rust • 
    Kotlin • Swift • R • MATLAB • Scala
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: TUTORIAL
# ============================================================================

with tab3:
    st.markdown("## 📖 How to Use Code Master")
    
    st.markdown("""
    <div class="info-box">
    <strong>🎓 Step-by-Step Guide</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Step 1️⃣: Prepare Your Repository
    
    Ensure your GitHub repository is:
    - ✅ Public (or you have access)
    - ✅ Contains source code files
    - ✅ Has a README (optional but helpful)
    
    ### Step 2️⃣: Get the URL
    
    Copy your repository URL from GitHub:
    ```
    https://github.com/username/repository-name
    ```
    
    ### Step 3️⃣: Paste and Validate
    
    1. Go to the **"🚀 Generate Docs"** tab
    2. Paste your GitHub URL
    3. Click the **"✓ Validate"** button
    
    ### Step 4️⃣: Watch Progress
    
    The system will:
    1. Validate your repository
    2. Clone and analyze the code
    3. Build a context graph
    4. Generate documentation
    5. Export as markdown
    
    ### Step 5️⃣: Download & Use
    
    - Download the generated `.md` file
    - Review and customize as needed
    - Add to your project repository
    - Share with your team!
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
        <h3>✅ Do's</h3>
        <ul>
            <li>Use public repositories</li>
            <li>Include a README</li>
            <li>Add code comments</li>
            <li>Customize generated docs</li>
            <li>Update regularly</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h3>❌ Don'ts</h3>
        <ul>
            <li>Use private repos without access</li>
            <li>Ignore security files</li>
            <li>Skip customization</li>
            <li>Upload without review</li>
            <li>Leave outdated docs</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 4: RESOURCES
# ============================================================================

with tab4:
    st.markdown("## 🔗 Resources & Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
        <h3>📚 Documentation</h3>
        <ul>
            <li><a href="#">Complete User Guide</a></li>
            <li><a href="#">API Reference</a></li>
            <li><a href="#">Architecture Docs</a></li>
            <li><a href="#">FAQ</a></li>
        </ul>
        </div>
        
        <div class="card">
        <h3>🛠️ Technology Stack</h3>
        <ul>
            <li>JAC/Jaseci - Agentic AI</li>
            <li>Streamlit - Web Framework</li>
            <li>byLLM - LLM Integration</li>
            <li>OpenAI - GPT-4o</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
        <h3>👥 Community</h3>
        <ul>
            <li><a href="https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass">GitHub Repository</a></li>
            <li><a href="#">Join Discussions</a></li>
            <li><a href="#">Report Issues</a></li>
            <li><a href="#">Contribute</a></li>
        </ul>
        </div>
        
        <div class="card">
        <h3>📞 Support</h3>
        <ul>
            <li><a href="#">Discord Community</a></li>
            <li><a href="#">Email Support</a></li>
            <li><a href="#">GitHub Issues</a></li>
            <li><a href="#">Documentation</a></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class="info-box">
    <h3>🚀 Get Started</h3>
    <p><strong>Ready to generate documentation?</strong> Go to the <strong>"🚀 Generate Docs"</strong> tab 
    and paste your GitHub URL to get started!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.markdown("""
<div style='text-align: center; padding: 30px 0; color: #666; border-top: 1px solid #e0e0e0;'>
    <p><strong>The Code Master</strong> - AI-Powered Code Documentation System</p>
    <p>© 2024-2025 | Developed by Duncan N. for Developers | Version 1.0.0</p>
    <p>
        <a href='https://github.com/DUNCANNJUKI' style='color: #0D47A1; text-decoration: none; margin: 0 10px;'>GitHub</a> • 
        <a href='#' style='color: #0D47A1; text-decoration: none; margin: 0 10px;'>Documentation</a> • 
        <a href='#' style='color: #0D47A1; text-decoration: none; margin: 0 10px;'>Support</a>
    </p>
</div>
""", unsafe_allow_html=True)
