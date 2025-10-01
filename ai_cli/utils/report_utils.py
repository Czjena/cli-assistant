import json

def save_report_to_file(report, path):
    if path.endswith(".json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    elif path.endswith(".md") or path.endswith(".txt"):
        with open(path, "w", encoding="utf-8") as f:
            for item in report:
                f.write(f"# {item['file']}\n\n{item['analysis']}\n\n---\n")
    else:
        print("  Nieobsługiwany format raportu. Obsługiwane: .json, .md, .txt")
