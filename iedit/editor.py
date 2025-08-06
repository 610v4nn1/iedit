import re
from pathlib import Path
from iedit.bedrock import BedrockClient
import typer

class LatexEditor:
    def __init__(self, file_path: Path, bedrock_client: BedrockClient):
        self.file_path = file_path
        self.bedrock_client = bedrock_client
        self.content = self.file_path.read_text()

    def _extract_numbers(self, text: str) -> list[str]:
        return re.findall(r'-?\d+(?:\.\d+)?', text)

    def get_chunks(self):
        # Split by one or more blank lines. This is a simple approach.
        # It might need to be refined to handle complex LaTeX structures.
        chunks = re.split(r'\n\s*\n', self.content)
        return [chunk for chunk in chunks if chunk.strip()]

    def edit(self):
        chunks = self.get_chunks()
        for chunk in chunks:
            prompt = self._create_prompt(chunk)
            polished_chunk = self.bedrock_client.invoke_model(prompt)

            if polished_chunk:
                original_numbers = self._extract_numbers(chunk)
                polished_numbers = self._extract_numbers(polished_chunk)

                if original_numbers != polished_numbers:
                    typer.echo(f"Warning: Numerical values were changed in a chunk. Reverting to original.", err=True)
                    yield chunk, chunk
                else:
                    yield chunk, polished_chunk
            else:
                yield chunk, None


    def _create_prompt(self, text: str) -> str:
        prompt = f"""
Please proofread and polish the following LaTeX text.
Fix any grammatical errors, improve the style, and ensure it is clear and concise.
Do not change any LaTeX commands or environments.
Do not change any numerical values.
Here is the text:

{text}
"""
        return prompt
