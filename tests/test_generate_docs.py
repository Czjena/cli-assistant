import os
from unittest.mock import patch
from ai_cli.commands.generate_docs import generate_docs

@patch("ai_cli.commands.generate_docs.ask_llm")
def test_generate_docs_single_file(mock_llm, tmp_path, capsys):
    # Przygotuj plik .py
    code = 'def add(a, b):\n    return a + b\n'
    file_path = tmp_path / "sample.py"
    file_path.write_text(code, encoding="utf-8")

    mock_doc = """
# add function
Adds two numbers together.
"""
    mock_llm.return_value = mock_doc

    generate_docs(str(file_path))

    # Sprawdź, czy wywołano ask_llm i czy prompt zawiera kod
    called_prompt = mock_llm.call_args[0][0]
    assert "def add(a, b):" in called_prompt

    # Sprawdź, czy plik dokumentacji powstał i zawiera wygenerowany tekst
    doc_file = os.path.abspath("GENERATED_DOCUMENTATION.md")
    assert os.path.exists(doc_file)
    content = open(doc_file, "r", encoding="utf-8").read()
    assert "Adds two numbers together." in content

    # Sprawdź komunikat na stdout
    captured = capsys.readouterr()
    assert "📘 Documentation saved to GENERATED_DOCUMENTATION.md" in captured.out

    # Sprzątanie
    os.remove(doc_file)
