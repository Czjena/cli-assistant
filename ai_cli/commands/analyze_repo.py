
from ai_cli.utils.ai_client import ask_llm
from ai_cli.utils.language_utils  import detect_language
from ai_cli.utils.file_utils import get_files_by_language
from ai_cli.utils.report_utils import save_report_to_file


def analyze_repo(path: str, output_path: str = None):
    language = detect_language(path)
    print(f"Analiza repozytorium w języku: {language}")

    files = get_files_by_language(path, language)

    if not files:
        print("Nie znaleziono żadnych plików do analizy.")
        return

    report = []

    for file_path in files:
        print(f"Analiza pliku: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            print(f"Błąd przy odczycie {file_path}: {e}")
            continue

        prompt = build_prompt(code, language)
        analysis = ask_llm(prompt)

        report.append({
            "file": file_path,
            "analysis": analysis.strip()
        })

    print("\n===  Raport ===\n")
    for item in report:
        print(f" {item['file']}\n{item['analysis']}\n{'-' * 40}")

    if output_path:
        save_report_to_file(report, output_path)
        print(f"\n Raport zapisany do: {output_path}")


def build_prompt(code, language):
    return f"""
You're an expert in {language}. Here's the code from the repository.
List the quality issues in this file and provide specific refactoring suggestions.
Don't explain the theory – just a list of things to improve with examples.
Code:
{code}
"""
