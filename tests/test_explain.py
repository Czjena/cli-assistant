import os
import tempfile
from unittest.mock import patch
from ai_cli.commands.explain import explain


@patch("ai_cli.commands.explain.ask_llm")
def test_explain_reads_file_and_calls_ai(mock_ask_llm):
    # Przygotuj tymczasowy plik z kodem
    code = "def add(a, b): return a + b"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".py") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    # Mock odpowiedzi AI
    mock_ask_llm.return_value = "This function adds two numbers."

    # Wywołanie funkcji
    explain(temp_file_path)

    # Sprawdzenie, czy ask_llm został wywołany z odpowiednim promptem
    mock_ask_llm.assert_called_once()
    prompt = mock_ask_llm.call_args[0][0]
    assert "Explain this code like for a junior developer" in prompt
    assert "def add(a, b)" in prompt

    # Posprzątaj plik
    os.remove(temp_file_path)


@patch("ai_cli.commands.explain.ask_llm")
def test_explain_handles_missing_file(mock_ask_llm):
    # Plik nie istnieje
    non_existent_file = "some/fake/path.py"

    result = explain(non_existent_file)

    # Nie powinno wywołać ask_llm
    mock_ask_llm.assert_not_called()

    # Powinno zwrócić None
    assert result is None
