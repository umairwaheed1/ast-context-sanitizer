from src.sanitizer import sanitize_code


def test_docstring_removal_function():
    raw_code = '''def test_fn():
    """This docstring should be removed."""
    return True'''

    cleaned, reduction = sanitize_code(raw_code)
    assert '"""This docstring should be removed."""' not in cleaned
    assert "return True" in cleaned
    assert reduction > 0


def test_empty_string():
    cleaned, reduction = sanitize_code("")
    assert cleaned == ""
    assert reduction == 0.0


def test_class_docstring_removal():
    raw_code = '''class DataPipeline:
    """Class docstring to strip."""
    def process(self):
        pass'''

    cleaned, _ = sanitize_code(raw_code)
    assert '"""Class docstring to strip."""' not in cleaned
    assert "class DataPipeline" in cleaned