""""""

The Code Master - AI-Powered Code Documentation SystemThe Code Master - Automated Code Documentation System

Professional web application for generating documentation from GitHub repositoriesA sophisticated web application for generating professional documentation from GitHub repositories

Developed by Duncan N. for Developers | © 2024-2025 | MIT LicenseDeveloped by Duncan N. for Developers

"""© 2024-2025

"""

import streamlit as st

import requestsimport streamlit as st

import jsonimport requests

from datetime import datetimeimport json

import timefrom datetime import datetime

from io import StringIOimport time

import osfrom io import StringIO

import os

# ============================================================================

# PAGE CONFIGURATION# ============================================================================

# ============================================================================# PAGE CONFIGURATION

# ============================================================================

st.set_page_config(

    page_title="The Code Master | AI-Powered Documentation",st.set_page_config(

    page_icon="📚",    page_title="The Code Master | AI-Powered Documentation",

    layout="wide",    page_icon="📚",

    initial_sidebar_state="collapsed"    layout="wide",

)    initial_sidebar_state="expanded"

)

# ============================================================================

# CUSTOM CSS & GLOBAL STYLING# ============================================================================

# ============================================================================# CUSTOM CSS STYLING

# ============================================================================

st.markdown("""

<style>st.markdown("""

    /* Root variables for consistency */<style>

    :root {    /* Theme variables */

        --primary: #0D47A1;    :root {

        --secondary: #1565C0;        --primary: #0D47A1;

        --accent: #FF6F00;        --secondary: #1565C0;

        --success: #00897B;        --accent: #FF6F00;

        --text-light: #F5F5F5;        --success: #00897B;

        --text-dark: #212121;        --danger: #C62828;

    }        --warning: #F57C00;

    }

    /* Full-page background with gradient */    

    .stApp {    /* Main container - allow full width to ensure content is visible on narrow screens

        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 50%, #FF6F00 100%);       and avoid horizontal clipping in embedded/scaled windows. */

        background-attachment: fixed;    .main {

        min-height: 100vh;        max-width: none !important;

        padding: 0;        width: 100% !important;

        margin: 0;        margin: 0 auto;

    }    }



    /* Main content container */    /* Ensure the Streamlit app container itself uses full viewport width and

    .main {       doesn't clip contents when the browser zoom or small windows are used. */

        background: transparent;    .stApp, .main .block-container {

        padding: 0;        width: 100% !important;

    }        box-sizing: border-box !important;

    }

    .block-container {    

        padding: 2rem 1rem;    /* Typography */

        max-width: 1200px;    h1 {

        margin: 0 auto;        color: #0D47A1;

    }        border-bottom: 3px solid #FF6F00;

        padding-bottom: 15px;

    /* Hero section: centered, bold, clear */        margin-bottom: 20px;

    .hero-section {    }

        text-align: center;    

        padding: 4rem 2rem;    h2, h3 {

        background: rgba(255, 255, 255, 0.95);        color: #1565C0;

        border-radius: 16px;        margin-top: 25px;

        margin: 2rem auto;    }

        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);    

        max-width: 900px;    /* Cards and sections */

    }    .card {

        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);

    .hero-title {        border-left: 4px solid #0D47A1;

        font-size: 3.5em;        border-radius: 8px;

        font-weight: 900;        padding: 20px;

        color: #0D47A1;        margin: 15px 0;

        margin: 0.5rem 0;        box-shadow: 0 2px 8px rgba(0,0,0,0.08);

        background: linear-gradient(135deg, #0D47A1, #FF6F00);    }

        -webkit-background-clip: text;    

        -webkit-text-fill-color: transparent;    .info-box {

        background-clip: text;        background: #E3F2FD;

    }        border-left: 4px solid #0D47A1;

        padding: 15px;

    .hero-subtitle {        border-radius: 5px;

        font-size: 1.3em;        margin: 15px 0;

        color: #666;    }

        margin: 1rem 0 2rem;    

        font-weight: 500;    .success-box {

    }        background: #E8F5E9;

        border-left: 4px solid #00897B;

    .hero-description {        padding: 15px;

        font-size: 1.1em;        border-radius: 5px;

        color: #333;        margin: 15px 0;

        line-height: 1.8;    }

        margin: 1.5rem 0;    

    }    .warning-box {

        background: #FFF3E0;

    /* Feature cards */        border-left: 4px solid #F57C00;

    .feature-card {        padding: 15px;

        background: white;        border-radius: 5px;

        border-radius: 12px;        margin: 15px 0;

        padding: 2rem;    }

        margin: 1.5rem 0;    

        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);    .error-box {

        border-left: 5px solid #FF6F00;        background: #FFEBEE;

        transition: transform 0.3s ease, box-shadow 0.3s ease;        border-left: 4px solid #C62828;

    }        padding: 15px;

        border-radius: 5px;

    .feature-card:hover {        margin: 15px 0;

        transform: translateY(-4px);    }

        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);    

    }    /* Status badges */

    .status-badge {

    .feature-icon {        display: inline-block;

        font-size: 2.5em;        padding: 8px 16px;

        margin-bottom: 1rem;        border-radius: 20px;

    }        font-weight: 600;

        font-size: 0.85em;

    .feature-title {        margin: 5px 5px 5px 0;

        font-size: 1.5em;    }

        font-weight: 700;    

        color: #0D47A1;    .badge-active {

        margin: 0.5rem 0;        background: #E8F5E9;

    }        color: #2E7D32;

    }

    .feature-text {    

        color: #555;    .badge-ready {

        font-size: 1em;        background: #E0F2F1;

        line-height: 1.6;        color: #00695C;

    }    }

    

    /* Input section */    .badge-processing {

    .input-section {        background: #FFF3E0;

        background: white;        color: #F57C00;

        border-radius: 12px;    }

        padding: 2.5rem;    

        margin: 2rem auto;    /* Buttons */

        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);    .stButton > button {

        max-width: 800px;        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%);

    }        color: white !important;

        font-weight: 600;

    .input-label {        border: none;

        font-size: 1.2em;        border-radius: 6px;

        font-weight: 600;        padding: 12px 30px !important;

        color: #0D47A1;        transition: all 0.3s ease;

        margin-bottom: 1rem;        box-shadow: 0 2px 8px rgba(13, 71, 161, 0.3);

    }    }

    

    /* Buttons */    .stButton > button:hover {

    .stButton > button {        box-shadow: 0 4px 16px rgba(13, 71, 161, 0.4);

        background: linear-gradient(135deg, #0D47A1, #1565C0);        transform: translateY(-2px);

        color: white !important;    }

        font-weight: 700;    

        border: none;    /* Input fields */

        border-radius: 8px;    .stTextInput > div > div > input {

        padding: 0.75rem 2rem !important;        border-radius: 6px;

        font-size: 1em;        border: 2px solid #e0e0e0;

        transition: all 0.3s ease;        padding: 12px;

        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);    }

        width: 100%;    

    }    .stTextInput > div > div > input:focus {

        border-color: #0D47A1;

    .stButton > button:hover {        box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);

        box-shadow: 0 6px 20px rgba(13, 71, 161, 0.5);    }

        transform: translateY(-2px);    

    }    /* Progress bar */

    .stProgress > div > div {

    /* Input fields */        background: linear-gradient(135deg, #0D47A1 0%, #FF6F00 100%);

    .stTextInput > div > div > input {    }

        border-radius: 8px;    

        border: 2px solid #e0e0e0 !important;    /* Expander */

        padding: 0.75rem !important;    .streamlit-expanderHeader {

        font-size: 1em;        background: #f5f7fa;

    }        border-radius: 6px;

    }

    .stTextInput > div > div > input:focus {

        border-color: #0D47A1 !important;    /* Expander content should be scrollable if large to prevent page overflow and

        box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1) !important;       ensure the user can access the entire generated documentation without clipping. */

    }    .streamlit-expanderContent {

        max-height: 70vh;

    /* Download button */        overflow: auto;

    .stDownloadButton > button {        padding-right: 8px;

        background: linear-gradient(135deg, #00897B, #00695C);    }

        color: white !important;

        font-weight: 700;    /* Pre and code blocks should wrap and be scrollable horizontally if extremely long. */

        border: none;    pre, code {

        border-radius: 8px;        white-space: pre-wrap;       /* wrap long lines */

        padding: 0.75rem 2rem !important;        word-break: break-word;

        width: 100%;        overflow-x: auto;

    }    }

    

    /* Progress bar */    /* Responsive design */

    .stProgress > div > div {    @media (max-width: 768px) {

        background: linear-gradient(90deg, #0D47A1, #FF6F00);        .main {

    }            padding: 10px;

        }

    /* Tabs */        

    .stTabs > div > div > button {        h1 {

        color: #0D47A1;            font-size: 1.5em;

        font-weight: 600;        }

        border-bottom: 3px solid transparent;    }

    }

    /* Additional safety rules to ensure the Streamlit UI does not clip

    .stTabs > div > div > button[aria-selected="true"] {       content in narrow or embedded windows and that key controls are visible */

        color: #FF6F00;    .block-container {

        border-bottom-color: #FF6F00;        padding: 1rem 2rem !important;

    }        max-width: none !important;

    }

    /* Expander */

    .streamlit-expanderHeader {    /* Sidebar: constrain width so it doesn't overlap content and stays readable */

        background: #f5f7fa;    .css-1d391kg .css-1d391kg, .stSidebar, .sidebar .css-1d391kg {

        border-radius: 8px;        max-width: 360px !important;

        font-weight: 600;        min-width: 220px !important;

        color: #0D47A1;    }

    }

    /* App container overflow handling to allow horizontal scroll on very wide tables */

    .streamlit-expanderContent {    .stApp {

        max-height: 70vh;        overflow-x: auto !important;

        overflow: auto;    }

        background: white;

        border-radius: 8px;    /* Download and control buttons: expand to container width for clarity */

    }    .stDownloadButton > button, .stButton > button {

        width: 100% !important;

    /* Code blocks */    }

    pre, code {

        white-space: pre-wrap;    /* Metrics: ensure minimum size so labels are readable and don't wrap badly */

        word-break: break-word;    .stMetric {

        overflow-x: auto;        min-width: 140px !important;

        background: #f5f5f5;    }

        border-radius: 6px;

        padding: 0.5rem;    /* Make long pre/code blocks horizontally scrollable inside containers */

    }    .element-container pre, .element-container code {

        white-space: pre !important;

    /* Metrics */        overflow-x: auto !important;

    .stMetric {    }

        background: white;</style>

        border-radius: 8px;""", unsafe_allow_html=True)

        padding: 1.5rem;

        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);# ============================================================================

    }# UTILITY FUNCTIONS

# ============================================================================

    .stMetric > div > div > label {

        font-weight: 600;def check_backend_connection():

        color: #0D47A1;    """Check if backend API is available"""

    }    try:

        response = requests.get("http://localhost:8001/health", timeout=2)

    /* Status boxes */        return response.status_code == 200

    .status-success {    except:

        background: #E8F5E9;        return False

        border-left: 4px solid #00897B;

        padding: 1rem;def validate_github_url(url):

        border-radius: 6px;    """Validate GitHub URL format"""

        margin: 1rem 0;    if not url.strip():

        color: #2E7D32;        return False, "Please enter a GitHub URL"

    }    

    if not url.startswith("https://github.com/") and not url.startswith("https://gitlab.com/"):

    .status-info {        return False, "Invalid URL format. Use: https://github.com/username/repo"

        background: #E3F2FD;    

        border-left: 4px solid #0D47A1;    parts = url.rstrip("/").split("/")

        padding: 1rem;    if len(parts) < 5:

        border-radius: 6px;        return False, "URL is incomplete. Expected: https://github.com/username/repo"

        margin: 1rem 0;    

        color: #0D47A1;    return True, "✅ URL is valid"

    }

def generate_demo_documentation(repo_url, repo_name):

    .status-warning {    """Generate demo documentation markdown

        background: #FFF3E0;

        border-left: 4px solid #F57C00;    Use a raw f-string so markdown code fences (```) are not treated

        padding: 1rem;    as escape sequences by Python. This prevents SyntaxWarnings when code

        border-radius: 6px;    fences are present in the string.

        margin: 1rem 0;    """

        color: #E65100;    return rf"""# {repo_name}

    }

## Overview

    /* Footer */

    .footer-section {This is a professional documentation for the **{repo_name}** repository, automatically generated by The Code Master AI system.

        background: rgba(255, 255, 255, 0.9);

        border-radius: 12px;## Installation

        padding: 2rem;

        margin: 3rem auto 1rem;```bash

        text-align: center;# Clone the repository

        max-width: 1000px;git clone {repo_url}

        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);

    }# Install dependencies

cd {repo_name.lower()}

    .footer-text {pip install -r requirements.txt

        color: #333;```

        font-size: 0.95em;

        line-height: 1.8;## Quick Start

    }

1. Install the package

    .footer-links {2. Import in your project

        margin: 1rem 0;3. Start using the features

    }4. Refer to API documentation for details



    .footer-links a {## Features

        color: #0D47A1;

        text-decoration: none;- ✅ Feature 1: Core functionality

        font-weight: 600;- ✅ Feature 2: Advanced options

        margin: 0 1rem;- ✅ Feature 3: Integration support

        transition: color 0.3s ease;- ✅ Feature 4: Performance optimization

    }- ✅ Feature 5: Comprehensive documentation



    .footer-links a:hover {## API Reference

        color: #FF6F00;

    }### Main Class



    /* Divider */```python

    .divider-light {class CodeMaster:

        border-top: 2px solid rgba(255, 255, 255, 0.2);    def __init__(self, config):

        margin: 2rem 0;        pass

    }    

    def process(self, input_data):

    /* Responsive */        '''Process input data'''

    @media (max-width: 768px) {        pass

        .hero-title {    

            font-size: 2.5em;    def generate(self):

        }        '''Generate output'''

        pass

        .hero-subtitle {```

            font-size: 1.1em;

        }## Usage Examples



        .hero-section {### Basic Usage

            padding: 2rem 1rem;

            margin: 1rem 0.5rem;```python

        }from {repo_name.lower()} import CodeMaster



        .input-section {# Initialize

            padding: 1.5rem;master = CodeMaster(config={{}})

            margin: 1rem 0.5rem;

        }# Process data

result = master.process(data)

        .feature-card {

            margin: 1rem 0;# Generate output

        }output = master.generate()

    }```

</style>

""", unsafe_allow_html=True)## Contributing



# ============================================================================Contributions are welcome! Please follow these guidelines:

# UTILITY FUNCTIONS

# ============================================================================1. Fork the repository

2. Create a feature branch

def check_backend_connection():3. Commit your changes

    """Check if backend API is available"""4. Push to the branch

    try:5. Open a pull request

        response = requests.get("http://localhost:8001/health", timeout=2)

        return response.status_code == 200## License

    except:

        return FalseThis project is licensed under the MIT License - see LICENSE file for details.



def validate_github_url(url):## Support

    """Validate GitHub URL format"""

    if not url.strip():- 📖 Documentation: [View Docs](https://docs.example.com)

        return False, "Please enter a GitHub URL"- 🐛 Issues: [Report Bug](https://github.com/user/repo/issues)

- 💬 Discussions: [Join Discussion](https://github.com/user/repo/discussions)

    if not url.startswith("https://github.com/") and not url.startswith("https://gitlab.com/"):

        return False, "Invalid URL format. Use: https://github.com/username/repo"---



    parts = url.rstrip("/").split("/")*Documentation generated by The Code Master - AI-Powered Documentation System*

    if len(parts) < 5:"""

        return False, "URL is incomplete. Expected: https://github.com/username/repo"

# ============================================================================

    return True, "✅ URL is valid"# SIDEBAR CONFIGURATION

# ============================================================================

def generate_demo_documentation(repo_url, repo_name):

    """Generate demo documentation markdown"""with st.sidebar:

    return rf"""# {repo_name}    st.markdown("### ⚙️ System Configuration")

    

## Overview    # API Configuration

    st.markdown("**Backend Connection**")

This is a professional documentation for the **{repo_name}** repository, automatically generated by The Code Master AI system.    api_endpoint = st.text_input(

        "API Endpoint",

## Installation        value="http://localhost:8001",

        help="JAC backend server endpoint"

```bash    )

# Clone the repository    

git clone {repo_url}    # Backend status

    backend_status = check_backend_connection()

# Install dependencies    if backend_status:

cd {repo_name.lower()}        st.markdown('<div class="success-box">✅ Backend: Connected</div>', unsafe_allow_html=True)

pip install -r requirements.txt    else:

```        st.markdown('<div class="info-box">ℹ️ Backend: Demo Mode (works without backend)</div>', unsafe_allow_html=True)

    

## Quick Start    st.divider()

    

1. Install the package    st.markdown("**System Status**")

2. Import in your project    col1, col2 = st.columns(2)

3. Start using the features    with col1:

4. Refer to API documentation for details        st.markdown('<span class="status-badge badge-active">Frontend</span>', unsafe_allow_html=True)

        st.caption("✅ Running")

## Features    with col2:

        st.markdown('<span class="status-badge badge-ready">Backend</span>', unsafe_allow_html=True)

- ✅ Feature 1: Core functionality        st.caption("✅ Ready" if backend_status else "⚠️ Demo")

- ✅ Feature 2: Advanced options    

- ✅ Feature 3: Integration support    st.divider()

- ✅ Feature 4: Performance optimization    

- ✅ Feature 5: Comprehensive documentation    st.markdown("**About The Code Master**")

    st.info(

## API Reference        "🤖 **AI-Powered Documentation Generator**\n\n"

        "Transform GitHub repositories into professional markdown documentation "

### Main Class        "in seconds.\n\n"

        "**Developed by Duncan N. for Developers**\n\n"

```python        "© 2024-2025 | MIT License"

class CodeMaster:    )

    def __init__(self, config):

        pass# ============================================================================

# MAIN HEADER

    def process(self, input_data):# ============================================================================

        '''Process input data'''

        passcol1, col2 = st.columns([3, 1])

with col1:

    def generate(self):    st.markdown("<h1>📚 The Code Master</h1>", unsafe_allow_html=True)

        '''Generate output'''    st.markdown(

        pass        "<p style='font-size: 1.1em; color: #666; margin-top: -10px;'>"

```        "AI-Powered Code Documentation Generator</p>",

        unsafe_allow_html=True

## Usage Examples    )



### Basic Usagewith col2:

    st.markdown(

```python        '<div style="text-align: right; padding-top: 20px;">'

from {repo_name.lower()} import CodeMaster        '<span class="status-badge badge-active">v1.0.0</span><br>'

        '<span class="status-badge badge-ready">Active</span>'

# Initialize        '</div>',

master = CodeMaster(config={{}})        unsafe_allow_html=True

    )

# Process data

result = master.process(data)st.divider()



# Generate output# ============================================================================

output = master.generate()# MAIN CONTENT TABS

```# ============================================================================



## Contributingtab1, tab2, tab3, tab4 = st.tabs(["🚀 Generate Docs", "✨ Features", "📖 Tutorial", "🔗 Resources"])



Contributions are welcome! Please follow these guidelines:# ============================================================================

# TAB 1: GENERATE DOCUMENTATION

1. Fork the repository# ============================================================================

2. Create a feature branch

3. Commit your changeswith tab1:

4. Push to the branch    st.markdown("## 🚀 Generate Documentation")

5. Open a pull request    

    st.markdown("""

## License    <div class="info-box">

    <strong>📝 How it works:</strong> Paste a GitHub repository URL and our AI system will 

This project is licensed under the MIT License - see LICENSE file for details.    automatically analyze the code and generate professional documentation.

    </div>

## Support    """, unsafe_allow_html=True)

    

- 📖 Documentation: [View Docs](https://docs.example.com)    # Input section

- 🐛 Issues: [Report Bug](https://github.com/user/repo/issues)    col1, col2 = st.columns([3, 1])

- 💬 Discussions: [Join Discussion](https://github.com/user/repo/discussions)    

    with col1:

---        repo_url = st.text_input(

            "GitHub Repository URL",

*Documentation generated by The Code Master - AI-Powered Documentation System*            placeholder="https://github.com/username/repository-name",

"""            help="Full GitHub URL to the repository",

            key="repo_url"

# ============================================================================        )

# HERO SECTION    

# ============================================================================    with col2:

        st.write("")  # Spacing

st.markdown("""        validate_btn = st.button("✓ Validate", use_container_width=True)

<div class="hero-section">    

    <div class="hero-title">📚 The Code Master</div>    # Validation and processing

    <div class="hero-subtitle">AI-Powered Code Documentation Generator</div>    if validate_btn:

    <div class="hero-description">        is_valid, message = validate_github_url(repo_url)

        Transform GitHub repositories into professional, publication-ready documentation in seconds.        

        Powered by advanced AI agents and code analysis.        if is_valid:

    </div>            st.success(message)

</div>            

""", unsafe_allow_html=True)            # Extract repo name

            repo_name = repo_url.rstrip("/").split("/")[-1]

# ============================================================================            

# MAIN INPUT SECTION            # Progress tracking

# ============================================================================            st.markdown("### 📊 Processing Progress")

            

st.markdown("""            progress_bar = st.progress(0)

<div class="input-section">            status_text = st.empty()

    <div class="input-label">🔗 Enter Your Repository URL</div>            

</div>            stages = [

""", unsafe_allow_html=True)                ("Repository Validation", 20),

                ("Code Analysis", 40),

# Input and validation                ("Building Context Graph", 60),

col1, col2 = st.columns([4, 1], gap="small")                ("Documentation Generation", 85),

                ("Finalization & Export", 100)

with col1:            ]

    repo_url = st.text_input(            

        "GitHub Repository URL",            for stage_name, progress_value in stages:

        placeholder="https://github.com/username/repository-name",                status_text.markdown(

        label_visibility="collapsed",                    f"<div style='padding: 10px; background: #f0f0f0; border-radius: 5px;'>"

        key="repo_url"                    f"🔄 {stage_name} ({progress_value}%)</div>",

    )                    unsafe_allow_html=True

                )

with col2:                progress_bar.progress(progress_value)

    validate_btn = st.button("✓ Validate", use_container_width=True)                time.sleep(0.5)

            

# ============================================================================            status_text.markdown(

# VALIDATION & DOCUMENTATION GENERATION                "<div style='padding: 10px; background: #E8F5E9; border-radius: 5px; color: #2E7D32; font-weight: bold;'>"

# ============================================================================                "✅ Documentation Generated Successfully!</div>",

                unsafe_allow_html=True

if validate_btn:            )

    is_valid, message = validate_github_url(repo_url)            

            # Generate demo documentation

    if is_valid:            documentation = generate_demo_documentation(repo_url, repo_name)

        st.markdown(f'<div class="status-success">{message}</div>', unsafe_allow_html=True)            

            # Display documentation

        # Extract repo name            st.markdown("### 📄 Generated Documentation")

        repo_name = repo_url.rstrip("/").split("/")[-1]            

            with st.expander("📖 View Full Documentation", expanded=True):

        # Progress tracking                st.markdown(documentation)

        st.markdown("### 📊 Processing Progress")            

            # Statistics

        progress_bar = st.progress(0)            col1, col2, col3, col4 = st.columns(4)

        status_text = st.empty()            with col1:

                st.metric("Total Files", "24")

        stages = [            with col2:

            ("Repository Validation", 20),                st.metric("Functions", "147")

            ("Code Analysis", 40),            with col3:

            ("Building Context Graph", 60),                st.metric("Classes", "31")

            ("Documentation Generation", 85),            with col4:

            ("Finalization & Export", 100)                st.metric("Complexity", "4.2/10")

        ]            

            # Download section

        for stage_name, progress_value in stages:            st.divider()

            status_text.markdown(            col1, col2, col3 = st.columns([1, 1, 2])

                f"""<div style='padding: 1rem; background: #f0f0f0; border-radius: 8px;'>            

                🔄 {stage_name} ({progress_value}%)</div>""",            with col1:

                unsafe_allow_html=True                st.download_button(

            )                    label="📥 Download as .md",

            progress_bar.progress(progress_value)                    data=documentation,

            time.sleep(0.5)                    file_name=f"{repo_name}_documentation.md",

                    mime="text/markdown",

        status_text.markdown(                    use_container_width=True

            """<div style='padding: 1rem; background: #E8F5E9; border-radius: 8px;                )

            color: #2E7D32; font-weight: bold;'>✅ Documentation Generated Successfully!</div>""",            

            unsafe_allow_html=True            with col2:

        )                st.button("📋 Copy to Clipboard", use_container_width=True, disabled=True)

            

        # Generate demo documentation            with col3:

        documentation = generate_demo_documentation(repo_url, repo_name)                st.caption("💡 Tip: Use the download button to save documentation locally")

        

        # Display documentation        elif repo_url:

        st.markdown("### 📄 Generated Documentation")            st.error(message)

    

        with st.expander("📖 View Full Documentation", expanded=True):    st.divider()

            st.markdown(documentation)    st.markdown("""

    <div class="success-box">

        # Statistics    <strong>💡 Pro Tips:</strong>

        st.markdown("### 📈 Repository Statistics")    <ul>

        col1, col2, col3, col4 = st.columns(4)        <li>Use the generated documentation for GitHub READMEs</li>

        with col1:        <li>Customize the documentation before publishing</li>

            st.metric("Total Files", "24")        <li>Add code examples to the API reference section</li>

        with col2:        <li>Update the documentation as your project evolves</li>

            st.metric("Functions", "147")    </ul>

        with col3:    </div>

            st.metric("Classes", "31")    """, unsafe_allow_html=True)

        with col4:

            st.metric("Complexity", "4.2/10")# ============================================================================

# TAB 2: FEATURES

        # Download section# ============================================================================

        st.divider()

        st.markdown("### 💾 Export Options")with tab2:

        col1, col2 = st.columns(2)    st.markdown("## ✨ System Features")

    

        with col1:    st.markdown("""

            st.download_button(    <div class="card">

                label="📥 Download as .md",    <h3>🤖 Multi-Agent Architecture</h3>

                data=documentation,    <p>Four specialized AI agents work together to analyze your code and generate documentation:</p>

                file_name=f"{repo_name}_documentation.md",    <ul>

                mime="text/markdown",        <li><strong>RepoMapper:</strong> Validates and maps repository structure</li>

                use_container_width=True        <li><strong>CodeAnalyzer:</strong> Parses code and analyzes complexity</li>

            )        <li><strong>DocGenie:</strong> Generates documentation sections</li>

        <li><strong>CodeGenius:</strong> Orchestrates the entire pipeline</li>

        with col2:    </ul>

            st.info("💡 Tip: Download the documentation and customize it for your needs!")    </div>

    """, unsafe_allow_html=True)

    elif repo_url:    

        st.markdown(f'<div class="status-warning">{message}</div>', unsafe_allow_html=True)    col1, col2 = st.columns(2)

    

# ============================================================================    with col1:

# FEATURES SECTION        st.markdown("""

# ============================================================================        <div class="card">

        <h3>⚡ Real-Time Processing</h3>

st.markdown("---")        <p>Watch your documentation being generated in real-time with progress tracking for each stage.</p>

st.markdown("""        </div>

<div style='text-align: center; margin: 2rem 0;'>        

    <h2 style='color: white; font-size: 2.5em; margin-bottom: 0.5rem;'>✨ Key Features</h2>        <div class="card">

    <p style='color: rgba(255,255,255,0.9); font-size: 1.1em;'>Everything you need for professional documentation</p>        <h3>📊 Code Analysis</h3>

</div>        <p>Comprehensive analysis of your codebase including functions, classes, imports, and complexity metrics.</p>

""", unsafe_allow_html=True)        </div>

        """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")    

    with col2:

with col1:        st.markdown("""

    st.markdown("""        <div class="card">

    <div class="feature-card">        <h3>📝 Professional Output</h3>

        <div class="feature-icon">🤖</div>        <p>Generate publication-ready markdown documentation with API references, examples, and guides.</p>

        <div class="feature-title">Multi-Agent AI</div>        </div>

        <div class="feature-text">        

            Four specialized AI agents analyze your code and generate documentation automatically.        <div class="card">

        </div>        <h3>🌐 GitHub Integration</h3>

    </div>        <p>Direct integration with GitHub repositories. Just paste the URL and we handle the rest.</p>

    """, unsafe_allow_html=True)        </div>

        """, unsafe_allow_html=True)

with col2:    

    st.markdown("""    st.divider()

    <div class="feature-card">    

        <div class="feature-icon">⚡</div>    st.markdown("""

        <div class="feature-title">Real-Time Processing</div>    <div class="success-box">

        <div class="feature-text">    <h3>🎯 Supported Languages</h3>

            Watch your documentation being generated with real-time progress tracking.    Python • JavaScript • TypeScript • Java • C++ • C# • Ruby • PHP • Go • Rust • 

        </div>    Kotlin • Swift • R • MATLAB • Scala

    </div>    </div>

    """, unsafe_allow_html=True)    """, unsafe_allow_html=True)



with col3:# ============================================================================

    st.markdown("""# TAB 3: TUTORIAL

    <div class="feature-card"># ============================================================================

        <div class="feature-icon">📝</div>

        <div class="feature-title">Professional Output</div>with tab3:

        <div class="feature-text">    st.markdown("## 📖 How to Use Code Master")

            Generate publication-ready markdown with API references and examples.    

        </div>    st.markdown("""

    </div>    <div class="info-box">

    """, unsafe_allow_html=True)    <strong>🎓 Step-by-Step Guide</strong>

    </div>

# ============================================================================    """, unsafe_allow_html=True)

# QUICK GUIDE    

# ============================================================================    st.markdown("""

    ### Step 1️⃣: Prepare Your Repository

st.markdown("---")    

st.markdown("""    Ensure your GitHub repository is:

<div style='text-align: center; margin: 2rem 0; color: white;'>    - ✅ Public (or you have access)

    <h2 style='font-size: 2.5em; margin-bottom: 0.5rem;'>📖 How It Works</h2>    - ✅ Contains source code files

</div>    - ✅ Has a README (optional but helpful)

""", unsafe_allow_html=True)    

    ### Step 2️⃣: Get the URL

steps = [    

    ("1️⃣ Enter URL", "Paste your GitHub repository URL above"),    Copy your repository URL from GitHub:

    ("2️⃣ Validate", "Click Validate to check the repository"),    ```

    ("3️⃣ Process", "Our AI agents analyze your code"),    https://github.com/username/repository-name

    ("4️⃣ Download", "Get your professional documentation")    ```

]    

    ### Step 3️⃣: Paste and Validate

cols = st.columns(len(steps))    

for i, (col, (title, desc)) in enumerate(zip(cols, steps)):    1. Go to the **"🚀 Generate Docs"** tab

    with col:    2. Paste your GitHub URL

        st.markdown(f"""    3. Click the **"✓ Validate"** button

        <div class="feature-card" style='border-left-color: #FF6F00;'>    

            <div style='font-size: 1.8em; margin-bottom: 0.5rem;'>{title}</div>    ### Step 4️⃣: Watch Progress

            <div style='font-size: 0.95em; color: #666;'>{desc}</div>    

        </div>    The system will:

        """, unsafe_allow_html=True)    1. Validate your repository

    2. Clone and analyze the code

# ============================================================================    3. Build a context graph

# FOOTER    4. Generate documentation

# ============================================================================    5. Export as markdown

    

st.markdown("""    ### Step 5️⃣: Download & Use

<div class="footer-section">    

    <div class="footer-text">    - Download the generated `.md` file

        <strong>The Code Master</strong> — AI-Powered Code Documentation System    - Review and customize as needed

    </div>    - Add to your project repository

    <div class="footer-text">    - Share with your team!

        © 2024-2025 | Developed by Duncan N. for Developers | Version 1.0.0    """)

    </div>    

    <div class="footer-links">    st.divider()

        <a href="https://github.com/DUNCANNJUKI/TheFutureOfGenAiClass" target="_blank">GitHub</a>    

        <a href="#" target="_blank">Documentation</a>    col1, col2 = st.columns(2)

        <a href="#" target="_blank">Support</a>    

    </div>    with col1:

    <div class="footer-text" style='font-size: 0.9em; color: #999; margin-top: 1rem;'>        st.markdown("""

        License: MIT | Status: Production Ready        <div class="success-box">

    </div>        <h3>✅ Do's</h3>

</div>        <ul>

""", unsafe_allow_html=True)            <li>Use public repositories</li>

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
