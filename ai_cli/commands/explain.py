from typing import Optional
from ai_cli.utils.ai_client import ask_llm


def explain(file: str) -> Optional[None]:
    """
    Reads source code from the given file path and generates an explanation of the code using a local AI model.

    Parameters:
        file (str): Path to the source code file to explain.

    Returns:
        None: Prints the explanation to the console.
              Returns None explicitly if the file is not found.

    Behavior:
        - Reads the entire content of the specified file.
        - If the file does not exist, prints an error message and returns None.
        - Constructs a prompt asking the AI to explain the code like for a junior developer.
        - Sends the prompt to the local AI client (ask_llm).
        - Prints the explanation received from the AI.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File {file} does not exist.")
        return None

    prompt = (
        "Explain this code like for a junior developer.\n\n"
        f"{code}"
    )

    explanation = ask_llm(prompt)
    print("\n🧠 Code explanation:\n")
    print(explanation)
