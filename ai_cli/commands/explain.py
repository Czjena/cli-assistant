from ai_cli.utils.ai_client import ask_llm


def explain(file: str):
    """Explains what code does in file"""
    try:
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ Plik {file} nie istnieje.")
        return

    prompt = (
        "Explain this code like for a junior dev.\n\n"
        f"{code}"
    )

    explanation = ask_llm(prompt)
    print("\n🧠 Wyjaśnienie kodu:\n")
    print(explanation)
