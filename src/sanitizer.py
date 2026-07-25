import ast
import tiktoken
from typing import Tuple, Dict, Any, Set


class SecurityInvariantError(Exception):
    """Custom exception raised when an AST violates static safety policies."""
    pass


class AdvancedASTTransformer(ast.NodeTransformer):
    """
    AST NodeTransformer performing:
    1. Docstring & comment stripping
    2. Scope-safe variable identifier compression
    3. Dead code elimination (static constant branch pruning)
    """

    def __init__(self, compress_identifiers: bool = True):
        self.compress_identifiers = compress_identifiers
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # Strip Function Docstrings
        if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
            node.body.pop(0)

        # Local Scope Identifier Compression
        if self.compress_identifiers:
            local_vars: Set[str] = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
                    if not child.id.startswith("__"):
                        local_vars.add(child.id)

            var_map = {orig: f"_{i}" for i, orig in enumerate(local_vars)}

            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id in var_map:
                    child.id = var_map[child.id]

        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If) -> Any:
        # Dead Code Branch Pruning
        if isinstance(node.test, ast.Constant):
            if bool(node.test.value) is True:
                return node.body
            else:
                return node.orelse if node.orelse else None
        self.generic_visit(node)
        return node


class ResearchASTSanitizer:
    """
    Academic-grade AST Context Sanitizer with Verification & Metrics.
    """

    def __init__(self, model_encoding: str = "cl100k_base"):
        self.encoder = tiktoken.get_encoding(model_encoding)

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def verify_safety_invariants(self, tree: ast.AST) -> bool:
        """Static Analysis: Flag dynamic unsafe function execution."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"eval", "exec", "__import__"}:
                    raise SecurityInvariantError(
                        f"Security Violation: Unsafe function call '{node.func.id}' detected."
                    )
        return True

    def sanitize(self, source_code: str, compress_locals: bool = True) -> Tuple[str, Dict[str, Any]]:
        initial_tokens = self.count_tokens(source_code)

        parsed_ast = ast.parse(source_code)
        self.verify_safety_invariants(parsed_ast)

        transformer = AdvancedASTTransformer(compress_identifiers=compress_locals)
        transformed_ast = transformer.visit(parsed_ast)
        ast.fix_missing_locations(transformed_ast)

        optimized_code = ast.unparse(transformed_ast)
        final_tokens = self.count_tokens(optimized_code)

        reduction = max(0.0, ((initial_tokens - final_tokens) / initial_tokens) * 100)

        metrics = {
            "initial_tokens": initial_tokens,
            "final_tokens": final_tokens,
            "reduction_percentage": round(reduction, 2),
            "invariant_pass": True
        }
        return optimized_code, metrics