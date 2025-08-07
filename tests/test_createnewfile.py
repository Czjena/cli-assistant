import os

from ai_cli.commands.createnewfile import create_new_file


def test_create_new_file(tmp_path):
        # Set file_path to be a subdirectory of tmp_path
        file_path = str(tmp_path / "test.txt")
        content = "Hello, World!"
        create_new_file(file_path, content)
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        assert data == content


def test_overwrite_existing_file(tmp_path):
        file_path = str(tmp_path / "overwrite.txt")
        # First create an empty file (or write some initial content)
        with open(file_path, 'w', encoding='utf-8') as f:
            pass
        # Then call the function again to overwrite it
        new_content = "Overwritten!"
        create_new_file(file_path, new_content)
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        assert data == new_content

