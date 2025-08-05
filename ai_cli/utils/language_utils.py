# language_utils.py

def detect_language(file_path):
    extension_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".cs": "csharp",
        ".rb": "ruby",
        ".go": "go",
        ".php": "php",
        ".rs": "rust",
        ".swift": "swift",
        ".kt": "kotlin",
        ".sh": "bash",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".xml": "xml",
        ".sql": "sql"
    }

    for ext, lang in extension_map.items():
        if file_path.endswith(ext):
            return lang
    return "plain_text"
