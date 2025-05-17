"""
Integration with Amazon Bedrock AI models.
"""

import json
import boto3
from typing import Dict, List, Optional
from botocore.exceptions import ClientError

class BedrockClient:
    """Client for interacting with Amazon Bedrock models."""
    
    def __init__(self, model: str = "anthropic.claude-v2", config: Optional[Dict] = None):
        """
        Initialize the Bedrock client.
        
        Args:
            model: The model ID to use
            config: Configuration dictionary with AWS settings
        """
        self.model = model
        self.config = config or {}
        
        # Initialize the Bedrock client
        session_kwargs = {}
        if self.config.get("aws_profile"):
            session_kwargs["profile_name"] = self.config["aws_profile"]
            
        session = boto3.Session(**session_kwargs)
        self.bedrock_client = session.client(
            service_name="bedrock-runtime",
            region_name=self.config.get("aws_region", "us-east-1")
        )
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the specified Bedrock model.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            The generated text
        """
        try:
            # Prepare the request body based on the model
            if self.model.startswith("anthropic.claude"):
                body = json.dumps({
                    "prompt": f"\\n\\nHuman: {prompt}\\n\\nAssistant:",
                    "max_tokens_to_sample": 4000,
                    "temperature": 0.5,
                    "top_p": 0.9,
                })
            elif self.model.startswith("amazon.titan"):
                body = json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 4000,
                        "temperature": 0.5,
                        "topP": 0.9,
                    }
                })
            elif self.model.startswith("ai21"):
                body = json.dumps({
                    "prompt": prompt,
                    "maxTokens": 4000,
                    "temperature": 0.5,
                    "topP": 0.9,
                })
            else:
                raise ValueError(f"Unsupported model: {self.model}")
            
            # Invoke the model
            response = self.bedrock_client.invoke_model(
                modelId=self.model,
                body=body
            )
            
            # Parse the response based on the model
            response_body = json.loads(response.get("body").read())
            
            if self.model.startswith("anthropic.claude"):
                return response_body.get("completion", "")
            elif self.model.startswith("amazon.titan"):
                return response_body.get("results", [{}])[0].get("outputText", "")
            elif self.model.startswith("ai21"):
                return response_body.get("completions", [{}])[0].get("data", {}).get("text", "")
            else:
                return ""
                
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            error_message = e.response.get("Error", {}).get("Message")
            raise Exception(f"Bedrock API error ({error_code}): {error_message}")
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")

def get_available_models() -> List[str]:
    """
    Get a list of available Amazon Bedrock models.
    
    Returns:
        List of model IDs
    """
    try:
        session = boto3.Session()
        bedrock_client = session.client(service_name="bedrock")
        
        response = bedrock_client.list_foundation_models()
        models = [model["modelId"] for model in response.get("modelSummaries", [])]
        
        # Filter to text generation models
        text_models = [
            model for model in models 
            if any(name in model for name in ["claude", "titan", "jurassic", "llama"])
        ]
        
        return text_models
    except Exception:
        # Return a default list of common models if we can't query the API
        return [
            "anthropic.claude-v2",
            "anthropic.claude-v2:1",
            "anthropic.claude-instant-v1",
            "amazon.titan-text-express-v1",
            "ai21.j2-ultra-v1",
        ]