"""
The Code Master - Enhanced Frontend with Chatbot & Download
A sophisticated web application for generating professional documentation from GitHub repositories
Developed by Duncan N. for Developers (2025)
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time
from io import StringIO, BytesIO
import os
import base64

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="The Code Master v2.0 | AI-Powered Documentation",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING FOR HERO LAYOUT
# ============================================================================

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 50%, #FF6F00 100%) !important;
        min-height: 100vh;
        width: 100%;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 50%, #FF6F00 100%) !important;
    }
    
    .main {
        max-width: 100% !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] {
        background: rgba(13, 71, 161, 0.95) !important;
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(13, 71, 161, 0.9) 0%, rgba(21, 101, 192, 0.9) 50%, rgba(255, 111, 0, 0.9) 100%);
        padding: 80px 20px;
        text-align: center;
        color: white;
        margin: 0;
        width: 100%;
    }
    
    .hero-section h1 {
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-section p {
        font-size: 1.3em;
        margin-bottom: 10px;
        opacity: 0.95;
    }
    
    .hero-subtitle {
        font-size: 1.1em;
        opacity: 0.85;
        margin-bottom: 40px;
    }
    
    .content-wrapper {
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px 20px;
        width: 100%;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .feature-card h3 {
        color: #0D47A1;
        margin-bottom: 15px;
        font-size: 1.5em;
    }
    
    .feature-card p {
        color: #555;
        line-height: 1.6;
        font-size: 0.95em;
    }
    
    .input-section {
        background: white;
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .input-section h2 {
        color: #0D47A1;
        margin-bottom: 20px;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #1565C0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 1em !important;
    }
    
    .stButton > button {
        background-color: #FF6F00 !important;
        color: white !important;
        border: none !important;
        padding: 12px 40px !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        background-color: #E55100 !important;
        transform: scale(1.05) !important;
    }
    
    .output-container {
        background: white;
        border-radius: 12px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .success-message {
        background: #C8E6C9;
        border-left: 4px solid #00897B;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    .info-message {
        background: #BBDEFB;
        border-left: 4px solid #1565C0;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    .chat-message {
        background: #f9f9f9;
        border-left: 4px solid #1565C0;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .download-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 20px 0;
    }
    
    footer {
        text-align: center;
        padding: 20px;
        color: white;
        margin-top: 40px;
    }
    
    .tabs {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .tab-button {
        padding: 10px 20px;
        background: white;
        border: 2px solid #1565C0;
        border-radius: 8px;
        cursor: pointer;
        color: #0D47A1;
        font-weight: 600;
    }
    
    .tab-button.active {
        background: #1565C0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# BACKEND CONFIGURATION
# ============================================================================

BACKEND_URL = "http://localhost:8001"
MAX_RETRIES = 3
RETRY_DELAY = 1

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def check_backend_connection():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def analyze_repository(repo_url: str):
    """Analyze repository with retries"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={"repo_url": repo_url},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
            else:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        except:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return None

def chat_with_repo(repo_url: str, question: str):
    """Chat with repository chatbot"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"repo_url": repo_url, "question": question},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def download_documentation(repo_url: str, format_type: str = "md"):
    """Download documentation in specified format"""
    try:
        # Encode repo URL for use in path
        encoded_url = repo_url.replace("/", "___").replace(".", "__")
        response = requests.get(
            f"{BACKEND_URL}/download/{encoded_url}/{format_type}",
            timeout=30
        )
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None

# ============================================================================
# HERO SECTION
# ============================================================================

st.markdown("""
<div class="hero-section">
    <h1>📚 The Code Master v2.0</h1>
    <p>Automated Documentation Generation with AI Chatbot</p>
    <p class="hero-subtitle">Analyze GitHub Repos • Ask Questions • Download Documentation</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT WRAPPER
# ============================================================================

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# ============================================================================
# FEATURES SECTION
# ============================================================================

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3>⚙️ Multi-Agent AI</h3>
        <p>Analyze architecture, code patterns, and dependencies with specialized AI agents.</p>
    </div>
    <div class="feature-card">
        <h3>💬 Smart Chatbot</h3>
        <p>Ask questions about analyzed repositories and get intelligent, context-aware answers.</p>
    </div>
    <div class="feature-card">
        <h3>📊 API Extraction</h3>
        <p>Automatically detect and extract all API endpoints and external dependencies.</p>
    </div>
    <div class="feature-card">
        <h3>⚡ Fast Processing</h3>
        <p>Real-time analysis and instant documentation generation from GitHub URLs.</p>
    </div>
    <div class="feature-card">
        <h3>📥 Download Export</h3>
        <p>Export documentation as Markdown, PDF, HTML, or JSON for easy sharing.</p>
    </div>
    <div class="feature-card">
        <h3>🔍 Professional Output</h3>
        <p>Get comprehensive, well-structured documentation with all technical details.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CHECK BACKEND CONNECTION
# ============================================================================

