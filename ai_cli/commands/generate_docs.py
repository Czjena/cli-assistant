import os
import typer
from ai_cli.utils.ai_client import ask_llm

def generate_docs(
    path: str = typer.Argument(..., help="Path to file or folder to generate documentation for")
):
    """
    Generate documentation for the given code file or directory.
    """

    if os.path.isdir(path):
        code = ""
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in {'.venv', 'venv', '__pycache__', '.git'}]
            for filename in files:
                if filename.endswith(".py"):
                    full_path = os.path.join(root, filename)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            relative_path = os.path.relpath(full_path, path)
                            code += f"\n\n# File: {relative_path}\n"
                            code += f.read()
                    except Exception as e:
                        print(f"⚠️ Could not read {filename}: {e}")
    else:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

    prompt = (
        "You are an experienced software documenter.\n"
        "Generate documentation for the following Python code. "
        "Prefer docstrings and clear formatting. Do not change the logic of the code.\n\n"
        f"{code}"
    )

    documentation = ask_llm(prompt)

    doc_path = "GENERATED_DOCUMENTATION.md"
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(documentation)

    print(f"📘 Documentation saved to {doc_path}")
