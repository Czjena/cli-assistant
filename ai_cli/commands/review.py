from ai_cli.utils.ai_client import ask_llm
import typer


def review(file: str = typer.Argument(..., help="Path to the code file to review")):
    """
    Perform code review on the given file using AI.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File '{file}' not found.")
        return

    prompt = (
        "You are an expert software developer.\n"
        "Perform a thorough code review of the following Python code.\n"
        "Point out bugs, code smells, and suggest improvements.\n\n"
        f"{code}"
    )

    print("🔍 Running code review...\n")
    review_result = ask_llm(prompt)
    print("\n📝 Code review result:\n")
    print(review_result)
