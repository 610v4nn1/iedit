"""
Tests for the command-line interface
"""
import pytest
from click.testing import CliRunner
from iedit.cli import main

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Edit LaTeX files' in result.output

def test_cli_invalid_file(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['nonexistent.tex'])
        assert result.exit_code == 1
        
def test_cli_non_tex_file(runner):
    with runner.isolated_filesystem():
        with open('test.txt', 'w') as f:
            f.write('Some content')
        result = runner.invoke(main, ['test.txt'])
        assert result.exit_code == 1
        assert 'not a LaTeX file' in result.output