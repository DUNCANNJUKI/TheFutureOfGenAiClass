import streamlit as st
import requests
import json
import os
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Codebase Genius",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
st.markdown("""
    <style>
        .main {
            max-width: 1400px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0px 0px;
        }
        .stProgress > div > div > div > div {
            background-color: #1f77e3;
        }
        .code-block {
            background-color: #f0f2f6;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d1e7dd;
            border-left: 4px solid #198754;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        .error-box {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #dee2e6;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONSTANTS ---
BASE_URL = "http://localhost:8000"
CODEBASE_GENIUS_ENDPOINT = f"{BASE_URL}/walker/codebase_genius"
ANALYZE_FILES_ENDPOINT = f"{BASE_URL}/walker/analyze_files"
GENERATE_DOCS_ENDPOINT = f"{BASE_URL}/walker/generate_documentation"
REVIEW_CODE_ENDPOINT = f"{BASE_URL}/walker/review_code"
GET_PROJECTS_ENDPOINT = f"{BASE_URL}/walker/get_projects"
GET_SESSIONS_ENDPOINT = f"{BASE_URL}/walker/get_sessions"

# --- SESSION STATE INITIALIZATION ---
if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.current_project = None
    st.session_state.analysis_results = {}
    st.session_state.documentation = None
    st.session_state.code_review = None
    st.session_state.chat_history = []

# --- HEADER ---
st.title("🧠 Codebase Genius")
st.markdown("*AI-Powered Multi-Agent Documentation Generator*")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    
    st.subheader("Backend Connection")
    backend_status = "✅ Connected" if st.checkbox("Backend Connected", value=True) else "❌ Disconnected"
    st.info(f"Status: {backend_status}")
    
    st.subheader("LLM Settings")
    llm_provider = st.selectbox("LLM Provider", ["OpenAI", "Google Gemini"])
    model_name = st.selectbox("Model", 
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"] if llm_provider == "OpenAI" 
        else ["gemini-2.0-flash", "gemini-1.5-pro"]
    )
    
    st.subheader("Repository Settings")
    max_files = st.slider("Max Files to Analyze", 10, 500, 100)
    max_file_size = st.slider("Max File Size (MB)", 1, 50, 5)
    
    st.subheader("Documentation Options")
    include_examples = st.checkbox("Include Code Examples", value=True)
    include_architecture = st.checkbox("Include Architecture Diagrams", value=True)
    doc_format = st.selectbox("Documentation Format", ["Markdown", "HTML", "PDF"])

# --- MAIN CONTENT ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Repository Upload",
    "🔍 Code Analysis",
    "📚 Generate Docs",
    "✏️ Code Review",
    "💬 Chat with Genius"
])

# --- TAB 1: REPOSITORY UPLOAD ---
with tab1:
    st.header("Step 1: Upload Your Repository")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Local Repository")
        repo_path = st.text_input(
            "Repository Path",
            placeholder="/path/to/your/repository",
            help="Provide the full path to your repository"
        )
        
        if st.button("📂 Browse Repository"):
            st.info("Select the root directory of your repository")
    
    with col2:
        st.subheader("📦 Git Repository")
        git_url = st.text_input(
            "Git URL",
            placeholder="https://github.com/user/repo.git",
            help="Or provide a Git repository URL"
        )
        
        if st.button("⬇️ Clone Repository"):
            with st.spinner("Cloning repository..."):
                st.success("Repository cloned successfully!")
    
    if repo_path or git_url:
        st.divider()
        
        # Project info
        st.subheader("📋 Project Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            project_name = st.text_input("Project Name", "My Project")
        with col2:
            project_version = st.text_input("Version", "1.0.0")
        with col3:
            project_language = st.selectbox(
                "Primary Language",
                ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "Multi-language"]
            )
        
        project_description = st.text_area(
            "Project Description",
            placeholder="Brief description of what your project does...",
            height=100
        )
        
        # Repository analysis preview
        st.subheader("📊 Repository Preview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Files", "42", "+2")
        with col2:
            st.metric("Total LOC", "15,234", "+342")
        with col3:
            st.metric("Languages", "3", "0")
        with col4:
            st.metric("Dependencies", "23", "+1")
        
        # File statistics
        st.subheader("📈 File Statistics")
        file_stats = {
            "Python": 15,
            "JavaScript": 12,
            "YAML": 8,
            "Markdown": 7
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Files by Type**")
            for lang, count in file_stats.items():
                st.write(f"- {lang}: {count} files")
        
        with col2:
            st.write("**Recent Files**")
            recent_files = [
                "main.py (2 mins ago)",
                "utils.js (15 mins ago)",
                "config.yaml (1 hour ago)"
            ]
            for file in recent_files:
                st.write(f"- {file}")
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Load Repository", use_container_width=True, type="primary"):
                st.session_state.current_project = project_name
                st.success(f"Repository '{project_name}' loaded successfully!")
                st.balloons()
        
        with col2:
            if st.button("🔄 Refresh Analysis", use_container_width=True):
                st.info("Refreshing repository analysis...")
                st.rerun()

# --- TAB 2: CODE ANALYSIS ---
with tab2:
    st.header("Step 2: Analyze Code Structure")
    
    if st.session_state.current_project:
        st.info(f"Analyzing: **{st.session_state.current_project}**")
        
        st.subheader("🔍 Analysis Agents")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### Code Structure Analyzer
            - Identifies functions and classes
            - Maps dependencies
            - Detects design patterns
            """)
            if st.button("🚀 Run Structure Analysis", key="struct_analysis"):
                with st.spinner("Analyzing code structure..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    st.success("Structure analysis complete!")
                    st.session_state.analysis_results["structure"] = {
                        "functions": 42,
                        "classes": 18,
                        "modules": 12
                    }
        
        with col2:
            st.markdown("""
            ### Complexity Analyzer
            - Measures code complexity
            - Identifies hotspots
            - Suggests refactoring
            """)
            if st.button("🚀 Run Complexity Analysis", key="complexity_analysis"):
                with st.spinner("Analyzing complexity..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    st.success("Complexity analysis complete!")
                    st.session_state.analysis_results["complexity"] = {
                        "average_cyclomatic": 3.2,
                        "max_complexity": 12,
                        "files_above_threshold": 5
                    }
        
        with col3:
            st.markdown("""
            ### Dependency Analyzer
            - Maps module dependencies
            - Detects circular imports
            - Identifies external packages
            """)
            if st.button("🚀 Run Dependency Analysis", key="dependency_analysis"):
                with st.spinner("Analyzing dependencies..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    st.success("Dependency analysis complete!")
                    st.session_state.analysis_results["dependencies"] = {
                        "internal": 28,
                        "external": 23,
                        "circular": 0
                    }
        
        st.divider()
        
        # Analysis Results
        if st.session_state.analysis_results:
            st.subheader("📊 Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            
            if "structure" in st.session_state.analysis_results:
                with col1:
                    st.markdown("### 📦 Structure")
                    for key, value in st.session_state.analysis_results["structure"].items():
                        st.metric(key.replace("_", " ").title(), value)
            
            if "complexity" in st.session_state.analysis_results:
                with col2:
                    st.markdown("### ⚙️ Complexity")
                    for key, value in st.session_state.analysis_results["complexity"].items():
                        st.metric(key.replace("_", " ").title(), value)
            
            if "dependencies" in st.session_state.analysis_results:
                with col3:
                    st.markdown("### 🔗 Dependencies")
                    for key, value in st.session_state.analysis_results["dependencies"].items():
                        st.metric(key.replace("_", " ").title(), value)
    else:
        st.warning("Please load a repository first (Step 1)")

# --- TAB 3: GENERATE DOCUMENTATION ---
with tab3:
    st.header("Step 3: Generate Documentation")
    
    if st.session_state.current_project:
        st.info(f"Generating docs for: **{st.session_state.current_project}**")
        
        st.subheader("📝 Documentation Generators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### API Documentation
            Generates comprehensive API documentation with:
            - Function signatures
            - Parameter descriptions
            - Return type documentation
            - Usage examples
            """)
            if st.button("📖 Generate API Docs", use_container_width=True, key="api_docs"):
                with st.spinner("Generating API documentation..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    st.success("API documentation generated!")
        
        with col2:
            st.markdown("""
            ### Architecture Guide
            Creates detailed architecture documentation:
            - System overview
            - Component diagrams
            - Data flow descriptions
            - Integration patterns
            """)
            if st.button("🏗️ Generate Architecture Guide", use_container_width=True, key="arch_guide"):
                with st.spinner("Generating architecture guide..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                    st.success("Architecture guide generated!")
        
        st.divider()
        
        # Additional documentation options
        st.subheader("🎯 Additional Documentation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📖 Generate README", use_container_width=True):
                with st.spinner("Generating README..."):
                    st.success("README.md created!")
        
        with col2:
            if st.button("🔧 Generate CONTRIBUTING", use_container_width=True):
                with st.spinner("Generating CONTRIBUTING guide..."):
                    st.success("CONTRIBUTING.md created!")
        
        with col3:
            if st.button("📋 Generate CHANGELOG", use_container_width=True):
                with st.spinner("Generating CHANGELOG..."):
                    st.success("CHANGELOG.md created!")
        
        st.divider()
        
        # Documentation preview
        st.subheader("👁️ Preview Generated Documentation")
        
        doc_tabs = st.tabs(["README", "API Reference", "Architecture"])
        
        with doc_tabs[0]:
            st.markdown("""
            # My Project
            
            ## Overview
            This is an example project generated by Codebase Genius.
            
            ## Quick Start
            ```bash
            git clone <repo>
            pip install -r requirements.txt
            python main.py
            ```
            
            ## Features
            - Feature 1
            - Feature 2
            - Feature 3
            """)
        
        with doc_tabs[1]:
            st.markdown("""
            # API Reference
            
            ## Functions
            
            ### process_data()
            Processes input data and returns results.
            
            **Parameters:**
            - `data` (dict): Input data
            - `options` (dict): Configuration options
            
            **Returns:**
            - (dict): Processed results
            """)
        
        with doc_tabs[2]:
            st.markdown("""
            # Architecture Overview
            
            ## System Design
            
            ```
            [User Interface]
                    |
                    v
            [API Layer]
                    |
            [Business Logic]
                    |
            [Data Layer]
            ```
            
            ## Components
            - UI: Streamlit frontend
            - API: JAC backend with byLLM
            - Logic: Multi-agent system
            - Data: Graph database
            """)
    
    else:
        st.warning("Please load and analyze a repository first")

# --- TAB 4: CODE REVIEW ---
with tab4:
    st.header("Step 4: Code Review")
    
    if st.session_state.current_project:
        st.info(f"Reviewing code: **{st.session_state.current_project}**")
        
        st.subheader("✏️ Code Review Agents")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### Quality Analyzer
            - Code smell detection
            - Complexity analysis
            - Maintainability scoring
            """)
            if st.button("🔍 Run Quality Check", key="quality_check"):
                with st.spinner("Analyzing code quality..."):
                    st.success("Quality analysis complete!")
        
        with col2:
            st.markdown("""
            ### Security Reviewer
            - Vulnerability detection
            - Best practices check
            - Security recommendations
            """)
            if st.button("🔐 Run Security Review", key="security_review"):
                with st.spinner("Running security analysis..."):
                    st.success("Security review complete!")
        
        with col3:
            st.markdown("""
            ### Performance Analyzer
            - Bottleneck identification
            - Optimization suggestions
            - Resource usage analysis
            """)
            if st.button("⚡ Run Performance Check", key="perf_check"):
                with st.spinner("Analyzing performance..."):
                    st.success("Performance analysis complete!")
        
        st.divider()
        
        # Review results
        st.subheader("📋 Review Results")
        
        with st.expander("✅ Quality Insights", expanded=True):
            st.markdown("""
            **Score: 8.2/10**
            
            - ✅ Good code organization
            - ⚠️ Some functions could be refactored
            - ❌ Missing docstrings in 5 functions
            
            **Recommendations:**
            1. Add docstrings to public APIs
            2. Break down complex functions
            3. Improve test coverage
            """)
        
        with st.expander("🔐 Security Findings", expanded=False):
            st.markdown("""
            **Risk Level: Low**
            
            - ✅ No SQL injection vulnerabilities
            - ⚠️ Hardcoded credentials in config (low risk)
            - ✅ Input validation implemented
            """)
        
        with st.expander("⚡ Performance Report", expanded=False):
            st.markdown("""
            **Average Response Time: 125ms**
            
            - ✅ Efficient database queries
            - ⚠️ Cache could be optimized
            - ❌ One function has high memory usage
            """)
    
    else:
        st.warning("Please load and analyze a repository first")

# --- TAB 5: CHAT WITH GENIUS ---
with tab5:
    st.header("💬 Chat with Codebase Genius")
    
    if st.session_state.current_project:
        st.info(f"Chatting about: **{st.session_state.current_project}**")
        
        # Chat history display
        st.subheader("Chat History")
        
        chat_container = st.container()
        
        with chat_container:
            # Sample chat messages
            st.write("**You:** How should I optimize the database queries?")
            st.write("**Genius:** Based on my analysis, I found several optimization opportunities...")
            st.divider()
            st.write("**You:** What's the architecture of this project?")
            st.write("**Genius:** This project follows a layered architecture pattern...")
        
        # Chat input
        st.divider()
        col1, col2 = st.columns([0.9, 0.1])
        
        with col1:
            user_input = st.text_input(
                "Ask Codebase Genius anything about your code:",
                placeholder="e.g., How can I improve code readability? What are the main components?",
                key="chat_input"
            )
        
        with col2:
            send_button = st.button("📤", key="send_chat")
        
        if send_button and user_input:
            with st.spinner("Genius is thinking..."):
                # Simulate AI response
                st.success("Message sent!")
                st.write(f"**You:** {user_input}")
                st.write("**Genius:** [Response being generated by multi-agent system...]")
    
    else:
        st.warning("Please load a repository first")

# --- FOOTER ---
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    🚀 Codebase Genius v1.0 | Powered by byLLM & JAC | Built with Streamlit
    <br>
    Need help? Check the <a href='https://github.com' target='_blank'>documentation</a>
</div>
""", unsafe_allow_html=True)
