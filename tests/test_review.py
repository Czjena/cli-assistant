from unittest.mock import patch
from ai_cli.commands.review import review

def test_review_successful(tmp_path, capsys):
    # Przygotowanie pliku testowego
    code = "def add(a, b):\n    return a + b"
    file_path = tmp_path / "sample.py"
    file_path.write_text(code)

    mock_response = "Looks good, but consider adding type hints."

    with patch("ai_cli.commands.review.ask_llm", return_value=mock_response) as mock_llm:
        review(str(file_path))

    # Przechwycenie stdout
    captured = capsys.readouterr()
    assert "🔍 Running code review..." in captured.out
    assert "📝 Code review result:" in captured.out
    assert mock_response in captured.out

    # Sprawdzenie czy LLM dostał odpowiedni prompt
    called_prompt = mock_llm.call_args[0][0]
    assert "expert software developer" in called_prompt
    assert code in called_prompt

def test_review_file_not_found(capsys):
    review("non_existent_file.py")
    captured = capsys.readouterr()
    assert "❌ File 'non_existent_file.py' not found." in captured.out