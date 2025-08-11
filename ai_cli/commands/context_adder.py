import os

class ContextAdder:
    def __init__(self, base_path):
        self.base_path = base_path

    def _load_related_files(self, main_file):
        folder = os.path.dirname(main_file)
        related_files = []
        for fname in os.listdir(folder):
            if fname.endswith('.py') and fname != os.path.basename(main_file):
                path = os.path.join(folder, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    related_files.append(f.read())
        return related_files

    def add_context(self, main_file: str, original_prompt: str) -> str:
        related_contents = self._load_related_files(main_file)
        context_text = "\n\n### Related files:\n" + "\n\n---\n\n".join(related_contents)
        full_prompt = original_prompt + context_text
        return full_prompt