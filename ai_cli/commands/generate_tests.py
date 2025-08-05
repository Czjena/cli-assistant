import os

import typer

from ai_cli.utils.ai_client import ask_llm

def generate_tests(file_path: str, with_context: bool = True, output_dir: str = "tests"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File {file_path} not found.")
        return

    include_context = typer.confirm("Do you want to include context(it includes whole project)",default =True)

    context = ""
    if include_context:
        # Znajdź główny folder projektu
        project_root = os.path.abspath(os.path.join(file_path, "..", ".."))

        # Dodaj wszystkie inne pliki .py jako kontekst
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if
                       d not in {'.venv', 'venv', '__pycache__', '.git', 'node_modules', 'dist', 'build'}]
        for root, _, files in os.walk(project_root):
            for name in files:
                full_path = os.path.join(root, name)
                if name.endswith(".py") and full_path != os.path.abspath(file_path):
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            relative = os.path.relpath(full_path, project_root)
                            context += f"\n\n# File: {relative}\n" + f.read()
                    except Exception as e:
                        print(f"⚠️ Skipping {name}: {e}")

    prompt = (
        "Here is the full codebase context (read-only):\n"
        "Do NOT write tests for the context files."
        "Do NOT write tests for the context files.\n"
        f"{context}\n\n"
        "Now, write ONLY simple pytest unit tests for the following target file. "
        "Do NOT write tests for the context files. "
        "Do NOT include explanations or comments. Focus on basic correctness:\n\n"
        f"{code}"
    )
    if with_context and context:
        prompt += f"# CONTEXT:\n{context}\n\n"

    prompt += f"# TARGET FILE:\n{code}"

    tests = ask_llm(prompt)

    # Zapisz do folderu 'tests'
    tests_dir = output_dir
    os.makedirs(tests_dir, exist_ok=True)

    test_file_name = f"test_{os.path.basename(file_path)}"
    test_file_path = os.path.join(tests_dir, test_file_name)

    try:
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(tests)
        print(f"✅ Tests saved to {test_file_path}")
    except Exception as e:
        print(f"❌ Error saving generated tests: {e}")
