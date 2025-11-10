import from datetime { datetime }
import os;

def get_current_datetime() -> str {
    return str(datetime.now());
}

def get_file_extension(filepath: str) -> str {
    return filepath.split('.')[-1] if '.' in filepath else "";
}

def get_language_from_extension(ext: str) -> str {
    ext_map = {
        "py": "Python",
        "js": "JavaScript",
        "ts": "TypeScript",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "go": "Go",
        "rs": "Rust",
        "rb": "Ruby",
        "php": "PHP",
        "cs": "C#",
        "swift": "Swift",
        "kt": "Kotlin",
        "sql": "SQL",
        "jac": "Jac",
        "md": "Markdown"
    };
    return ext_map.get(ext.lower(), "Unknown");
}

def truncate_content(content: str, max_chars: int = 5000) -> str {
    if len(content) > max_chars {
        return content[:max_chars] + f"\n...[Content truncated - {len(content) - max_chars} characters omitted]";
    }
    return content;
}

def sanitize_filename(filename: str) -> str {
    invalid_chars = ['<', '>', ':', '"', '/', '\\\\', '|', '?', '*'];
    sanitized = filename;
    for char in invalid_chars {
        sanitized = sanitized.replace(char, '_');
    }
    return sanitized;
}
