import os
import typer
from ai_cli.utils.ai_client import ask_llm

def analyze():
    """
    Analyze the current project and give suggestions as a senior developer.
    """
    confirm = typer.confirm("Do you want to analyze the entire project?")
    if not confirm:
        raise typer.Abort()

    project_root = os.getcwd()

    context = ""
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if
                   d not in {'.venv', 'venv', '__pycache__', '.git', 'node_modules', 'dist', 'build'}]
        for filename in files:
            if filename.endswith(".py"):
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        relative_path = os.path.relpath(full_path, project_root)
                        context += f"\n\n# File: {relative_path}\n"
                        context += f.read()
                except Exception as e:
                    print(f"⚠️ Could not read {filename}: {e}")

    prompt = (
        "You are a senior software engineer.\n"
        "The user is asking for a code review of the following project.\n"
        "Go through the project and give suggestions about code quality, structure, naming, potential issues,\n"
        "bugs, security problems, or opportunities to refactor.\n"
        "Focus on high-level insights and don’t rewrite the code.\n\n"
        f"{context}"
    )

    response = ask_llm(prompt)

    print("\nAI Feedback:\n")
    print(response)
