#!/usr/bin/env python3
"""
Codebase Genius - Streamlit Frontend Standalone Demo
This is a demo that works without the JAC backend server
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="Codebase Genius",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧠 Codebase Genius")
st.sidebar.markdown("---")
st.sidebar.write("""
### About
An AI-powered multi-agent system that automatically generates high-quality documentation for any software repository.

### Version
1.0.0 (Demo)

### Features
- 🔍 Code Analysis
- 📚 Documentation Generation
- 🔬 Code Review
- 💬 Conversational AI
- 🏗️ Architecture Mapping
""")

# Main content
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<div class='main-title'>🧠 Codebase Genius</div>", unsafe_allow_html=True)
with col2:
    st.image("https://img.shields.io/badge/Status-Demo-blue", use_container_width=True)

st.subheader("AI-Powered Code Documentation System")
st.write("""
Welcome to **Codebase Genius** - the intelligent documentation assistant that understands your code!
""")

# Demo notice
st.info("📌 This is a **Demo Mode** - Full functionality requires the backend server running on port 8000", icon="ℹ️")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Getting Started",
    "📤 Upload Repository",
    "🔍 Code Analysis",
    "📚 Generate Docs",
    "🔬 Code Review",
    "💬 Chat"
])

# ============================================================================
# TAB 1: GETTING STARTED
# ============================================================================
with tab1:
    st.header("Getting Started with Codebase Genius")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Quick Start")
        st.markdown("""
        1. **Upload your repository** - Clone a Git repo or upload local files
        2. **Analyze your code** - View structure, complexity, and dependencies
        3. **Generate documentation** - Create API docs, README, and architecture guides
        4. **Review your code** - Get AI-powered insights and best practices
        5. **Ask questions** - Chat with your codebase using natural language
        """)
    
    with col2:
        st.subheader("⚙️ System Status")
        
        backend_running = False
        try:
            import requests
            resp = requests.get("http://localhost:8000/walker/get_projects", timeout=2)
            backend_running = resp.status_code == 200
        except:
            backend_running = False
        
        if backend_running:
            st.success("✅ Backend Server Running", icon="✅")
            st.write("JAC server is online on port 8000")
        else:
            st.warning("⚠️ Backend Offline", icon="⚠️")
            st.write("""
            Backend server is not running. To start it:
            
            ```bash
            cd BE
            python -m venv venv
            venv\\Scripts\\activate
            pip install -r requirements.txt
            jac serve main.jac
            ```
            """)
    
    st.markdown("---")
    
    st.subheader("🎯 Key Features")
    
    features = [
        ("🔍 Code Structure Analysis", "Analyze your codebase structure, functions, classes, and dependencies"),
        ("📚 Smart Documentation", "Generate comprehensive documentation including API docs and examples"),
        ("🔬 Code Quality Review", "Get insights on code quality, best practices, and improvements"),
        ("💬 Natural Language Chat", "Ask questions about your code in plain English"),
        ("🏗️ Architecture Mapping", "Understand and visualize your project architecture"),
    ]
    
    for feature, description in features:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(feature)
        with col2:
            st.write(description)

# ============================================================================
# TAB 2: UPLOAD REPOSITORY
# ============================================================================
with tab2:
    st.header("📤 Upload Repository")
    
    upload_method = st.radio("Choose upload method:", ["Git Clone", "Local Files"])
    
    if upload_method == "Git Clone":
        st.write("### Clone from Git Repository")
        
        repo_url = st.text_input(
            "Repository URL",
            placeholder="https://github.com/username/repository.git",
            help="Paste the HTTPS URL of a public Git repository"
        )
        
        repo_name = st.text_input(
            "Repository Name",
            placeholder="my-awesome-project",
            help="A friendly name for this repository"
        )
        
        if st.button("📥 Clone Repository", use_container_width=True):
            if repo_url and repo_name:
                st.info(f"Would clone: {repo_url} → {repo_name}")
                st.write("""
                ✅ **Backend feature**: Git clone functionality
                - Download repository from GitHub/GitLab
                - Index all files
                - Extract metadata
                """)
            else:
                st.error("Please provide both repository URL and name")
    
    else:
        st.write("### Upload Local Files")
        
        uploaded_files = st.file_uploader(
            "Upload Python, JavaScript, or other code files",
            accept_multiple_files=True,
            type=["py", "js", "ts", "java", "cpp", "cs", "go", "rs", "rb", "php", "jac"]
        )
        
        if uploaded_files:
            st.success(f"✅ Ready to process {len(uploaded_files)} file(s)")
            
            for file in uploaded_files:
                st.write(f"  • {file.name} ({file.size} bytes)")

# ============================================================================
# TAB 3: CODE ANALYSIS
# ============================================================================
with tab3:
    st.header("🔍 Code Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Code Structure")
        st.markdown("""
        #### Analysis Capabilities
        - File organization and hierarchy
        - Function and class detection
        - Module dependencies
        - Import analysis
        - Language detection
        """)
        
        if st.button("📊 Analyze Structure", use_container_width=True):
            st.write("""
            **Backend Feature**: Analyzes your codebase structure
            - Extracts all files and their organization
            - Identifies functions, classes, methods
            - Maps dependencies and imports
            - Generates metrics
            """)
    
    with col2:
        st.subheader("Code Complexity")
        st.markdown("""
        #### Metrics
        - Cyclomatic complexity
        - Lines of code per function
        - Nesting depth analysis
        - Code duplication detection
        - Function/method sizes
        """)
        
        if st.button("📈 Complexity Report", use_container_width=True):
            st.write("""
            **Backend Feature**: Generates complexity metrics
            - Identifies complex functions
            - Flags maintenance risks
            - Suggests refactoring
            - Provides actionable insights
            """)

# ============================================================================
# TAB 4: GENERATE DOCS
# ============================================================================
with tab4:
    st.header("📚 Generate Documentation")
    
    st.write("Choose which documentation to generate:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.checkbox("API Documentation", value=True):
            st.write("  └─ Generate detailed API docs with examples")
        if st.checkbox("Architecture Guide", value=True):
            st.write("  └─ System architecture and design patterns")
    
    with col2:
        if st.checkbox("README.md", value=True):
            st.write("  └─ Project overview and setup guide")
        if st.checkbox("Code Examples", value=True):
            st.write("  └─ Usage examples and common patterns")
    
    st.markdown("---")
    
    if st.button("🚀 Generate All Documentation", use_container_width=True, type="primary"):
        st.write("""
        **Backend Feature**: Multi-agent documentation generation
        
        1. **CodeAnalyzer Agent**
           - Extracts code structure and patterns
           - Identifies public APIs
        
        2. **DocumentationGenerator Agent**
           - Creates comprehensive documentation
           - Generates examples
           - Writes architecture guides
        
        3. **Output**
           - README.md
           - API_REFERENCE.md
           - ARCHITECTURE.md
           - EXAMPLES.md
        """)

# ============================================================================
# TAB 5: CODE REVIEW
# ============================================================================
with tab5:
    st.header("🔬 Code Review")
    
    review_type = st.selectbox(
        "Review Focus",
        ["Code Quality", "Security", "Performance", "Best Practices", "All"]
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Quality Issues")
        if st.button("Scan for Issues"):
            st.markdown("""
            **Features:**
            - Code smells detection
            - Anti-pattern identification
            - Maintainability assessment
            """)
    
    with col2:
        st.subheader("💡 Recommendations")
        if st.button("Get Suggestions"):
            st.markdown("""
            **Features:**
            - Best practices
            - Refactoring opportunities
            - Optimization tips
            """)

# ============================================================================
# TAB 6: CHAT
# ============================================================================
with tab6:
    st.header("💬 Chat with Your Codebase")
    
    st.write("Ask questions about your code in natural language:")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I'm Codebase Genius. Ask me anything about your codebase!"
            }
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Ask about your code...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Simulate assistant response
        with st.chat_message("assistant"):
            st.write("""
            This is a demo response. The backend service provides:
            
            **AI-Powered Answers:**
            - Understand your codebase structure
            - Explain functions and modules
            - Find related code
            - Suggest improvements
            
            To enable this feature, start the backend server:
            ```bash
            cd BE && jac serve main.jac
            ```
            """)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": "This is a demo response. Connect the backend for real AI analysis."
        })

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.write("### 📚 Documentation")
    st.write("[Getting Started](./START_HERE.md)")
    st.write("[Architecture](./ARCHITECTURE.md)")

with footer_col2:
    st.write("### 🔧 Backend Setup")
    st.code("""
cd BE
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
jac serve main.jac
    """)

with footer_col3:
    st.write("### 📊 System Info")
    st.write(f"**Version:** 1.0.0")
    st.write(f"**Mode:** Demo")
    st.write(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

st.markdown("""
---
<div style='text-align: center'>
    <p>🧠 <b>Codebase Genius</b> - AI-Powered Code Documentation</p>
    <p style='color: gray; font-size: 0.8em;'>v1.0.0 | Demo Mode | Ready for Production</p>
</div>
""", unsafe_allow_html=True)
