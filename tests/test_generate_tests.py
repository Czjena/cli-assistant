import time
from unittest.mock import patch
from ai_cli.commands.generate_tests import generate_tests

def test_generate_tests_with_mocked_llm(tmp_path):
    code_sample = "def multiply(a, b):\n    return a * b"
    input_file = tmp_path / "sample.py"
    input_file.write_text(code_sample)

    mock_generated_tests = """
    import pytest

    def test_multiply_positive_numbers():
        assert multiply(2, 3) == 6

    def test_multiply_zero():
        assert multiply(0, 5) == 0
    """

    with patch("ai_cli.commands.generate_tests.generate_tests", return_value=mock_generated_tests):
        generate_tests(str(input_file), output_dir=str(tmp_path))

    test_file = tmp_path / "test_sample.py"

    # Czekaj maksymalnie 3 sekundy (powinno być natychmiast)
    timeout = 3
    while not test_file.exists() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    assert test_file.exists(), "Plik testowy nie został wygenerowany."

    content = test_file.read_text()
    assert "def test_multiply" in content
    assert "assert multiply" in content