⚙️ Installation
Clone the repository and set up your virtual environment:

PowerShell
# Clone repository
git clone [https://github.com/your-username/ast-context-sanitizer.git](https://github.com/your-username/ast-context-sanitizer.git)
cd ast-context-sanitizer

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
🚀 Quickstart Usage
1. CLI Execution
Sanitize a single module or entire folder and print token savings:

Bash
python main.py sanitize --input ./src/ast_context_sanitizer --output ./dist/sanitized
2. Programmatic Python API
Python
from ast_context_sanitizer import ASTSanitizer

code_snippet = """
def process_data(records: list[dict]) -> dict:
    \"\"\"Process raw database records and extract metrics.\"\"\"
    # Strip unnecessary loops and memory allocations for prompt context
    processed = {}
    for item in records:
        processed[item['id']] = item['value'] * 2
    return processed
"""

sanitizer = ASTSanitizer(strip_docstrings=True, keep_signatures=True)
sanitized_code = sanitizer.sanitize(code_snippet)

print(sanitized_code)
# Output:
# def process_data(records: list[dict]) -> dict:
#     pass
🧪 Running Tests
Ensure all AST transformation and token calculation modules are working correctly:

Bash
pytest tests/ -v
📄 License
Distributed under the MIT License. See LICENSE for more details.