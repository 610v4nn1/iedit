# iedit

A CLI tool for editing LaTeX files to improve their form, syntax, and grammar. Its aim is to provide a polished version of the document, similar to the ones published at top scientific conferences. The tool is inspired by ispell but it targets significantly more complex changes, thanks to the usage of AI.

## Features

`iedit` allows you to:

* Connect to the AI models provided by Amazon Bedrock
* Specify which model to use to polish the document
* See the changes one by one before they are applied to the files (with your confirmation)
* Make localized changes in the document, while offering sufficient context to evaluate the impact
* Specify folders containing several LaTeX documents to polish all of them
* Retain exactly the numerical values provided in the LaTeX documents

## Installation

You can easily install `iedit` using pip:

```bash
pip install iedit
```

## Usage

Basic usage:

```bash
iedit path/to/your/file.tex
```

Process all LaTeX files in a directory:

```bash
iedit path/to/your/directory/
```

Specify a specific Amazon Bedrock model:

```bash
iedit --model claude-v2 path/to/your/file.tex
```

For more options:

```bash
iedit --help
```

## Configuration

By default, iedit uses your AWS credentials for accessing Amazon Bedrock. Make sure you have configured your AWS credentials using:

```bash
aws configure
```

You can also set specific AWS credentials for iedit in a configuration file at `~/.iedit/config.yaml`.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.