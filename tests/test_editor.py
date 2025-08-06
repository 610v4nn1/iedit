from pathlib import Path
import pytest
from iedit.editor import LatexEditor

class MockBedrockClient:
    def invoke_model(self, prompt: str, model_id="anthropic.claude-v2"):
        return ""

@pytest.fixture
def editor(tmp_path):
    test_file = tmp_path / "test.tex"
    test_file.write_text("Hello world.\n\nThis is a test.\n\n\\section{test}")
    bedrock_client = MockBedrockClient()
    return LatexEditor(test_file, bedrock_client)

def test_get_chunks(editor):
    chunks = editor.get_chunks()
    assert len(chunks) == 3
    assert chunks[0] == "Hello world."
    assert chunks[1] == "This is a test."
    assert chunks[2] == "\\section{test}"

def test_extract_numbers(editor):
    numbers = editor._extract_numbers("The answer is 42, not -10.5.")
    assert numbers == ["42", "-10.5"]
