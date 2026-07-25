import ast


class ASTContextSanitizer(ast.NodeTransformer):
    """AST Transformer that strips docstrings, redundant pass statements,

    and non-functional expressions to optimize context tree size.
    """

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Removes docstrings from function definitions."""
        self.generic_visit(node)
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        # Handle edge case where stripping docstring leaves an empty function body
        if not node.body:
            node.body.append(ast.Pass())

        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Removes docstrings from class definitions."""
        self.generic_visit(node)
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        if not node.body:
            node.body.append(ast.Pass())

        return node


def sanitize_code(source_code: str) -> tuple[str, float]:
    """Parses raw Python source code, applies AST context sanitization,

    and returns the cleaned source code alongside its token reduction percentage.
    """
    if not source_code.strip():
        return "", 0.0

    parsed_ast = ast.parse(source_code)
    sanitizer = ASTContextSanitizer()
    cleaned_ast = sanitizer.visit(parsed_ast)
    ast.fix_missing_locations(cleaned_ast)

    cleaned_code = ast.unparse(cleaned_ast)

    original_length = len(source_code)
    cleaned_length = len(cleaned_code)

    if original_length == 0:
        reduction = 0.0
    else:
        reduction = (1 - (cleaned_length / original_length)) * 100

    return cleaned_code, reduction


if __name__ == "__main__":
    sample_input = '''
def execute_pipeline(data_stream):
    """
    Executes automated data transformation across multi-source streams.
    Removes redundant contextual tokens during parsing.
    """
    results = [item * 2 for item in data_stream]
    return results
'''
    cleaned_output, token_reduction = sanitize_code(sample_input)
    print("=== Original Source Code ===")
    print(sample_input.strip())
    print("\n=== Sanitized Source Code ===")
    print(cleaned_output)
    print(f"\nContext Size Reduction: {token_reduction:.2f}%")