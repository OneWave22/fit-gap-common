import pytest
import os
from core.pdf import extract_text_from_pdf

def test_extract_text_from_valid_pdf():
    # Use the created test.pdf
    text = extract_text_from_pdf("tests/test.pdf")
    assert "Hello World" in text

def test_extract_text_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("non_existent.pdf")

def test_extract_text_unsupported_extension():
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_text_from_pdf("test.txt")
