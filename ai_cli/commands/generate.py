import os
import typer
from ai_cli.utils.ai_client import ask_llm
from ai_cli.utils.language_utils import detect_language

def generate(
    file: str = typer.Argument(..., help="File name to save the generated code"),
    prompt: str = typer.Argument(..., help="Description of the code to generate"),
    languages: str = typer.Option(None, help="Comma-separated list of languages to include in context, e.g. 'python,javascript'"),
    extra_context: str = None
):
    full_prompt = prompt
    if extra_context:
        full_prompt += "\n\n### Additional context:\n" + extra_context


    print(f"Prompt wysłany do AI:\n{full_prompt}")
    """
    Generate a code file based on the provided prompt, optionally sending the project context.
    """

    include_context = typer.confirm("📦 Do you want to include the project context?", default=True)

    allowed_langs = None
    if languages:
        allowed_langs = set(lang.strip().lower() for lang in languages.split(","))

    context = ""
    if include_context:
        project_root = os.getcwd()
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in {'.venv', 'venv', '__pycache__', '.git', 'node_modules', 'dist', 'build'}]
            for filename in files:
                full_path = os.path.join(root, filename)
                file_language = detect_language(full_path)
                if allowed_langs is None or (file_language and file_language.lower() in allowed_langs):
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            relative_path = os.path.relpath(full_path, project_root)
                            context += f"\n\n# File: {relative_path}\n"
                            context += f.read()
                    except Exception as e:
                        print(f"⚠️ Could not read {filename}: {e}")

    full_prompt = (
        "You are a senior developer assistant.\n"
        + (f"Here is the full project context (read-only):\n{context}\n\n" if context else "")
        + "Generate only the code requested, without any comments, explanations, or extra text.\n"
        + f"{prompt}"
    )

    code = ask_llm(full_prompt)

    with open(file, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Code saved to {file}")
