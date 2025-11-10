# Codebase Genius - Architecture Document

## System Design Overview

Codebase Genius is built on an agentic AI architecture that leverages multiple specialized agents to analyze code repositories and generate comprehensive documentation automatically.

## Core Architecture Patterns

### 1. Multi-Agent Orchestration Pattern

```
User Request
     |
     v
┌────────────────┐
│ Orchestrator   │
│  (Router)      │
└────┬───────────┘
     |
     ├──────────────┬──────────────┬──────────────┐
     |              |              |              |
     v              v              v              v
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│  Analyzer  │ │  Doc Gen   │ │  Reviewer  │ │   Chat     │
│   Agent    │ │   Agent    │ │   Agent    │ │   Agent    │
└────┬───────┘ └────┬───────┘ └────┬───────┘ └────┬───────┘
     |              |              |              |
     └──────────────┴──────────────┴──────────────┘
                    |
                    v
            ┌──────────────────┐
            │  Knowledge Base  │
            │  (Graph DB)      │
            └──────────────────┘
```

### 2. ReAct Agent Framework

Each agent uses the **ReAct** (Reasoning + Acting) pattern:

```
┌─────────────────────────────────────────┐
│          ReAct Agent Cycle               │
├─────────────────────────────────────────┤
│                                         │
│  1. THINK                               │
│     └─ Analyze task requirements        │
│                                         │
│  2. ACT                                 │
│     └─ Call appropriate tools           │
│                                         │
│  3. OBSERVE                             │
│     └─ Evaluate tool results            │
│                                         │
│  4. DECIDE                              │
│     └─ Continue or complete             │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Session & State Management

```
┌──────────────────────────────────────────────┐
│         Session Management                    │
├──────────────────────────────────────────────┤
│                                              │
│  Session {                                   │
│    - history: List[str]                      │
│    - created_at: timestamp                   │
│    - project_id: reference                   │
│    - metadata: dict                          │
│  }                                           │
│                                              │
│  Memory Node {                               │
│    - sessions: List[Session]                 │
│    - global_state: dict                      │
│  }                                           │
│                                              │
└──────────────────────────────────────────────┘
```

## Agent Architecture

### Code Analyzer Agent

**Purpose:** Understand code structure and extract meaningful information

**Workflow:**

```
Input: Code File
  |
  ├─→ Extract Functions/Classes
  |      └─→ Identify signatures
  |      └─→ Map relationships
  |
  ├─→ Analyze Structure
  |      └─→ Module organization
  |      └─→ Design patterns
  |
  ├─→ Measure Complexity
  |      └─→ Cyclomatic complexity
  |      └─→ Cognitive complexity
  |
  ├─→ Extract Dependencies
  |      └─→ Internal imports
  |      └─→ External packages
  |
  v
Output: Structured Analysis Data
```

**Tools Used:**
- AST/syntax analysis (via LLM understanding)
- Pattern recognition
- Dependency extraction

**Semantic Instructions:**
```
"Analyze the code and provide:
1. High-level overview
2. Main classes, modules, or functions
3. Architecture patterns
4. Dependencies and imports"
```

### Documentation Generator Agent

**Purpose:** Create comprehensive, professional documentation

**Workflow:**

```
Input: Code Analysis + Project Info
  |
  ├─→ Generate API Docs
  |      └─→ Function signatures
  |      └─→ Parameter descriptions
  |      └─→ Return types
  |
  ├─→ Create Usage Examples
  |      └─→ Basic usage
  |      └─→ Advanced patterns
  |      └─→ Error handling
  |
  ├─→ Build Architecture Overview
  |      └─→ System design
  |      └─→ Component relationships
  |      └─→ Data flow
  |
  ├─→ Format README
  |      └─→ Project description
  |      └─→ Installation guide
  |      └─→ Quick start
  |
  v
Output: Complete Documentation Set
```

**Semantic Instructions:**
```
"Generate professional documentation including:
- Clear API documentation
- Practical code examples
- Architecture diagrams
- Contributing guidelines"
```

### Code Reviewer Agent

**Purpose:** Identify issues and suggest improvements

**Workflow:**

```
Input: Code File + Analysis
  |
  ├─→ Identify Issues
  |      └─→ Bugs and errors
  |      └─→ Security concerns
  |      └─→ Performance issues
  |
  ├─→ Suggest Improvements
  |      └─→ Code readability
  |      └─→ Maintainability
  |      └─→ Performance optimization
  |
  ├─→ Check Best Practices
  |      └─→ Language conventions
  |      └─→ Design patterns
  |      └─→ Error handling
  |
  v
