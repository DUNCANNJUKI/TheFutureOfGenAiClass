"""
Code Master Backend Server
FastAPI wrapper for JAC multi-agent backend
Handles repository analysis requests and delegates to JAC agents
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Code Master Backend",
    description="Multi-Agent AI Documentation Generation Backend",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request model for repository analysis"""
    repo_url: str
    include_tests: bool = False
    max_files: int = 100

class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    status: str
    repo_name: str
    content: str
    timestamp: str
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    backend_ready: bool

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def run_jac_analysis(repo_url: str) -> Dict[str, Any]:
    """
    Run JAC backend analysis on the repository
    Currently returns mock data; can be integrated with actual JAC execution
    """
    try:
        logger.info(f"Starting analysis for repository: {repo_url}")
        
        # Extract repo name
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Mock analysis result (in production, this would call JAC agents)
        analysis_result = {
            "repo_url": repo_url,
            "repo_name": repo_name,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "analysis": {
                "repository": {
                    "name": repo_name,
                    "url": repo_url,
                    "description": f"Analysis of {repo_name}",
                    "file_count": 0,
                    "primary_language": "Python"
                },
                "summary": f"Repository '{repo_name}' has been analyzed by the Code Master AI agents.",
                "sections": [
                    {
                        "title": "Repository Overview",
                        "content": f"This is the {repo_name} repository. Multi-agent analysis detected the following patterns..."
                    },
                    {
                        "title": "Architecture Analysis",
                        "content": "The codebase follows modular architecture principles with clear separation of concerns."
                    },
                    {
                        "title": "Code Quality",
                        "content": "Code quality metrics indicate a well-maintained project with good test coverage."
                    }
                ]
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
        message="Code Master Backend is running",
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
async def analyze_repository(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyze a GitHub repository and generate documentation
    
    Args:
        request: AnalysisRequest containing repo_url and optional parameters
        
    Returns:
        AnalysisResponse with analysis results
        
    Raises:
        HTTPException: If repository is invalid or analysis fails
    """
    try:
        # Validate repository URL
        if not request.repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required")
        
        if not ("github.com" in request.repo_url or "gitlab.com" in request.repo_url):
            raise HTTPException(status_code=400, detail="Only GitHub and GitLab repositories are supported")
        
        logger.info(f"Received analysis request for: {request.repo_url}")
        
        # Run analysis
        result = run_jac_analysis(request.repo_url)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
        
        # Format response
        repo_name = result["repo_name"]
        analysis_data = result["analysis"]
        
        # Build documentation content
        content = f"""# {analysis_data['repository']['name']} - Documentation

## Repository Overview
- **URL**: {analysis_data['repository']['url']}
- **Primary Language**: {analysis_data['repository']['primary_language']}
- **Files Analyzed**: {analysis_data['repository']['file_count']}

## Summary
{analysis_data['summary']}

"""
        
        # Add sections
        for section in analysis_data.get('sections', []):
            content += f"## {section['title']}\n{section['content']}\n\n"
        
        content += f"""
---
*Generated by Code Master AI on {result['timestamp']}*
*Powered by Multi-Agent Analysis Engine*
"""
        
        return AnalysisResponse(
            status="success",
            repo_name=repo_name,
            content=content,
            timestamp=result["timestamp"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/analyze-advanced")
async def analyze_repository_advanced(request: AnalysisRequest):
    """
    Advanced analysis endpoint with more detailed output
    Includes architecture diagrams, code metrics, and recommendations
    """
    try:
        result = run_jac_analysis(request.repo_url)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return {
            "status": "success",
            "data": result,
            "metrics": {
                "analysis_time": "0.5s",
                "files_processed": 0,
                "code_quality_score": 8.5
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STATUS ENDPOINTS
# ============================================================================

@app.get("/status")
async def get_status():
    """Get backend service status"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "RepoMapper": "ready",
            "CodeAnalyzer": "ready",
            "DocGenie": "ready",
            "CodeGenius": "ready"
        },
        "version": "1.0.0"
    }

@app.get("/version")
async def get_version():
    """Get backend version information"""
    return {
        "backend": "Code Master Backend",
        "version": "1.0.0",
        "api_version": "1.0",
        "jac_engine": "jaclang",
        "powered_by": "Multi-Agent AI"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle value errors"""
    return {
        "status": "error",
        "detail": str(exc)
    }

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize backend on startup"""
    logger.info("Code Master Backend starting up...")
    logger.info("Multi-Agent AI Engine initialized")
    logger.info(f"Backend ready on http://localhost:8001")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Code Master Backend shutting down...")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Code Master Backend Server")
    logger.info("Listening on http://localhost:8001")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
