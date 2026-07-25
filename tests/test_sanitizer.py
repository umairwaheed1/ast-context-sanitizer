import ast
import tiktoken
import pytest


# Simple AST transformer logic
class ASTContextSanitizer(ast.NodeTransformer):
    """AST Transformer that replaces function bodies with 'pass' and strips docstrings."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # Re-visit child nodes first if necessary
        self.generic_visit(node)

        # Replace implementation body with a single 'pass' node
        node.body = [ast.Pass()]
        node.decorator_list = []  # Optionally strip decorators

        # CRITICAL FIX: Return the node itself, NOT 'self'
        return node


def sanitize_code(source_code: str) -> str:
    """Parses Python source code, transforms AST, and unparses back to string."""
    parsed_ast = ast.parse(source_code)
    sanitizer = ASTContextSanitizer()
    transformed_ast = sanitizer.visit(parsed_ast)
    ast.fix_missing_locations(transformed_ast)
    return ast.unparse(transformed_ast)


def count_tokens(text: str, model_encoding: str = "cl100k_base") -> int:
    """Calculates token counts using OpenAI's tiktoken library."""
    encoding = tiktoken.get_encoding(model_encoding)
    return len(encoding.encode(text))


# --- TEST CASES ---

@pytest.fixture
def sample_python_code():
    return """
def calculate_financial_metrics(records: list[dict]) -> dict:
    \"\"\"
    Process dense ledger transactions and calculate yield ratios.
    This docstring contains descriptive text that bloats LLM context windows.
    \"\"\"
    # Iterative processing over records
    total_revenue = 0.0
    for row in records:
        margin = row.get("revenue", 0) - row.get("cost", 0)
        total_revenue += margin

    return {"status": "complete", "yield": total_revenue}
"""


def test_ast_strips_implementation_body(sample_python_code):
    """Verifies that internal function logic is replaced by 'pass'."""
    sanitized = sanitize_code(sample_python_code)

    # Assert signature exists but implementation loops are removed
    assert "def calculate_financial_metrics(records: list[dict]) -> dict:" in sanitized
    assert "for row in records:" not in sanitized
    assert "total_revenue += margin" not in sanitized
    assert "pass" in sanitized


def test_token_count_reduction(sample_python_code):
    """Verifies that token counts drop significantly after AST sanitization."""
    raw_tokens = count_tokens(sample_python_code)
    sanitized_code = sanitize_code(sample_python_code)
    sanitized_tokens = count_tokens(sanitized_code)

    # Calculate token savings percentage
    savings_pct = ((raw_tokens - sanitized_tokens) / raw_tokens) * 100

    print(
        f"\n[BENCHMARK] Raw Tokens: {raw_tokens} | Sanitized Tokens: {sanitized_tokens} | Reduction: {savings_pct:.2f}%")

    # Assert that token count decreased by at least 40%
    assert sanitized_tokens < raw_tokens
    assert savings_pct >= 40.0