Output: Comprehensive Review Report
```

## Data Model

### Node Types

```jac
node CodeFile {
    filepath: str
    filename: str
    language: str
    content: str
    lines_of_code: int
    analysis: str
}

node CodebaseProject {
    name: str
    description: str
    root_path: str
    file_count: int
    total_loc: int
    languages: List[str]
    created_at: datetime
}

node Session {
    history: List[str]
    created_at: datetime
    project_id: str
}

node Memory {
    sessions: List[Session]
    global_state: dict
}
```

### Edge Types

```
Memory ──[contains]──> Session
Project ──[contains]──> CodeFile
CodeFile ──[imports]──> CodeFile
CodeFile ──[references]──> CodeFile
Session ──[analyzes]──> Project
```

## Walker Functions

### `codebase_genius` - Main Orchestrator

```jac
walker codebase_genius {
    action: str  # "analyze", "review", "document", "chat"
    message: str
    project_path: str
    files_data: List[dict]
    
    Workflow:
    1. Initialize memory and session
    2. Parse action type
    3. Route to appropriate agent
    4. Manage state and history
    5. Return results
}
```

### `analyze_files` - Code Analysis

```jac
walker analyze_files {
    file_nodes: List[str]
    
    Workflow:
    1. Get file references
    2. Spawn CodeAnalyzer agent
    3. Analyze each file
    4. Aggregate results
    5. Store in graph
}
```

### `generate_documentation` - Doc Generation

```jac
walker generate_documentation {
    project_id: str
    
    Workflow:
    1. Load project and files
    2. Spawn DocumentationGenerator
    3. Generate multi-format docs
    4. Store documentation
    5. Return output
}
```

### `review_code` - Code Review

```jac
walker review_code {
    project_id: str
    
    Workflow:
    1. Load project files
    2. Spawn CodeReviewer agent
    3. Review each file
    4. Aggregate findings
    5. Return report
}
```

## Frontend Architecture

### Streamlit Component Structure

```
app.py
├── Page Config & Styling
├── Constants & API Endpoints
├── Session State Management
├── Navigation Tabs
│   ├── Repository Upload
│   │   ├── Local/Git Upload
│   │   ├── Project Metadata
│   │   └── Preview
│   ├── Code Analysis
│   │   ├── Agent Triggers
│   │   └── Results Display
│   ├── Documentation Generation
│   │   ├── Doc Type Selection
│   │   ├── Customization
│   │   └── Preview/Export
│   ├── Code Review
│   │   ├── Review Types
│   │   └── Findings Display
│   └── Chat Interface
│       ├── Chat History
│       └── Message Input
└── Footer & Navigation
```

### State Management

```python
st.session_state {
    session_id: str              # Current session
    current_project: str         # Active project
    analysis_results: dict       # Analysis data
    documentation: str           # Generated docs
    code_review: dict           # Review findings
    chat_history: List[dict]    # Chat messages
}
```

## Backend Deployment Architecture

### JAC Server Setup

```
┌──────────────────────────────┐
│   JAC Server (Port 8000)      │
├──────────────────────────────┤
│                              │
│  ├─ HTTP API Listener        │
│  ├─ Walker Executor          │
│  ├─ Graph Database (Jarcdb)  │
│  ├─ byLLM Integration        │
│  └─ Session Manager          │
│                              │
└──────────────────────────────┘
```

### LLM Integration

```
┌──────────────────────────────┐
│   byLLM Framework            │
├──────────────────────────────┤
│                              │
│  ┌────────────────────────┐  │
│  │  Model Management      │  │
│  │  - Model Selection     │  │
│  │  - API Key Handling    │  │
│  │  - Token Management    │  │
│  └────────────────────────┘  │
│                              │
│  ┌────────────────────────┐  │
│  │  Tool Binding          │  │
│  │  - Function Wrapping   │  │
│  │  - Context Management  │  │
│  │  - Result Parsing      │  │
│  └────────────────────────┘  │
│                              │
│  ┌────────────────────────┐  │
│  │  Reasoning Methods     │  │
│  │  - ReAct Pattern       │  │
│  │  - Semantic Routing    │  │
│  │  - Response Generation │  │
│  └────────────────────────┘  │
│                              │
└──────────────────────────────┘
```

## Data Flow Diagrams

### Complete Analysis Pipeline

```
┌─────────────────┐
│ User Upload     │
│ Repository      │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│ File Loading & Parsing          │
│ - Read files                    │
│ - Detect language              │
│ - Calculate metrics             │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Code Analysis Phase             │
│ [CodeAnalyzer Agent]            │
│ - Structure analysis            │
│ - Function extraction           │
│ - Complexity measurement        │
│ - Dependency mapping            │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Parallel Processing             │
├─────────────┬───────────────────┤
│ Review Phase│ Doc Generation    │
│ [Reviewer]  │ [Doc Generator]   │
└─────────────┴────────┬──────────┘
                       │
                       v
