# iedit

`iedit` is a CLI tool for editing LaTeX files to improve their form, syntax, and grammar. It uses AI models from Amazon Bedrock to provide a polished version of your documents, similar to the ones published at top scientific conferences.

## Features

*   Connects to Amazon Bedrock to power the editing.
*   Allows you to specify which model to use (though currently hardcoded to `anthropic.claude-v2`).
*   Shows you the changes one by one before they are applied, with an interactive confirmation prompt.
*   Can process a single `.tex` file or all `.tex` files in a directory and its subdirectories.
*   Includes a mechanism to prevent changes to numerical values in your document.

## Installation

You can install `iedit` using `pip`:

```bash
pip install .
```

## Usage

To use `iedit`, you need to have your AWS credentials configured in your environment, with access to Amazon Bedrock.

To edit a single file:

```bash
iedit edit path/to/your/file.tex
```

To edit all `.tex` files in a directory:

```bash
iedit edit path/to/your/directory
```

The tool will then show you the proposed changes for each chunk of your document. You can accept or reject each change individually.

### Testing Bedrock Connection

You can test your connection to Bedrock with the following command:

```bash
iedit test-bedrock "Hello, Bedrock!"
```

## Known Limitations

*   The mechanism to retain numerical values currently only supports integers and simple floats. It might fail with more complex number formats.
*   The chunking of the LaTeX document is done by splitting the text by blank lines. This might not be optimal for all documents and could be improved to be more aware of the LaTeX structure.
*   The choice of the Bedrock model is currently hardcoded. This will be made configurable in a future version.
