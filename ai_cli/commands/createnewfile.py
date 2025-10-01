import os

def create_new_file(file_path: str, content: str = ""):
    """
    Creates a new file with the given content.
    If the file already exists, it will be overwritten.

    Args:
        file_path (str): Path to the new file.
        content (str): Content to write into the file. Defaults to empty string.
    """
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:  # tylko jeśli katalog istnieje w ścieżce
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" File created: {file_path}")
    except Exception as e:
        print(f" Error creating file {file_path}: {e}")