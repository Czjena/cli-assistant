import typer
from ai_cli.utils.ai_client import ask_llm

def generate(
    file: str = typer.Argument(..., help="File name to save the generated code"),
    prompt: str = typer.Argument(..., help="Description of the code to generate")
):
    """
    Generate a code file based on the provided prompt.

    Args:
        file: The target filename to save the generated code.
        prompt: The prompt describing what code should be generated.
    """
    code = ask_llm(prompt)
    with open(file, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Code saved to {file}")