col1, col2, col3 = st.columns(3)
with col1:
    backend_status = "✅ Connected" if check_backend_connection() else "❌ Disconnected"
    st.metric("Backend Status", backend_status)

with col2:
    st.metric("Version", "2.0.0")

with col3:
    st.metric("Updated", "2025")

# ============================================================================
# INPUT SECTION
# ============================================================================

st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h2>🚀 Start Your Analysis</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    github_url = st.text_input(
        "Enter GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed"
    )
with col2:
    submit_button = st.button("Analyze", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ANALYSIS & RESULTS
# ============================================================================

if submit_button and github_url:
    if not check_backend_connection():
        st.error("❌ Backend is not running. Please start the backend server on port 8001.")
    else:
        with st.spinner("🔍 Analyzing repository..."):
            data = analyze_repository(github_url)
        
        if data and data.get("status") == "success":
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.markdown('<h3>✅ Documentation Generated</h3>', unsafe_allow_html=True)
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.markdown(f"✅ Successfully analyzed: {github_url}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Store in session state for later use
            st.session_state.last_analysis = data
            st.session_state.last_repo_url = github_url
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📄 Documentation", "💬 Chatbot", "📊 APIs & Dependencies", "📥 Download"])
            
            # Tab 1: Documentation
            with tab1:
                if "content" in data:
                    st.markdown(data["content"])
            
            # Tab 2: Chatbot
            with tab2:
                st.subheader("Ask Me About This Repository")
                
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                # Display chat history
                for message in st.session_state.chat_history:
                    if message["role"] == "user":
                        st.write(f"**You:** {message['content']}")
                    else:
                        st.write(f"**Bot:** {message['content']}")
                
                # Chat input
                col1, col2 = st.columns([4, 1])
                with col1:
                    user_question = st.text_input(
                        "Ask a question about the repository:",
                        placeholder="What APIs does this project expose?",
                        key="chat_input"
                    )
                with col2:
                    ask_button = st.button("Ask", use_container_width=True)
                
                if ask_button and user_question:
                    st.session_state.chat_history.append({"role": "user", "content": user_question})
                    
                    with st.spinner("🤖 Thinking..."):
                        response = chat_with_repo(github_url, user_question)
                    
                    if response:
                        answer = response.get("answer", "Could not generate answer")
                        confidence = response.get("confidence", 0)
                        st.session_state.chat_history.append({"role": "bot", "content": answer})
                        st.markdown(f"**Bot:** {answer}")
                        st.caption(f"Confidence: {confidence:.0%}")
                    else:
                        st.error("Could not get response from chatbot")
            
            # Tab 3: APIs & Dependencies
            with tab3:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔌 Detected APIs")
                    apis = data.get("apis", [])
                    if apis:
                        for api in apis[:15]:
                            st.code(api, language="text")
                    else:
                        st.info("No APIs detected")
                
                with col2:
                    st.subheader("📦 Dependencies")
                    imports = data.get("imports", [])
                    if imports:
                        for imp in imports[:15]:
                            st.code(imp, language="text")
                    else:
                        st.info("No dependencies detected")
            
            # Tab 4: Download
            with tab4:
                st.subheader("📥 Download Documentation")
                st.write("Choose your preferred format:")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📄 Markdown", use_container_width=True):
                        content = download_documentation(github_url, "md")
                        if content:
                            st.download_button(
                                label="Download MD",
                                data=content,
                                file_name=f"{data['repo_name']}_docs.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Could not generate Markdown")
                
                with col2:
                    if st.button("📝 Text", use_container_width=True):
                        content = download_documentation(github_url, "txt")
                        if content:
                            st.download_button(
                                label="Download TXT",
                                data=content,
                                file_name=f"{data['repo_name']}_docs.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error("Could not generate Text")
                
                with col3:
                    if st.button("🌐 HTML", use_container_width=True):
                        content = download_documentation(github_url, "html")
                        if content:
                            st.download_button(
                                label="Download HTML",
                                data=content,
                                file_name=f"{data['repo_name']}_docs.html",
                                mime="text/html"
                            )
                        else:
                            st.error("Could not generate HTML")
                
                with col4:
                    if st.button("🔗 JSON", use_container_width=True):
                        content = download_documentation(github_url, "json")
                        if content:
                            st.download_button(
                                label="Download JSON",
                                data=content,
                                file_name=f"{data['repo_name']}_analysis.json",
                                mime="application/json"
                            )
                        else:
                            st.error("Could not generate JSON")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.error("❌ Failed to analyze repository. Please check the URL and try again.")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<footer>
    <p>The Code Master v2.0 - Powered by Multi-Agent AI</p>
    <p style="font-size: 0.9em; margin-top: 10px;">Developed by Duncan N. for Developers | 2025 | v2.0.0</p>
    <p style="font-size: 0.85em; margin-top: 5px;">Features: Multi-Agent Analysis • Smart Chatbot • API Extraction • Documentation Export</p>
</footer>
""", unsafe_allow_html=True)
