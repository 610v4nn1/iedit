"""
Tests for the LaTeX editor functionality.
"""
import pytest
from pathlib import Path
from iedit.editor import LatexEditor
from iedit.config import Config


@pytest.fixture
def editor():
    return LatexEditor(model_id='anthropic.claude-v2', config=Config())


def test_split_content(editor):
    content = r"""
    \section{Introduction}
    This is a test paragraph.
    With multiple lines.
    
    This is another paragraph.
    Also with multiple lines.
    """
    chunks = editor._split_content(content)
    assert len(chunks) == 2
    assert "This is a test paragraph." in chunks[0]
    assert "This is another paragraph." in chunks[1]


def test_apply_suggestions(editor):
    chunk = "This is a test sentense with a typo."
    suggestions = [("sentense", "sentence")]
    
    # Simulate user confirming the change
    def mock_confirm(*args, **kwargs):
        return True
        
    import click
    original_confirm = click.confirm
    click.confirm = mock_confirm
    
    try:
        result = editor._apply_suggestions(chunk, suggestions)
        assert result == "This is a test sentence with a typo."
    finally:
        click.confirm = original_confirm