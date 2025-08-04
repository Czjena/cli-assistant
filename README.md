# AI CLI Assistant

## Overview

AI CLI Assistant is a command-line tool that connects locally to LM Studio (a local large language model) to execute various AI-powered commands.

It allows you to generate code, explain existing code, perform code reviews, and more — all from your terminal.

## Features

- Generate code based on text prompts and save it to a file
- Explain code from a given file with step-by-step clarifications
- Review code for bugs, smells, and suggestions
- Interactive mode with a user-friendly menu to select commands

## Requirements

- Python 3.8+
- LM Studio running locally on http://localhost:1234
- Python packages listed in requirements.txt

## Installation

```
git clone https://github.com/Czjena/ai-cli-assistant.git
cd ai-cli-assistant
```

Create and activate a virtual environment:

**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Make sure LM Studio is running on port 1234.

## Usage

Generate code from prompt and save to file:
```
python cli.py generate hello.py "Write a Python function that prints 'Hello, World!'"
```

Explain code from a file:
```
python cli.py explain hello.py
```

Review code from a file:
```
python cli.py review hello.py
```

Use interactive mode:
```
python cli.py interactive
```

## Notes

- The CLI communicates with LM Studio via its REST API:  
  http://localhost:1234/v1/chat/completions
- Ensure LM Studio is running and a model is loaded before starting the CLI.
- AI responses and output depend on the capabilities of the model loaded in LM Studio.

## License

MIT License — feel free to use and modify.
