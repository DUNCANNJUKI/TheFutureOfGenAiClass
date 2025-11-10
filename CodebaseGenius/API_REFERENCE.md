# Codebase Genius - API Reference

## Overview

The Codebase Genius backend exposes 6 main Walker functions via HTTP REST API. All endpoints run on `localhost:8000` by default.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production deployment, add authentication layer.

## Response Format

All responses are JSON:

```json
{
  "data": {},           // Response payload
  "status": "success",  // success, error, pending
  "message": "Description"
}
```

## Walkers (Endpoints)

### 1. Codebase Genius (Main Orchestrator)

**Endpoint:** `POST /walker/codebase_genius`

**Purpose:** Main orchestrator that routes tasks to appropriate agents

**Request Body:**

```json
{
  "action": "analyze|document|review|chat",
  "message": "User input or command",
  "project_id": "optional_project_id",
  "project_path": "/path/to/repository",
  "files_data": [
    {
      "path": "src/main.py",
      "name": "main.py",
      "ext": "py",
      "content": "code content here",
      "loc": 150
    }
  ]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | Yes | Action: analyze, document, review, or chat |
| `message` | string | Yes | Command or query |
| `project_id` | string | No | Existing project ID to operate on |
| `project_path` | string | No | Path to repository (for new projects) |
| `files_data` | array | No | File data for analysis |

**Response:**

```json
{
  "data": {
    "result": "analysis/documentation/review/response",
    "project_id": "node_id",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "status": "success",
  "message": "Task completed"
}
```

**Example Request (Analysis):**

```bash
curl -X POST http://localhost:8000/walker/codebase_genius \
  -H "Content-Type: application/json" \
  -d '{
    "action": "analyze",
    "message": "MyProject",
    "project_path": "/home/user/myproject",
    "files_data": [
      {
        "path": "src/main.py",
        "name": "main.py",
        "ext": "py",
        "content": "def hello(): print(\"Hello\")",
        "loc": 1
      }
    ]
  }'
```

**Example Request (Chat):**

```bash
curl -X POST http://localhost:8000/walker/codebase_genius \
  -H "Content-Type: application/json" \
  -d '{
    "action": "chat",
    "message": "What is the architecture of this project?",
    "project_id": "existing_project_node_id"
  }'
