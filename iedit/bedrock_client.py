"""
Client for interacting with Amazon Bedrock.
"""

import json
import boto3
from typing import Dict, Optional, Any


class BedrockClient:
    """
    Client for interacting with Amazon Bedrock models.
    """
    
    def __init__(self, model: str, profile: Optional[str] = None, region: str = "us-west-2"):
        """
        Initialize the Bedrock client.
        
        Args:
            model: The Bedrock model ID to use
            profile: AWS profile to use (optional)
            region: AWS region to use
        """
        self.model = model
        self.region = region
        
        # Create a boto3 session with the specified profile
        if profile:
            session = boto3.Session(profile_name=profile, region_name=region)
        else:
            session = boto3.Session(region_name=region)
            
        self.bedrock_runtime = session.client(
            service_name="bedrock-runtime",
            region_name=region
        )
        
    def improve_latex(self, latex_content: str) -> str:
        """
        Improve the form, syntax, and grammar of LaTeX content.
        
        Args:
            latex_content: The LaTeX content to improve
            
        Returns:
            Improved LaTeX content
        """
        # Determine which model provider we're using and format the prompt accordingly
        if "anthropic.claude" in self.model:
            return self._call_claude_model(latex_content)
        else:
            # Default to Claude format
            return self._call_claude_model(latex_content)
    
    def _call_claude_model(self, latex_content: str) -> str:
        """
        Call Claude model to improve LaTeX content.
        
        Args:
            latex_content: The LaTeX content to improve
            
        Returns:
            Improved LaTeX content
        """
        prompt = f"""
        You are an expert LaTeX editor. Your task is to improve the form, syntax, and grammar of the LaTeX content provided below.
        
        Guidelines:
        - Fix grammatical errors and improve phrasing
        - Ensure consistent style and formatting
        - Maintain the original meaning and intent
        - Preserve all mathematical formulas and their meaning
        - Keep all numerical values exactly as they are
        - Do not add or remove substantive content
        - Return only the improved LaTeX content, without explanations
        
        Here is the LaTeX content to improve:
        
        ```latex
        {latex_content}
        ```
        """
        
        # Prepare the request payload for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100000,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Invoke the model
        response = self.bedrock_runtime.invoke_model(
            modelId=self.model,
            body=json.dumps(request_body)
        )
        
        # Parse the response
        response_body = json.loads(response.get("body").read())
        improved_content = response_body.get("content", [{}])[0].get("text", "")
        
        # Extract the LaTeX content if it's wrapped in code blocks
        if "```latex" in improved_content and "```" in improved_content:
            start_idx = improved_content.find("```latex") + 8
            end_idx = improved_content.rfind("```")
            improved_content = improved_content[start_idx:end_idx].strip()
        elif "```" in improved_content:
            start_idx = improved_content.find("```") + 3
            end_idx = improved_content.rfind("```")
            improved_content = improved_content[start_idx:end_idx].strip()
            
        return improved_content
