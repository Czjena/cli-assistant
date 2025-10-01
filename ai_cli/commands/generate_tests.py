import os
import typer

from ai_cli.utils.ai_client import ask_llm
from ai_cli.commands.context_adder import ContextAdder

def generate_tests(
    file_path: str,
    with_context: bool = True,
    output_dir: str = "tests",
    extra_context: str = None
):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f" File {file_path} not found.")
        return

    include_context = typer.confirm(
        "Do you want to include context (it includes whole project)?", default=True
    )

    prompt = "Now, write ONLY simple pytest unit tests for the following target file. " \
             "Do NOT write tests for the context files. " \
             "Do NOT include explanations or comments. Focus on basic correctness:\n\n"

    if with_context and include_context:
        project_root = os.path.abspath(os.path.join(file_path, "..", ".."))
        context_adder = ContextAdder(base_path=project_root)
        prompt = context_adder.add_context(file_path, prompt)

    # Dołóż dodatkowy kontekst, jeśli jest
    if extra_context:
        prompt += f"\n\n# EXTRA CONTEXT:\n{extra_context}\n\n"

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
        print(f" Tests saved to {test_file_path}")
    except Exception as e:
        print(f" Error saving generated tests: {e}")
