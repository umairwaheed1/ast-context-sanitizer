# AST Context Sanitizer 🔬

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AST Context Sanitizer** is an academic-grade Python static analysis tool designed to reduce large language model (LLM) context window bloat. By leveraging Python's built-in Abstract Syntax Tree (`ast`) module and OpenAI's `tiktoken` library, it strips non-essential implementation details while preserving code structure and verifying strict security invariants.

---

## ✨ Key Features

* **AST-Based Transformation:** Replaces function bodies with `pass` statements and strips docstrings to drastically lower token counts.
* **Scope-Safe Identifier Compression:** Compresses local variable names efficiently within function scopes.
* **Dead Code Branch Pruning:** Eliminates unreachable branches through static constant evaluation.
* **Security Invariant Verification:** Detects and flags unsafe dynamic execution calls (`eval`, `exec`, `__import__`).
* **Precise Token Metrics:** Calculates exact token reductions using `tiktoken` encodings (`cl100k_base`).


📁 **Project Architecture**

**text**
ast-context-sanitizer/
├── .github/workflows/      # CI/CD verification pipelines
├── docs/                   # Technical reports and documentation
├── src/                    # Core package source code
│   ├── __init__.py         # Package entry points & exports
│   ├── sanitizer.py        # Core AST transformer & sanitization logic
│   ├── metrics.py          # Token calculation utilities
│   └── cli.py              # Command-line interface handler
├── tests/                  # Unit test suite (pytest)
├── main.py                 # Root execution launcher
├── benchmark.py            # Performance benchmarking script
└── requirements.txt        # Project dependencies


**🚀 Installation & Setup**
Clone the Repository:


git clone [https://github.com/umairwaheed1/ast-context-sanitizer.git](https://github.com/umairwaheed1/ast-context-sanitizer.git)
cd ast-context-sanitizer
Create and Activate Virtual Environment:


python -m venv .venv
.venv\Scripts\Activate.ps1

**Install Dependencies:**

pip install -r requirements.txt
💻 **Usage**
Command-Line Interface (CLI)
Run the sanitizer directly on any Python script to view token savings and output the optimized code:


python main.py -i benchmark.py
To save the sanitized code to a separate output file:


python main.py -i benchmark.py -o sanitized_output.py

from src.sanitizer import ResearchASTSanitizer

sanitizer = ResearchASTSanitizer()
source_code = '''
def complex_algorithm(data: list) -> int:
    """Detailed docstring."""
    total = sum(data)
    return total
'''

optimized_code, metrics = sanitizer.sanitize(source_code)
print(optimized_code)
print(f"Token Reduction: {metrics['reduction_percentage']}%")

🧪** Running Tests**
**Execute the unit test suite using pytest:**
pytest tests/ -v
