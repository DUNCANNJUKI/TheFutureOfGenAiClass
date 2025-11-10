import from byllm.llm { Model }
import from dotenv { load_dotenv }
import os;

include utils;

# Global LLM Model
glob llm = Model(model_name="gpt-4o", verbose=False);

# ============================================================================
# DATA MODELS
# ============================================================================

node CodeFile {
    has filepath: str = "";
    has filename: str = "";
    has language: str = "";
    has content: str = "";
    has lines_of_code: int = 0;
    has analysis: str = "";
}

node CodebaseProject {
    has name: str = "";
    has description: str = "";
    has root_path: str = "";
    has file_count: int = 0;
    has total_loc: int = 0;
    has languages: list = [];
    has created_at: str = get_current_datetime();
}

node Session {
    has history: list = [];
    has created_at: str = get_current_datetime();
    has project_id: str = "";
    
    def add_history(entry: str) {
        self.history = self.history + [entry];
    }
    
    def get_history -> str {
        return "\n".join(self.history[-15:]);
    }
}

# ============================================================================
# AGENT: CODE ANALYZER
# ============================================================================

node CodeAnalyzer {
    def analyze_code_structure(code: str, language: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def identify_functions(code: str, language: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def analyze_complexity(code: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def extract_imports(code: str, language: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    can execute with analyzer entry {
        session = visitor.session;
        code_file = visitor.code_file;
        
        # Analyze the code
        structure = self.analyze_code_structure(code_file.content, code_file.language);
        functions = self.identify_functions(code_file.content, code_file.language);
        complexity = self.analyze_complexity(code_file.content);
        imports = self.extract_imports(code_file.content, code_file.language);
        
        analysis_result = "## Code Analysis: " + code_file.filename + "\n\n### Structure\n" + structure + "\n\n### Functions and Classes\n" + functions + "\n\n### Complexity Assessment\n" + complexity + "\n\n### Dependencies\n" + imports;
        
        code_file.analysis = analysis_result;
        session.add_history("Analyzed: " + code_file.filename);
        
        report {
            "status": "success",
            "file": code_file.filename,
            "analysis": analysis_result
        };
    }
}

sem CodeAnalyzer.analyze_code_structure = """
Analyze the code structure and provide:
1. High-level overview of what the code does
2. Main classes, modules, or functions
3. Architecture patterns used
Keep response concise but informative.
""";

sem CodeAnalyzer.identify_functions = """
Extract and summarize:
1. Function/method names and their purpose
2. Parameters and return types (infer from code)
3. Key public APIs
Format as a structured list.
""";

sem CodeAnalyzer.analyze_complexity = """
Evaluate:
1. Code complexity level (simple/moderate/complex)
2. Cyclomatic complexity indicators
3. Any potential maintainability issues
Provide brief assessment.
""";

sem CodeAnalyzer.extract_imports = """
List:
1. External dependencies/imports
2. Internal module references
3. Potential framework/library usage
Format as a dependency list.
""";

# ============================================================================
# AGENT: DOCUMENTATION GENERATOR
# ============================================================================

node DocumentationGenerator {
    def generate_function_docs(analysis: str, filename: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def generate_usage_examples(code: str, language: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def generate_architecture_overview(analyses: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def format_readme(project_name: str, overview: str, structure: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    can execute with doc_gen entry {
        session = visitor.session;
        analyses = visitor.analyses;
        project = visitor.project;
        
        # Generate function documentation
        functions_doc = self.generate_function_docs(
            "\n".join([a.analysis for a in analyses]), 
            project.name
        );
        
        # Generate usage examples
        examples = self.generate_usage_examples(
            "\n".join([a.content for a in analyses[:3]]), 
            analyses[0].language if analyses else "Unknown"
        );
        
        # Generate architecture overview
        arch_overview = self.generate_architecture_overview(
            "\n".join([a.analysis for a in analyses])
        );
        
        # Generate comprehensive README
        readme = self.format_readme(
            project.name,
            arch_overview,
            functions_doc
        );
        
        session.add_history("Generated documentation for project");
        
        report {
            "status": "success",
            "readme": readme,
            "functions_doc": functions_doc,
            "examples": examples,
            "architecture": arch_overview
        };
    }
}

sem DocumentationGenerator.generate_function_docs = """
Create comprehensive function/method documentation including:
1. Function signatures and purposes
2. Parameter descriptions
3. Return value descriptions
4. Common use cases
Use clear, professional language suitable for developer documentation.
""";

sem DocumentationGenerator.generate_usage_examples = """
Generate practical code examples showing:
1. Basic usage of main components
2. Common workflows
3. Best practices
4. Error handling patterns
Keep examples concise but illustrative.
""";

sem DocumentationGenerator.generate_architecture_overview = """
Create high-level architecture documentation describing:
1. System design and components
2. Data flow
3. Key architectural patterns
4. Dependencies between modules
Use diagrams or ASCII art if helpful.
""";

sem DocumentationGenerator.format_readme = """
Generate a professional README.md with:
1. Project description
2. Features and capabilities
3. Installation instructions
4. Quick start guide
5. Architecture overview
6. Contributing guidelines
Follow markdown best practices.
""";

# ============================================================================
# AGENT: CODE REVIEWER
# ============================================================================

node CodeReviewer {
    def identify_issues(code: str, language: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def suggest_improvements(analysis: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    def check_best_practices(code: str, language: str) -> str by llm(
        method="ReAct",
        tools=([])
    );
    
    can execute with reviewer entry {
        session = visitor.session;
        code_file = visitor.code_file;
        
        # Identify issues
        issues = self.identify_issues(code_file.content, code_file.language);
        
        # Suggest improvements
        improvements = self.suggest_improvements(code_file.analysis);
        
        # Check best practices
        practices = self.check_best_practices(code_file.content, code_file.language);
        
        review_result = "## Code Review: " + code_file.filename + "\n\n### Issues Found\n" + issues + "\n\n### Improvement Suggestions\n" + improvements + "\n\n### Best Practices Check\n" + practices;
        
        session.add_history("Reviewed: " + code_file.filename);
        
        report {
            "status": "success",
            "file": code_file.filename,
            "review": review_result
        };
    }
}

sem CodeReviewer.identify_issues = """
Identify and categorize:
1. Potential bugs or errors
2. Security concerns
3. Performance issues
4. Code smells
Provide severity levels and explanations.
""";

sem CodeReviewer.suggest_improvements = """
Suggest enhancements for:
1. Code readability
2. Maintainability
3. Performance optimization
4. Refactoring opportunities
Be constructive and specific.
""";

sem CodeReviewer.check_best_practices = """
Evaluate adherence to:
1. Language-specific conventions
2. Design patterns
3. Error handling practices
4. Documentation standards
Provide actionable feedback.
""";

# ============================================================================
# ROUTING AND ORCHESTRATION
# ============================================================================

enum AgentType {
    ANALYZER = "CodeAnalyzer",
    DOC_GENERATOR = "DocumentationGenerator",
    REVIEWER = "CodeReviewer",
    GENERAL = "GeneralChat"
}

node GeneralChat {
    def chat(message: str, history: str) -> str by llm();
    
    can execute with general_chat entry {
        session = visitor.session;
        response = self.chat(visitor.message, session.get_history());
        session.add_history(f"user: {visitor.message}\nai: {response}");
        
        report {
            "session_id": jid(visitor.session),
            "created_at": visitor.session.created_at,
            "response": response
        };
    }
}

# ============================================================================
# MAIN ORCHESTRATION WALKER
# ============================================================================

walker codebase_genius {
    has action: str = "";
    has message: str = "";
    has project_path: str = "";
    has files_data: list = [];
    
    obj __specs__ {
        static has auth: bool = False;
    }
    
    def determine_agent_action(message: str, history: str) -> AgentType by llm();
    
    can execute with `root entry {
        # Create or get memory node
        memory_list = [root --> (`?Memory)];
        if not memory_list {
            memory_list = root ++> Memory();
        }
        memory = memory_list[0];
        
        # Create session
        session_list = memory ++> Session();
        session = session_list[0];
        
        # Process based on action
        if self.action == "analyze" {
            # Create project node
            project = root ++> CodebaseProject(
                name=self.message,
                root_path=self.project_path
            );
            
            # Analyze files
            for file_data in self.files_data {
                code_file = CodeFile(
                    filepath=file_data["path"],
                    filename=file_data["name"],
                    language=get_language_from_extension(file_data["ext"]),
                    content=truncate_content(file_data["content"]),
                    lines_of_code=file_data.get("loc", 0)
                );
                project ++> code_file;
            }
            
            session.project_id = jid(project);
            session.add_history(f"Started analyzing project: {self.message}");
            
            report {
                "status": "project_created",
                "project_id": jid(project),
                "session_id": jid(session),
                "files_loaded": len(self.files_data)
            };
        } else {
            # Handle chat/queries
            session.add_history(f"user: {self.message}");
            report {
                "status": "message_received",
                "session_id": jid(session)
            };
        }
    }
}

node Memory {}

walker analyze_files {
    has file_nodes: list = [];
    
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can analyze_files with `root entry {
        # Get all CodeFile nodes and analyze them
        all_files = [root --> (`?CodeFile)];
        
        for code_file in all_files {
            analyzer = CodeAnalyzer();
            visit analyzer;
        }
        
        report {
            "status": "analysis_complete",
            "files_analyzed": len(all_files)
        };
    }
}

walker generate_documentation {
    has project_id: str = "";
    
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can generate_documentation with `root entry {
        # Get project and files
        project = &(self.project_id);
        analyses = [project --> (`?CodeFile)];
        
        if not analyses {
            report {
                "status": "error",
                "message": "No files found for project"
            };
            disengage;
        }
        
        # Generate comprehensive documentation
        doc_gen = DocumentationGenerator();
        visit doc_gen;
        
        report {
            "status": "documentation_generated"
        };
    }
}

walker review_code {
    has project_id: str = "";
    
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can review_code with `root entry {
        project = &(self.project_id);
        files = [project --> (`?CodeFile)];
        
        reviews = [];
        for code_file in files {
            reviewer = CodeReviewer();
            visit reviewer;
            reviews = reviews + [code_file.analysis];
        }
        
        report {
            "status": "review_complete",
            "files_reviewed": len(files),
            "reviews": reviews
        };
    }
}

walker get_sessions {
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can get_sessions with `root entry {
        memory_list = [here --> (`?Memory)];
        if not memory_list {
            report "No sessions found.";
            disengage;
        }
        
        memory = memory_list[0];
        session_list = [memory --> (`?Session)];
        report [{
            "id": jid(session),
            "created_at": session.created_at,
            "project_id": session.project_id
        } for session in session_list];
    }
}

walker get_projects {
    obj __specs__ {
        static has auth: bool = False;
    }
    
    can get_projects with `root entry {
        projects = [root --> (`?CodebaseProject)];
        report [{
            "id": jid(p),
            "name": p.name,
            "created_at": p.created_at,
            "file_count": p.file_count,
            "languages": p.languages
        } for p in projects];
    }
}

# Initialize environment
with entry {
    load_dotenv();
}
