"""
Tests for the LaTeX editor functionality
"""
import pytest
from unittest.mock import Mock, patch
from iedit.editor import LatexEditor

@pytest.fixture
def editor():
    return LatexEditor(model="anthropic.claude-v2")

def test_split_content(editor):
    content = """
    First paragraph with some
    text here.
    
    Second paragraph with
    more text.
    
    Third one.
    """
    chunks = editor._split_content(content)
    assert len(chunks) == 3
    assert "First paragraph" in chunks[0]
    assert "Second paragraph" in chunks[1]
    assert "Third one" in chunks[2]

@patch('boto3.client')
def test_get_suggestions(mock_boto, editor):
    mock_response = Mock()
    mock_response.return_value = {
        'body': b'Improved version of the text'
    }
    mock_client = Mock()
    mock_client.invoke_model = mock_response
    mock_boto.return_value = mock_client
    
    text = "Original text"
    suggestions = editor._get_suggestions(text)
    
    assert len(suggestions) == 1
    original, suggested = suggestions[0]
    assert original == text
    assert suggested == "Improved version of the text"

def test_get_suggestions_no_change(editor):
    with patch('boto3.client') as mock_boto:
        mock_response = Mock()
        mock_response.return_value = {
            'body': b'NONE'
        }
        mock_client = Mock()
        mock_client.invoke_model = mock_response
        mock_boto.return_value = mock_client
        
        text = "Perfect text"
        suggestions = editor._get_suggestions(text)
        assert len(suggestions) == 0

def test_get_suggestions_error(editor):
    with patch('boto3.client') as mock_boto:
        mock_client = Mock()
        mock_client.invoke_model.side_effect = Exception("API Error")
        mock_boto.return_value = mock_client
        
        text = "Some text"
        suggestions = editor._get_suggestions(text)
        assert len(suggestions) == 0