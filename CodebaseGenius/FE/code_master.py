"""
The Code Master - Automated Code Documentation System
A sophisticated web application for generating professional documentation from GitHub repositories
Developed by Duncan N. for Developers (2024-2025)
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="The Code Master | AI-Powered Documentation",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS STYLING FOR HERO LAYOUT
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
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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
    
    footer {
        text-align: center;
        padding: 20px;
        color: white;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero-section">
    <h1> The Code Master</h1>
    <p>Automated Documentation Generation</p>
    <p class="hero-subtitle">Transform Your GitHub Repositories into Professional Documentation Instantly</p>
</div>
""", unsafe_allow_html=True)

# MAIN CONTENT WRAPPER
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# FEATURES SECTION
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3> Multi-Agent AI</h3>
        <p>Powered by multiple specialized agents analyzing architecture, code patterns, and documentation needs.</p>
    </div>
    <div class="feature-card">
        <h3> Real-Time Processing</h3>
        <p>Get instant analysis and documentation generation from any GitHub repository URL.</p>
    </div>
    <div class="feature-card">
        <h3> Professional Output</h3>
        <p>Generate comprehensive, well-structured documentation with API references, architecture diagrams, and guides.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# INPUT SECTION
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h2>Start Your Documentation</h2>', unsafe_allow_html=True)

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

# BACKEND CONNECTION
BACKEND_URL = "http://localhost:8001"

if submit_button and github_url:
    st.markdown('<div class="info-message">', unsafe_allow_html=True)
    st.markdown(" Analyzing repository...", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"repo_url": github_url},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.markdown('<h3>Documentation Generated</h3>', unsafe_allow_html=True)
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.markdown(f" Successfully processed: {github_url}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if "content" in data:
                st.markdown(data["content"])
            else:
                st.json(data)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    
    except requests.exceptions.ConnectionError:
        st.markdown('<div class="output-container">', unsafe_allow_html=True)
        st.error("Backend Connection Failed")
        st.info("Make sure the backend is running on http://localhost:8001")
        st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<footer>
    <p>The Code Master - Powered by Multi-Agent AI</p>
    <p style="font-size: 0.9em; margin-top: 10px;">Developed by Duncan N. | 2024-2025</p>
</footer>
""", unsafe_allow_html=True)
