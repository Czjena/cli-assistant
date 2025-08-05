import os
from unittest.mock import patch
from ai_cli.commands.generate import generate

def test_generate_creates_file_with_mocked_llm(tmp_path):
    output_path = tmp_path / "generated_code.py"
    prompt = "def add(a, b): return a + b"

    mock_generated_code = """
def add(a, b):
    return a + b
"""

    # Podmieniamy funkcję LLM na zwracającą mockowany kod
    with patch("ai_cli.commands.generate.ask_llm", return_value=mock_generated_code):
        generate(file=str(output_path), prompt=prompt, languages="python")

    assert output_path.exists(), "Plik z wygenerowanym kodem nie powstał."
    content = output_path.read_text(encoding="utf-8")
    assert len(content) > 0, "Wygenerowany plik jest pusty."
    assert "def add" in content
    assert "return a + b" in content
