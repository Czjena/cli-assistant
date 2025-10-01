from typing import Optional
from ai_cli.utils.ai_client import ask_llm


def explain(file: str, extra_context: Optional[str] = None) -> Optional[None]:
    """
    Reads source code from the given file path and generates an explanation of the code using a local AI model.

    Parameters:
        file (str): Path to the source code file to explain.
        extra_context (Optional[str]): Additional context to include in the prompt.

    Returns:
        None: Prints the explanation to the console.
              Returns None explicitly if the file is not found.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f" File {file} does not exist.")
        return None

    prompt = (
        "Explain this code like for a junior developer.\n\n"
        f"{code}"
    )

    if extra_context:
        prompt += "\n\n### Additional context:\n" + extra_context

    explanation = ask_llm(prompt)
    print("\n Code explanation:\n")
    print(explanation)
