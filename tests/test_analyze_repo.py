import os
import tempfile
from unittest.mock import patch
from ai_cli.commands.analyze_repo import analyze_repo

def create_test_file(dir_path, filename, content):
    path = os.path.join(dir_path, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

@patch("ai_cli.commands.analyze_repo.detect_language", return_value="python")
@patch("ai_cli.commands.analyze_repo.ask_llm")
def test_analyze_repo_creates_report(mock_chat, mock_lang):
    mock_chat.return_value = "Mocked analysis: function too long, no docstring."

    with tempfile.TemporaryDirectory() as temp_dir:
        # Tworzymy przykładowy plik Pythona
        code = """
def bad_function(x):
    y = x + 1
    return y
"""
        create_test_file(temp_dir, "example.py", code)

        # Wywołujemy funkcję
        analyze_repo(temp_dir)

        # Sprawdzenie: czy wywołało chat_with_model
        assert mock_chat.called
        call_args = mock_chat.call_args[0][0]  # prompt
        assert "bad_function" in call_args
        assert "python" in call_args
