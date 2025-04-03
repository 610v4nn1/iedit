# iedit

A CLI tool for editing LaTeX files to improve their form, syntax and grammar using AI through Amazon Bedrock.

## Features

* Connect to AI models provided by Amazon Bedrock
* Specify which model to use to polish the document
* Interactive mode to review and confirm changes
* Make localized changes while preserving context
* Process multiple LaTeX documents in folders
* Preserve numerical values exactly

## Installation

```bash
pip install iedit
```

## Usage

Basic usage:

```bash
iedit document.tex
```

Process multiple files or directories:

```bash
iedit paper.tex thesis/
```

Specify a different AI model:

```bash
iedit --model anthropic.claude-v2 document.tex
```

Use a custom configuration file:

```bash
iedit --config myconfig.yaml document.tex
```

## Configuration

Configuration can be provided through a YAML file in either:
* `~/.config/iedit/config.yaml`
* `~/.iedit.yaml`
* Custom location specified with `--config`

Example configuration:

```yaml
model: anthropic.claude-v2
options:
  backup: true
  interactive: true
```

## Requirements

* Python 3.8 or later
* AWS credentials configured for Amazon Bedrock access

## License

MIT License