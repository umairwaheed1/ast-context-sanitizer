import pytest
from src.sanitizer import ResearchASTSanitizer, SecurityInvariantError


@pytest.fixture
def sanitizer():
    return ResearchASTSanitizer()


def test_docstring_removal(sanitizer):
    raw_code = '''
def add_numbers(a: int, b: int) -> int:
    """This docstring should be pruned."""
    return a + b
'''
    clean_code, metrics = sanitizer.sanitize(raw_code, compress_locals=False)
    assert 'This docstring should be pruned' not in clean_code
    assert metrics['reduction_percentage'] > 0


def test_security_invariant_trigger(sanitizer):
    unsafe_code = '''
def execute_payload(user_input: str):
    eval(user_input)
'''
    with pytest.raises(SecurityInvariantError):
        sanitizer.sanitize(unsafe_code)