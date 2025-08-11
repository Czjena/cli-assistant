import os
import tempfile
import pytest
from ai_cli.commands.context_adder import ContextAdder

def test_add_context(tmp_path):
    # Przygotuj pliki w tymczasowym katalogu
    main_file = tmp_path / "main.py"
    related_file1 = tmp_path / "helper.py"
    related_file2 = tmp_path / "utils.py"

    main_file.write_text("print('Main file')", encoding="utf-8")
    related_file1.write_text("def helper(): pass", encoding="utf-8")
    related_file2.write_text("def util(): pass", encoding="utf-8")

    ca = ContextAdder(base_path=str(tmp_path))

    prompt = "Initial prompt"
    result = ca.add_context(str(main_file), prompt)

    # Sprawdź, że prompt zawiera oryginalny tekst
    assert "Initial prompt" in result
    # Sprawdź, że dodany jest tekst z plików powiązanych
    assert "def helper(): pass" in result
    assert "def util(): pass" in result
    # Nie powinno być zawartości main.py dodanej drugi raz
    assert "print('Main file')" not in result  # bo main_file to punkt odniesienia, nie powinien być dodany

