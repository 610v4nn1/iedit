"""
Tests for the LaTeX editor functionality.
"""
import pytest
from pathlib import Path
from iedit.editor import LatexEditor
from iedit.config import Config
import json
from unittest.mock import MagicMock


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


def test_get_suggestions(editor):
    # Mock the Bedrock client response
    mock_response = {
        'body': MagicMock()
    }
    mock_response['body'].read.return_value = json.dumps({
        'completion': '''
Original: This is a sentense with a typo.
Suggestion: This is a sentence with a typo.

Original: LaTeX formating command
Suggestion: LaTeX formatting command
'''
    }).encode()
    
    editor.bedrock = MagicMock()
    editor.bedrock.invoke_model.return_value = mock_response
    
    # Test getting suggestions
    chunk = "This is a test paragraph with LaTeX formating command"
    suggestions = editor._get_suggestions(chunk)
    
    # Verify the request format
    call_args = editor.bedrock.invoke_model.call_args[1]
    request_body = json.loads(call_args['body'].decode())
    
    assert 'prompt' in request_body
    assert 'max_tokens_to_sample' in request_body
    assert 'anthropic_version' in request_body
    
    # Verify suggestions parsing
    assert len(suggestions) == 2
    assert suggestions[0] == ("This is a sentense with a typo.", "This is a sentence with a typo.")
    assert suggestions[1] == ("LaTeX formating command", "LaTeX formatting command")