# AST Context Sanitizer & Token Optimizer

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An open-source AST parsing and structural sanitization engine designed to strip redundant syntax, boilerplate tokens, and non-functional context trees from Python software repositories before downstream processing in data pipelines and LLM context windows.

---

## Key Features
* **Semantic-Preserving AST Pruning:** Traverses Abstract Syntax Trees using Python's native `ast` module without breaking programmatic execution semantics.
* **Token Bloat Reduction:** Eliminates docstring clutter, redundant node expressions, and dead structural tokens.
* **Context Efficiency Metrics:** Computes real-time context compression ratios to benchmark pipeline bandwidth savings.

---

## Quickstart

```bash
# Clone the repository
git clone [https://github.com/your-username/ast-context-sanitizer.git](https://github.com/your-username/ast-context-sanitizer.git)
cd ast-context-sanitizer

# Install dependencies
pip install -r requirements.txt

# Run core script
python src/sanitizer.py