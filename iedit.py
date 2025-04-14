import argparse
import sys
import boto3
import json
import os

def main():
    parser = argparse.ArgumentParser(
        prog="iedit", description="CLI tool for editing Latex files to improve their form, syntax, and grammar."
    )

    parser.add_argument("files", nargs="*", help="Paths to LaTeX files or directories containing LaTeX files.")
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="claude-3-opus-20240229",  # replace with a valid default model if available
        help="Specify the AI model to use for polishing (e.g., claude-3-opus-20240229).",
    )
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        help="Make localized changes, showing context and requiring confirmation for each change.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 0.1.0"
    )  # Changed version format

    args = parser.parse_args()

    try:
        # Initialize Bedrock client
        bedrock = boto3.client("bedrock-runtime")  # Assuming default region and credentials are set
        print("Successfully connected to Amazon Bedrock.")
    except Exception as e:
        print(f"Error connecting to Amazon Bedrock: {e}")
        sys.exit(1)

    if not args.files:
        parser.print_help()
        sys.exit(1)

    print(f"Using model: {args.model}")

    process_files(bedrock, args.files, args.model, args.local)

def process_files(bedrock, paths, model_id, local_mode):
    for path in paths:
        if os.path.isfile(path):
            if path.endswith(".tex"):
                process_file(bedrock, path, model_id, local_mode)
            else:
                print(f"Skipping non-LaTeX file: {path}")
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".tex"):
                        process_file(bedrock, os.path.join(root, file), model_id, local_mode)
        else:
            print(f"Invalid path: {path}")

def process_file(bedrock, file_path, model_id, local_mode):
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r") as f:
            content = f.read()

        polished_content = polish_latex(bedrock, content, model_id)

        if local_mode:
            apply_changes_interactive(file_path, content, polished_content)
        else:
            with open(file_path, "w") as f:
                f.write(polished_content)
            print(f"Polished version saved to: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def polish_latex(bedrock, latex_content, model_id):
    try:
        prompt = f"""Polish the grammar, syntax, and style of the following LaTeX document to improve its quality for publication. Retain all numerical values exactly as they are. Provide the polished LaTeX code as output, without any explanations or additional text.

        

if __name__ == "__main__":
    main()