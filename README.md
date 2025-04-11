# iedit

A CLI tool for editing LaTeX files to improve their form, syntax and grammar using AI via Amazon Bedrock.

## Features

- Connect to AI models provided by Amazon Bedrock
- Specify which model to use to polish the document
- Interactive mode to review and confirm changes
- Process single files or entire directories
- Preserve numerical values and LaTeX commands
- Create backups before making changes

## Installation

```bash
pip install iedit
```

## Usage

Basic usage:

```bash
# Process a single file
iedit document.tex

# Process all .tex files in a directory
iedit path/to/directory

# Process directory recursively
iedit -r path/to/directory

# Use a specific Bedrock model
iedit -m anthropic.claude-v2 document.tex

# Use a custom configuration file
iedit -c config.yaml document.tex
```

## Configuration

You can create a `.iedit.yaml` file in your home directory or specify a custom config file with the `-c` option. Example configuration:

```yaml
model: anthropic.claude-v2
# Additional configuration options can be added here
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/iedit.git
cd iedit

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run tests
pytest
```

## License

MIT License