┌─────────────────────────────────┐
│ Knowledge Base Update           │
│ - Store analysis results        │
│ - Link dependencies            │
│ - Create indexes               │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│ Export & Present Results        │
│ - Generate exports             │
│ - Display in UI                │
│ - Enable queries               │
└─────────────────────────────────┘
```

### Chat Query Flow

```
┌──────────────────┐
│ User Query       │
│ (Chat Input)     │
└────────┬─────────┘
         │
         v
┌──────────────────────────────┐
│ Context Retrieval            │
│ - Session history            │
│ - Project metadata           │
│ - Previous analyses          │
└────────┬─────────────────────┘
         │
         v
┌──────────────────────────────┐
│ Route to Appropriate Agent   │
│ - Analyzer?                  │
│ - Reviewer?                  │
│ - Doc Gen?                   │
│ - General Chat?              │
└────────┬─────────────────────┘
         │
         v
┌──────────────────────────────┐
│ Agent Processing             │
│ - Reason about query         │
│ - Execute tools              │
│ - Format response            │
└────────┬─────────────────────┘
         │
         v
┌──────────────────────────────┐
│ Update Session History       │
│ - Store Q&A pair            │
│ - Update context            │
└────────┬─────────────────────┘
         │
         v
┌──────────────────────────────┐
│ Return Response to User      │
│ - Display in chat            │
│ - Update UI                  │
└──────────────────────────────┘
```

## Security Architecture

### API Security

```
┌─────────────────────────────────┐
│  HTTP Request                   │
├─────────────────────────────────┤
│  - Headers validation           │
│  - Content-type check           │
│  - Size limits                  │
│  - Rate limiting                │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│  Input Sanitization             │
├─────────────────────────────────┤
│  - Code injection checks        │
│  - Path traversal prevention    │
│  - File type validation         │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│  Processing                     │
│  - Isolated execution           │
│  - Resource limits              │
│  - Timeout handling             │
└────────┬────────────────────────┘
         │
         v
┌─────────────────────────────────┐
│  Output Encoding                │
│  - Proper escaping              │
│  - Format validation            │
│  - Size control                 │
└─────────────────────────────────┘
```

## Performance Optimization

### Caching Strategy

```
┌──────────────────────────┐
│  Cache Layers            │
├──────────────────────────┤
│                          │
│  L1: LLM Response Cache  │
│      - TTL: 1 hour       │
│      - Key: prompt hash  │
│                          │
│  L2: Analysis Cache      │
│      - TTL: 24 hours     │
│      - Key: file hash    │
│                          │
│  L3: Graph Cache         │
│      - TTL: persistent   │
│      - Key: project id   │
│                          │
└──────────────────────────┘
```

### Async Processing

```
┌─────────────────────────────┐
│ Blocking Operations         │
├─────────────────────────────┤
│  - File I/O                 │
│  - LLM API calls            │
│  - Graph DB queries         │
└────────┬────────────────────┘
         │
         v
┌─────────────────────────────┐
│ Async Task Queue            │
├─────────────────────────────┤
│  - Task scheduling          │
│  - Worker pool              │
│  - Progress tracking        │
│  - Error handling           │
└─────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling

```
                ┌──────────────┐
                │ Load Balancer│
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        v              v              v
    ┌────────┐  ┌────────┐  ┌────────┐
    │ JAC    │  │ JAC    │  │ JAC    │
    │Server1 │  │Server2 │  │Server3 │
    └────┬───┘  └────┬───┘  └────┬───┘
         │           │           │
         └───────────┼───────────┘
                     │
                     v
            ┌─────────────────┐
            │ Shared Graph DB │
            │ (Jarcdb)        │
            └─────────────────┘
```

## Monitoring & Observability

### Metrics Collection

```
┌────────────────────────────┐
│ Metrics Collected          │
├────────────────────────────┤
│                            │
│  - Request latency         │
│  - LLM API usage           │
│  - Cache hit rates         │
│  - Error rates             │
│  - File processing time    │
│  - Analysis quality        │
│                            │
└────────────────────────────┘
```

---

**Document Version:** 1.0  
**Last Updated:** November 2025
