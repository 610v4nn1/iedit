from typer.testing import CliRunner
from pathlib import Path
import pytest
from iedit.main import app

runner = CliRunner()

class MockBedrockClient:
    def invoke_model(self, prompt: str, model_id="anthropic.claude-v2"):
        original_chunk = prompt.split("Here is the text:\n\n")[-1]
        return original_chunk.replace("original", "polished").replace("Original", "Polished")

@pytest.fixture
def mock_bedrock_client(monkeypatch):
    monkeypatch.setattr("iedit.main.BedrockClient", MockBedrockClient)

def test_edit_apply(mock_bedrock_client, tmp_path):
    # Create a dummy file in a temporary directory
    test_file = tmp_path / "test.tex"
    test_file.write_text("This is the original version.")

    # Run the edit command and answer "y" to the confirmation
    result = runner.invoke(app, ["edit", str(test_file)], input="y\n")

    assert result.exit_code == 0
    assert "saved." in result.stdout

    # Check that the file was modified
    new_content = test_file.read_text()
    assert new_content.strip() == "This is the polished version."

def test_edit_reject(mock_bedrock_client, tmp_path):
    # Create a dummy file in a temporary directory
    test_file = tmp_path / "test.tex"
    original_content = "This is the original version."
    test_file.write_text(original_content)

    # Run the edit command and answer "n" to the confirmation
    result = runner.invoke(app, ["edit", str(test_file)], input="n\n")

    assert result.exit_code == 0
    assert "saved." in result.stdout

    # Check that the file was NOT modified
    new_content = test_file.read_text()
    assert new_content == original_content


def test_edit_directory(mock_bedrock_client, tmp_path):
    # Create a directory structure
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()

    tex_file1 = tmp_path / "file1.tex"
    tex_file1.write_text("Original content 1")

    tex_file2 = sub_dir / "file2.tex"
    tex_file2.write_text("Original content 2")

    other_file = tmp_path / "file3.txt"
    other_file.write_text("This should not be touched")

    # Run the edit command on the directory
    result = runner.invoke(app, ["edit", str(tmp_path)], input="y\ny\n")

    assert result.exit_code == 0

    # Check that both .tex files were modified
    assert tex_file1.read_text().strip() == "Polished content 1"
    assert tex_file2.read_text().strip() == "Polished content 2"

    # Check that the other file was not touched
    assert other_file.read_text() == "This should not be touched"


def test_edit_number_change_rejects(monkeypatch, tmp_path):
    class MockBedrockClientNumbersChanged:
        def invoke_model(self, prompt: str, model_id="anthropic.claude-v2"):
            return "The polished version has the number 20."

    monkeypatch.setattr("iedit.main.BedrockClient", MockBedrockClientNumbersChanged)

    test_file = tmp_path / "test.tex"
    original_content = "The original version has the number 10."
    test_file.write_text(original_content)

    result = runner.invoke(app, ["edit", str(test_file)], input="y\n")

    assert result.exit_code == 0
    assert "Warning: Numerical values were changed" in result.stdout
    assert test_file.read_text() == original_content

def test_edit_number_same_applies(monkeypatch, tmp_path):
    class MockBedrockClientNumbersSame:
        def invoke_model(self, prompt: str, model_id="anthropic.claude-v2"):
            return "The polished version has the number 10, but is otherwise different."

    monkeypatch.setattr("iedit.main.BedrockClient", MockBedrockClientNumbersSame)

    test_file = tmp_path / "test.tex"
    original_content = "The original version has the number 10."
    test_file.write_text(original_content)

    result = runner.invoke(app, ["edit", str(test_file)], input="y\n")

    assert result.exit_code == 0
    assert "Warning: Numerical values were changed" not in result.stdout
    assert test_file.read_text() == "The polished version has the number 10, but is otherwise different."
