# iedit

A CLI tool for editing LaTeX files to improve their form, syntax, and grammar using AI.

## Overview

`iedit` is a CLI tool for editing LaTeX files to improve their form, syntax, and grammar. Its aim is to provide a polished version of the document, similar to those published at top scientific conferences.
The tool is inspired by ispell but targets significantly more complex changes, thanks to the usage of AI.

## Main Features

`iedit` allows you to:
* Connect to AI models provided by Amazon Bedrock
* Specify which model to use to polish the document
* See the changes one by one before they are applied to the files (with your confirmation)
* Make localized changes in the document, while offering sufficient context to evaluate the impact
* Specify folders containing several LaTeX documents to polish all of them
* Retain exactly the numerical values provided in the LaTeX documents

## Installation

```
pip install iedit
```

## Usage

```
iedit [OPTIONS] FILE_OR_DIRECTORY
```

### Options

- `--model MODEL`: Specify the Bedrock model to use (default: claude-3-sonnet)
- `--recursive`: Process directories recursively
- `--profile PROFILE`: AWS profile to use
- `--region REGION`: AWS region to use (default: us-west-2)
- `--help`: Show help message and exit

## Examples

Polish a single LaTeX file:
```
iedit paper.tex
```

Polish all LaTeX files in a directory:
```
iedit --recursive papers/
```

Use a specific Bedrock model:
```
iedit --model anthropic.claude-3-opus-20240229-v1:0 paper.tex
```

## Requirements

- Python 3.8+
- AWS account with access to Amazon Bedrock
- Configured AWS credentials
