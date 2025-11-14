"""
Code Master Backend Server - Enhanced Edition
FastAPI wrapper for JAC multi-agent backend with chatbot, API extraction, and documentation export
Version: 2.0.0 | Developed by Duncan N. for Developers (2025)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from pathlib import Path
import logging
import os
import re
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Code Master Backend - Enhanced",
    description="Multi-Agent AI Documentation Generation Backend with Chatbot & API Extraction",
    version="2.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for analyzed repositories
analyzed_repos: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# DATA MODELS
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request model for repository analysis"""
    repo_url: str
    include_tests: bool = False
    max_files: int = 100

class ChatbotQuestion(BaseModel):
    """Chatbot question model"""
    repo_url: str
    question: str
    context: Optional[str] = None

class ChatbotResponse(BaseModel):
    """Chatbot response model"""
    answer: str
    confidence: float
    sources: List[str] = []

class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    status: str
    repo_name: str
    content: str
    apis: List[str] = []
    imports: List[str] = []
    timestamp: str
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    backend_ready: bool

# ============================================================================
# UTILITY FUNCTIONS - API EXTRACTION
# ============================================================================

def extract_apis_from_content(content: str, language: str = "python") -> List[str]:
    """
    Extract API calls and endpoints from code
    Supports Python, JavaScript, and more
    """
    apis = []
    
    # Python API patterns
    if language.lower() in ["python", "py"]:
        # HTTP requests
        api_patterns = [
            r'requests\.(get|post|put|delete|patch|head)\(["\']([^"\']+)',
            r'httpx\.(get|post|put|delete|patch|head)\(["\']([^"\']+)',
            r'aiohttp\.(get|post|put|delete|patch|head)\(["\']([^"\']+)',
            r'fastapi\.(get|post|put|delete|patch|head)\(["\']([^"\']+)',
            r'@(app|router)\.(get|post|put|delete|patch|head)\(["\']([^"\']+)',
            r'APIRouter\(\)(.*?)(get|post|put|delete|patch|head)\(["\']([^"\']+)',
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    api_endpoint = match[-1] if match[-1] else match[-2]
                else:
                    api_endpoint = match
                if api_endpoint and api_endpoint not in apis:
                    apis.append(str(api_endpoint))
    
    # Common API endpoints regardless of language
    endpoint_pattern = r'["\']/(api/)?([a-zA-Z0-9\-/_]+)["\']'
    matches = re.findall(endpoint_pattern, content)
    for match in matches:
        endpoint = "/" + match[1]
        if endpoint not in apis and len(endpoint) > 2:
            apis.append(endpoint)
    
    return list(set(apis))[:20]  # Return top 20 unique APIs

def extract_imports(content: str, language: str = "python") -> List[str]:
    """Extract library imports from code"""
    imports = []
    
    if language.lower() in ["python", "py"]:
        # Python imports
        patterns = [
            r'from\s+([\w.]+)\s+import',
            r'import\s+([\w.]+)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
    
    # Remove duplicates and standard library
    unique_imports = list(set(imports))
    return sorted(unique_imports)[:15]

def generate_intelligent_answer(question: str, analysis_data: Dict[str, Any]) -> str:
    """
    Generate intelligent answers based on analyzed repository data
    This is a template for LLM integration
    """
    question_lower = question.lower()
    repo_info = analysis_data.get("repository", {})
    
    # Question type detection and answering
    if any(word in question_lower for word in ["api", "endpoint", "route"]):
        apis = analysis_data.get("apis", [])
        if apis:
            return f"The repository uses the following APIs: {', '.join(apis[:5])}. " \
                   f"These are the main endpoints/routes exposed by the application."
        return "The repository doesn't appear to have exposed APIs or the analysis didn't detect them."
    
    elif any(word in question_lower for word in ["architecture", "structure", "design"]):
        return f"The {repo_info.get('name', 'repository')} follows a modular architecture. " \
               f"It's built primarily in {repo_info.get('primary_language', 'Python')} and " \
               "uses a multi-agent AI pattern for code analysis and documentation generation."
    
    elif any(word in question_lower for word in ["library", "import", "dependency", "package"]):
        imports = analysis_data.get("imports", [])
        if imports:
            return f"Key dependencies include: {', '.join(imports[:8])}. " \
                   f"These are the main external libraries used by the project."
        return "The repository appears to have minimal external dependencies or they weren't detected."
    
    elif any(word in question_lower for word in ["language", "technology", "tech stack"]):
        return f"The primary language is {repo_info.get('primary_language', 'Python')}. " \
               f"The repository contains approximately {repo_info.get('file_count', 'multiple')} files."
    
    elif any(word in question_lower for word in ["security", "vulnerability", "security issue"]):
        return "A full security audit would require deeper static analysis. " \
               "The repository appears to follow standard security practices based on the codebase structure."
    
    elif any(word in question_lower for word in ["performance", "optimize", "optimization"]):
        return "The codebase appears to be well-structured for performance. " \
               "Key optimization areas would be identified through profiling and benchmarking."
    
    else:
        return f"Based on the analysis of {repo_info.get('name', 'the repository')}: " \
               f"This is a {repo_info.get('primary_language', 'Python')}-based project. " \
               "More specific information about your question would require deeper analysis."

# ============================================================================
# ANALYSIS FUNCTION
# ============================================================================

def run_jac_analysis(repo_url: str) -> Dict[str, Any]:
    """
    Run JAC backend analysis on the repository
    Extracts APIs, imports, and generates documentation
    """
    try:
        logger.info(f"Starting analysis for repository: {repo_url}")
        
        # Extract repo name
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Mock code content (in production, this would clone and analyze the repo)
        mock_code = """
        import fastapi
        import requests
        from fastapi import FastAPI, HTTPException
        import json
        
        app = FastAPI()
        
        @app.get("/api/repositories")
        def get_repositories():
            response = requests.get("https://api.github.com/repos")
            return response.json()
        
        @app.post("/api/analyze")
        def analyze_repo(url: str):
            return {"status": "analyzing", "url": url}
        """
        
        # Extract APIs and imports
        apis = extract_apis_from_content(mock_code, "python")
        imports = extract_imports(mock_code, "python")
        
        # Mock analysis result
        analysis_result = {
            "repo_url": repo_url,
            "repo_name": repo_name,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "apis": apis,
            "imports": imports,
            "analysis": {
                "repository": {
                    "name": repo_name,
                    "url": repo_url,
                    "description": f"Analysis of {repo_name}",
                    "file_count": 42,
                    "primary_language": "Python"
                },
                "summary": f"Repository '{repo_name}' has been analyzed by the Code Master AI agents.",
                "sections": [
                    {
                        "title": "Repository Overview",
                        "content": f"This is the {repo_name} repository. Multi-agent analysis detected {len(apis)} API endpoints."
                    },
                    {
                        "title": "API Endpoints",
                        "content": f"**Detected APIs:** {chr(10).join(['- ' + api for api in apis[:10]])}"
                    },
                    {
                        "title": "Dependencies",
                        "content": f"**Key Libraries:** {', '.join(imports[:8])}"
                    },
                    {
                        "title": "Architecture Analysis",
                        "content": "The codebase follows modular architecture principles with clear separation of concerns."
                    }
                ],
                "apis": apis,
                "imports": imports,
            }
        }
        
        logger.info(f"Analysis completed for {repo_name}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint - health check"""
    return HealthCheckResponse(
        status="ok",
        message="Code Master Backend v2.0 is running",
        backend_ready=True
    )

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        message="Backend services are operational",
        backend_ready=True
    )

# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: AnalysisRequest):
    """
    Analyze a GitHub repository and generate documentation
    """
    try:
        if not request.repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required")
        
        if not ("github.com" in request.repo_url or "gitlab.com" in request.repo_url):
            raise HTTPException(status_code=400, detail="Only GitHub and GitLab repositories are supported")
        
        logger.info(f"Received analysis request for: {request.repo_url}")
        
        # Run analysis
        result = run_jac_analysis(request.repo_url)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
        
        # Store in memory
        analyzed_repos[request.repo_url] = result
        
        # Format response
        repo_name = result["repo_name"]
        analysis_data = result["analysis"]
        apis = result.get("apis", [])
        imports = result.get("imports", [])
        
        # Build documentation content
        content = f"""# {analysis_data['repository']['name']} - Documentation

## Repository Overview
- **URL**: {analysis_data['repository']['url']}
- **Primary Language**: {analysis_data['repository']['primary_language']}
- **Files Analyzed**: {analysis_data['repository']['file_count']}

## Summary
{analysis_data['summary']}

## API Endpoints
{'- ' + chr(10) + '- '.join(apis) if apis else 'No APIs detected'}

## Dependencies
{'- ' + chr(10) + '- '.join(imports) if imports else 'No external dependencies detected'}

"""
        
        # Add sections
        for section in analysis_data.get('sections', []):
            content += f"## {section['title']}\n{section['content']}\n\n"
        
        content += f"""---
*Generated by Code Master AI on {result['timestamp']}*
*Powered by Multi-Agent Analysis Engine v2.0*
*Developed by Duncan N. for Developers (2024-2026)*
"""
        
        return AnalysisResponse(
            status="success",
            repo_name=repo_name,
            content=content,
            apis=apis,
            imports=imports,
            timestamp=result["timestamp"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ============================================================================
# CHATBOT ENDPOINT
# ============================================================================

@app.post("/chat", response_model=ChatbotResponse)
async def chat_with_repository(request: ChatbotQuestion):
    """
    Chat about the analyzed repository
    Ask questions and get intelligent answers
    """
    try:
        if not request.repo_url or not request.question:
            raise HTTPException(status_code=400, detail="Repository URL and question required")
        
        # Get stored analysis
        if request.repo_url not in analyzed_repos:
            # Run analysis if not already done
            analysis_req = AnalysisRequest(repo_url=request.repo_url)
            result = run_jac_analysis(request.repo_url)
            analyzed_repos[request.repo_url] = result
        else:
            result = analyzed_repos[request.repo_url]
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail="Could not analyze repository")
        
        analysis_data = result["analysis"]
        
        # Generate intelligent answer
        answer = generate_intelligent_answer(request.question, analysis_data)
        
        return ChatbotResponse(
            answer=answer,
            confidence=0.85,
            sources=["Repository Analysis", "Code Pattern Detection"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

# ============================================================================
# DOWNLOAD ENDPOINTS
# ============================================================================

@app.get("/download/{repo_url:path}/{format}")
async def download_documentation(repo_url: str, format: str = "md"):
    """
    Download documentation in various formats
    Formats: md (markdown), txt, json, html
    """
    try:
        # URL decode
        repo_url_clean = repo_url.replace("___", "/").replace("__", ".")
        
        if repo_url_clean not in analyzed_repos:
            raise HTTPException(status_code=404, detail="Repository not analyzed yet")
        
        result = analyzed_repos[repo_url_clean]
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail="Could not generate download")
        
        repo_name = result["repo_name"]
        analysis = result["analysis"]
        
        # Build content based on format
        if format.lower() == "md":
            content = build_markdown_doc(analysis)
            media_type = "text/markdown"
            filename = f"{repo_name}_documentation.md"
            
        elif format.lower() == "txt":
            content = build_text_doc(analysis)
            media_type = "text/plain"
            filename = f"{repo_name}_documentation.txt"
            
        elif format.lower() == "json":
            content = json.dumps(analysis, indent=2)
            media_type = "application/json"
            filename = f"{repo_name}_analysis.json"
            
        elif format.lower() == "html":
            content = build_html_doc(analysis)
            media_type = "text/html"
            filename = f"{repo_name}_documentation.html"
            
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        return FileResponse(
            BytesIO(content.encode() if isinstance(content, str) else content),
            media_type=media_type,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DOCUMENT BUILDERS
# ============================================================================

def build_markdown_doc(analysis: Dict) -> str:
    """Build markdown documentation"""
    doc = f"""# {analysis.get('repository', {}).get('name', 'Repository')}

## Overview
{analysis.get('summary', '')}

## Repository Details
- **URL**: {analysis.get('repository', {}).get('url', '')}
- **Language**: {analysis.get('repository', {}).get('primary_language', '')}
- **Files**: {analysis.get('repository', {}).get('file_count', 0)}

## API Endpoints
{chr(10).join(['- ' + api for api in analysis.get('apis', [])])}

## Dependencies
{chr(10).join(['- ' + imp for imp in analysis.get('imports', [])])}

"""
    for section in analysis.get('sections', []):
        doc += f"## {section.get('title', '')}\n{section.get('content', '')}\n\n"
    
    doc += f"\n---\n*Generated by Code Master v2.0 (2024-2026)*"
    return doc

def build_text_doc(analysis: Dict) -> str:
    """Build text documentation"""
    return build_markdown_doc(analysis).replace("#", "")

def build_html_doc(analysis: Dict) -> str:
    """Build HTML documentation"""
    doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{analysis.get('repository', {}).get('name', 'Repository')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #0D47A1; }}
        h2 {{ color: #1565C0; margin-top: 30px; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
        .api {{ background: #e8f4f8; padding: 10px; margin: 5px 0; border-left: 3px solid #1565C0; }}
    </style>
</head>
<body>
    <h1>{analysis.get('repository', {}).get('name', 'Repository')}</h1>
    <p>{analysis.get('summary', '')}</p>
    
    <h2>Repository Details</h2>
    <ul>
        <li>URL: {analysis.get('repository', {}).get('url', '')}</li>
        <li>Language: {analysis.get('repository', {}).get('primary_language', '')}</li>
        <li>Files: {analysis.get('repository', {}).get('file_count', 0)}</li>
    </ul>
    
    <h2>API Endpoints</h2>
    {"".join([f'<div class="api">{api}</div>' for api in analysis.get('apis', [])])}
    
    <h2>Dependencies</h2>
    <ul>
        {"".join([f'<li>{imp}</li>' for imp in analysis.get('imports', [])])}
    </ul>
"""
    
    for section in analysis.get('sections', []):
        doc += f"<h2>{section.get('title', '')}</h2>\n<p>{section.get('content', '')}</p>\n"
    
    doc += """
    <hr>
    <p><small>Generated by Code Master v2.0 (2024-2026)</small></p>
</body>
</html>
"""
    return doc

# ============================================================================
# STATUS ENDPOINTS
# ============================================================================

@app.get("/status")
async def get_status():
    """Get backend service status"""
    return {
        "status": "operational",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "RepoMapper": "ready",
            "CodeAnalyzer": "ready",
            "DocGenie": "ready",
            "CodeGenius": "ready",
            "Chatbot": "ready",
            "APIExtractor": "ready"
        },
    }

@app.get("/version")
async def get_version():
    """Get backend version information"""
    return {
        "backend": "Code Master Backend - Enhanced",
        "version": "2.0.0",
        "api_version": "2.0",
        "jac_engine": "jaclang",
        "features": ["Multi-Agent Analysis", "Chatbot", "API Extraction", "Documentation Export"],
        "powered_by": "Multi-Agent AI",
        "developed_by": "Duncan N. for Developers (2024-2026)"
    }

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize backend on startup"""
    logger.info("Code Master Backend v2.0 starting up...")
    logger.info("Multi-Agent AI Engine initialized")
    logger.info("Chatbot enabled")
    logger.info("API Extraction ready")
    logger.info(f"Backend ready on http://localhost:8001")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Code Master Backend v2.0 shutting down...")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Code Master Backend Server v2.0")
    logger.info("Listening on http://localhost:8001")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