```

### 2. Analyze Files

**Endpoint:** `POST /walker/analyze_files`

**Purpose:** Analyze code structure, complexity, and dependencies

**Request Body:**

```json
{
  "project_id": "node_id_from_creation",
  "analysis_type": "structure|complexity|dependencies"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string | Yes | Project node ID |
| `analysis_type` | string | No | Type: structure, complexity, or dependencies |

**Response:**

```json
{
  "data": {
    "analysis": {
      "files_analyzed": 50,
      "total_loc": 5000,
      "languages": ["Python", "JavaScript"],
      "functions": 120,
      "avg_complexity": 3.5,
      "dependencies": ["django", "requests", "numpy"]
    },
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "status": "success",
  "message": "Analysis complete"
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/walker/analyze_files \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "abc123xyz",
    "analysis_type": "structure"
  }'
```

### 3. Generate Documentation

**Endpoint:** `POST /walker/generate_documentation`

**Purpose:** Generate comprehensive project documentation

**Request Body:**

```json
{
  "project_id": "node_id_from_analysis",
  "doc_types": ["api", "architecture", "readme", "contributing"]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string | Yes | Project node ID |
| `doc_types` | array | No | Types of docs to generate |

**Response:**

```json
{
  "data": {
    "documentation": {
      "api": "# API Documentation\n...",
      "architecture": "# Architecture\n...",
      "readme": "# README\n...",
      "contributing": "# Contributing\n..."
    },
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "status": "success",
  "message": "Documentation generated"
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/walker/generate_documentation \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "abc123xyz",
    "doc_types": ["api", "architecture", "readme"]
  }'
```

**Example Response (Shortened):**

```json
{
  "data": {
    "documentation": {
      "api": "# API Reference\n\n## Endpoints\n\n### GET /users\n...",
      "architecture": "# System Architecture\n\n## Overview\n...",
      "readme": "# Project Name\n\n## Description\n..."
    }
  },
  "status": "success"
}
```

### 4. Review Code

**Endpoint:** `POST /walker/review_code`

**Purpose:** Perform code quality, security, and performance review

**Request Body:**

```json
{
  "project_id": "node_id_from_analysis",
  "review_types": ["quality", "security", "performance"]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string | Yes | Project node ID |
| `review_types` | array | No | Types of review to perform |

**Response:**

```json
{
  "data": {
    "review": {
      "quality": {
        "issues": 12,
        "findings": [
          {
            "severity": "warning",
            "file": "src/main.py",
            "line": 42,
            "issue": "Unused variable 'x'"
          }
        ]
      },
      "security": {
        "issues": 3,
        "findings": [
          {
            "severity": "critical",
            "issue": "SQL injection vulnerability in query",
            "recommendation": "Use parameterized queries"
          }
        ]
      },
      "performance": {
        "issues": 5,
        "findings": [
          {
            "severity": "warning",
            "issue": "O(n²) algorithm in loop",
            "recommendation": "Optimize to O(n log n)"
          }
        ]
      }
    },
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "status": "success",
  "message": "Code review complete"
}
```

**Example Request:**

```bash
curl -X POST http://localhost:8000/walker/review_code \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "abc123xyz",
    "review_types": ["quality", "security"]
  }'
```

### 5. Get Sessions

**Endpoint:** `GET /walker/get_sessions`

**Purpose:** Retrieve all analysis sessions

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max sessions to return (default: 50) |
| `offset` | integer | No | Pagination offset (default: 0) |

**Response:**

```json
{
  "data": {
    "sessions": [
      {
        "session_id": "sess_123",
        "project_name": "MyProject",
        "timestamp": "2024-01-15T10:30:00Z",
        "history": [
          {
            "action": "analyze",
            "timestamp": "2024-01-15T10:30:00Z"
          },
          {
            "action": "document",
            "timestamp": "2024-01-15T10:35:00Z"
          }
        ]
      }
    ],
    "total": 25,
    "limit": 10,
    "offset": 0
  },
  "status": "success",
  "message": "Sessions retrieved"
}
```

**Example Request:**

```bash
curl "http://localhost:8000/walker/get_sessions?limit=10&offset=0"
```

### 6. Get Projects

**Endpoint:** `GET /walker/get_projects`

**Purpose:** Retrieve all analyzed projects

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max projects to return (default: 50) |
| `offset` | integer | No | Pagination offset (default: 0) |
| `language` | string | No | Filter by language (e.g., "Python") |

**Response:**

```json
{
  "data": {
    "projects": [
      {
        "project_id": "proj_123",
        "name": "MyProject",
        "description": "My awesome project",
        "path": "/home/user/myproject",
        "languages": ["Python", "JavaScript"],
        "files_analyzed": 50,
        "total_loc": 5000,
        "timestamp": "2024-01-15T10:30:00Z",
        "last_analyzed": "2024-01-15T10:35:00Z"
      }
    ],
    "total": 15,
    "limit": 10,
    "offset": 0
  },
  "status": "success",
  "message": "Projects retrieved"
}
```

**Example Request:**

```bash
curl "http://localhost:8000/walker/get_projects?limit=20&language=Python"
```

## Client Integration Examples

### Python Client

```python
import requests
import json

BASE_URL = "http://localhost:8000"

class CodebaseGeniusClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def analyze_project(self, project_path, files_data):
        """Analyze a project"""
        response = requests.post(
            f"{self.base_url}/walker/codebase_genius",
            json={
                "action": "analyze",
                "message": "Analyze project",
                "project_path": project_path,
                "files_data": files_data
            }
        )
        return response.json()
    
    def generate_docs(self, project_id, doc_types):
        """Generate documentation"""
        response = requests.post(
            f"{self.base_url}/walker/generate_documentation",
            json={
                "project_id": project_id,
                "doc_types": doc_types
            }
        )
        return response.json()
    
    def review_code(self, project_id, review_types):
        """Review code"""
        response = requests.post(
            f"{self.base_url}/walker/review_code",
            json={
                "project_id": project_id,
                "review_types": review_types
            }
        )
        return response.json()
    
    def chat(self, project_id, message):
        """Chat about project"""
        response = requests.post(
            f"{self.base_url}/walker/codebase_genius",
            json={
                "action": "chat",
                "message": message,
                "project_id": project_id
            }
        )
        return response.json()
    
    def get_sessions(self, limit=50, offset=0):
        """Get all sessions"""
        response = requests.get(
            f"{self.base_url}/walker/get_sessions",
            params={"limit": limit, "offset": offset}
        )
        return response.json()
    
    def get_projects(self, limit=50, offset=0, language=None):
        """Get all projects"""
        params = {"limit": limit, "offset": offset}
        if language:
            params["language"] = language
        response = requests.get(
            f"{self.base_url}/walker/get_projects",
            params=params
        )
        return response.json()

# Usage
client = CodebaseGeniusClient()

# Analyze project
result = client.analyze_project(
    "/path/to/project",
    [
        {
            "path": "main.py",
            "name": "main.py",
            "ext": "py",
            "content": "...",
            "loc": 100
        }
    ]
)
project_id = result["data"]["project_id"]

# Generate docs
docs = client.generate_docs(project_id, ["api", "readme"])
print(docs["data"]["documentation"]["api"])

# Review code
review = client.review_code(project_id, ["quality", "security"])
print(review["data"]["review"])

# Chat
response = client.chat(project_id, "What's the architecture?")
print(response["data"]["result"])

# List projects
projects = client.get_projects(limit=10)
for proj in projects["data"]["projects"]:
    print(f"{proj['name']}: {proj['total_loc']} LOC")
```

### JavaScript/Node.js Client

```javascript
const axios = require('axios');

class CodebaseGeniusClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.client = axios.create({
            baseURL: baseUrl,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async analyzeProject(projectPath, filesData) {
        try {
            const response = await this.client.post('/walker/codebase_genius', {
                action: 'analyze',
                message: 'Analyze project',
                project_path: projectPath,
                files_data: filesData
            });
            return response.data;
        } catch (error) {
            console.error('Analysis failed:', error.message);
            throw error;
        }
    }

    async generateDocs(projectId, docTypes) {
        const response = await this.client.post(
            '/walker/generate_documentation',
            {
                project_id: projectId,
                doc_types: docTypes
            }
        );
        return response.data;
    }

    async reviewCode(projectId, reviewTypes) {
        const response = await this.client.post(
            '/walker/review_code',
            {
                project_id: projectId,
                review_types: reviewTypes
            }
        );
        return response.data;
    }

    async chat(projectId, message) {
        const response = await this.client.post(
            '/walker/codebase_genius',
            {
                action: 'chat',
                message: message,
                project_id: projectId
            }
        );
        return response.data;
    }

    async getSessions(limit = 50, offset = 0) {
        const response = await this.client.get(
            '/walker/get_sessions',
            {
                params: { limit, offset }
            }
        );
        return response.data;
    }

    async getProjects(limit = 50, offset = 0, language = null) {
        const params = { limit, offset };
        if (language) params.language = language;
        
        const response = await this.client.get(
            '/walker/get_projects',
            { params }
        );
        return response.data;
    }
}

// Usage
const client = new CodebaseGeniusClient();

(async () => {
    // Analyze
    const result = await client.analyzeProject('/path/to/project', [
        {
            path: 'main.py',
            name: 'main.py',
            ext: 'py',
            content: '...',
            loc: 100
        }
    ]);
    const projectId = result.data.project_id;

    // Generate docs
    const docs = await client.generateDocs(projectId, ['api', 'readme']);
    console.log(docs.data.documentation.api);

    // Chat
    const response = await client.chat(projectId, "What's the architecture?");
    console.log(response.data.result);

    // List projects
    const projects = await client.getProjects(10);
    projects.data.projects.forEach(proj => {
        console.log(`${proj.name}: ${proj.total_loc} LOC`);
    });
})();
```

## Error Handling

### Error Response Format

```json
{
  "data": {},
  "status": "error",
  "message": "Detailed error message"
}
```

### Common Error Codes

| Status | Message | Cause | Solution |
|--------|---------|-------|----------|
| 400 | Invalid request | Missing or invalid parameters | Check request body |
| 404 | Project not found | Invalid project_id | Verify project exists |
| 500 | Internal server error | Backend error | Check server logs |
| 503 | Service unavailable | Backend down | Restart server |

### Example Error Handling (Python)

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/walker/codebase_genius",
        json={"action": "analyze"}
    )
    response.raise_for_status()
    data = response.json()
    
    if data["status"] == "error":
        print(f"API Error: {data['message']}")
    else:
        print(f"Success: {data['data']}")
        
except requests.exceptions.ConnectionError:
    print("Cannot connect to backend")
except requests.exceptions.Timeout:
    print("Request timeout")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

## Rate Limiting and Throttling

Currently no rate limiting. For production:

```python
# Add this to backend
from functools import wraps
from time import time

def rate_limit(max_calls=10, time_window=60):
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            calls[:] = [c for c in calls if c > now - time_window]
            
            if len(calls) >= max_calls:
                return {"status": "error", "message": "Rate limit exceeded"}
            
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

## Pagination

Use `limit` and `offset` for large result sets:

```bash
# Get first 10
curl "http://localhost:8000/walker/get_projects?limit=10&offset=0"

# Get next 10
curl "http://localhost:8000/walker/get_projects?limit=10&offset=10"

# Get all with small batches
for offset in {0,10,20,30,...}; do
    curl "http://localhost:8000/walker/get_projects?limit=10&offset=$offset"
done
```

## Webhook Integration (Advanced)

For async processing:

```python
# In client code
import json
import subprocess

def analyze_and_notify(project_path, webhook_url):
    """Analyze and POST results to webhook"""
    result = client.analyze_project(project_path, [])
    
    # POST result to webhook
    requests.post(webhook_url, json=result)
```

## Performance Optimization

### Batch Processing

```python
# Process multiple projects efficiently
projects = [
    "/path/to/project1",
    "/path/to/project2",
    "/path/to/project3"
]

for project in projects:
    result = client.analyze_project(project, [])
    # Save results
    # Rate limit if needed
    time.sleep(1)
```

### Caching

```python
# Cache results locally
import json
from pathlib import Path

cache_dir = Path("./cache")

def get_project_with_cache(project_id):
    cache_file = cache_dir / f"{project_id}.json"
    
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    
    result = client.get_projects()
    cache_file.write_text(json.dumps(result))
    return result
```

## Testing API

### Using Postman

1. Import collection
2. Set base URL: `http://localhost:8000`
3. Test endpoints
4. Save responses

### Using pytest

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_get_projects():
    response = requests.get(f"{BASE_URL}/walker/get_projects")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_analyze_project():
    response = requests.post(
        f"{BASE_URL}/walker/codebase_genius",
        json={
            "action": "analyze",
            "message": "test",
            "project_path": "/tmp/test",
            "files_data": []
        }
    )
    assert response.status_code in [200, 500]  # Accept response or error
```

---

**API Reference Complete!**

See also:
- [Architecture Guide](ARCHITECTURE.md) - Detailed walker specifications
- [Getting Started](GETTING_STARTED.md) - Quick API examples
- [Deployment Guide](DEPLOYMENT.md) - Production setup
