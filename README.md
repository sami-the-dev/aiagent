# AI Coding Agent & Calculator

## Overview

This project is an AI-powered coding agent and calculator application. It provides:

- An interactive command-line calculator supporting basic arithmetic expressions.
- An agent system for reading, writing, and executing Python files in a secure, sandboxed environment.
- Modular functions for file management and code execution.

## Project Structure

- `main.py`: Entry point for the AI agent. Handles user prompts and interacts with the Gemini API.
- `config.py`: Configuration constants (e.g., file size limits).
- `calculator/`: Contains the calculator app and related files.
  - `main.py`: CLI for the calculator.
  - `pkg/calculator.py`: Implements the calculator logic (supports +, -, \*, /, infix evaluation).
  - `pkg/render.py`: Formats calculator results as JSON.
  - `README.md`, `lorem.txt`, `test_file.txt`, `morelorem.txt`: Documentation and sample files.
  - `tests.py`: Tests for calculator functionality.
- `functions/`: Modular Python functions for agent operations.
  - `function_call_part.py`: Maps function calls to implementations.
  - `get_file_content.py`: Securely reads file contents.
  - `get_files_info.py`: Lists files in a directory.
  - `run_python_file.py`: Executes Python files and returns output.
  - `write_file.py`: Securely writes content to files.

## Usage

### Calculator CLI

Run the calculator from the command line:

```zsh
python calculator/main.py "3 + 5 * 2"
```

Output is formatted as JSON:

```json
{
  "expression": "3 + 5 * 2",
  "result": 13
}
```

### AI Agent

The agent in `main.py` uses the Gemini API to answer coding questions and perform file operations. It:

- Lists available files
- Reads file contents
- Executes Python files
- Writes files

All operations are sandboxed to the working directory for security.

## Security

- File operations are restricted to the working directory.
- Large files are truncated to 10,000 characters.
- Only Python files can be executed.

## Extending

Add new functions to the `functions/` directory and update `function_call_part.py` to expose them to the agent.

## License

MIT License
