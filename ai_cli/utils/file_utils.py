import os

LANGUAGE_EXTENSIONS = {
    "python": [".py"],
    "javascript": [".js", ".jsx"],
    "java": [".java"],
    "typescript": [".ts", ".tsx"],
    # dodaj więcej jeśli chcesz
}

def get_files_by_language(path, language):
    exts = LANGUAGE_EXTENSIONS.get(language.lower(), [])
    collected = []

    for root, _, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                collected.append(os.path.join(root, file))

    return collected
