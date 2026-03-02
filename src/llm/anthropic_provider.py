import anthropic
import base64
from tenacity import retry, stop_after_attempt, wait_exponential
from src.llm.base import LLMProvider
from src.utils.config import config
import json
import logging

logger = logging.getLogger(__name__)

class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-3-5-sonnet-20240620"):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract(self, image_path: str, prompt: str, schema: dict):
        base64_image = self.encode_image(image_path)
        media_type = "image/jpeg" # Defaulting to jpeg
        
        try:
            # Claude requires schema description in the system prompt usually
            # or as part of the tool use. Here we'll append it to the prompt.
            full_prompt = f"{prompt}\n\nReturn ONLY a JSON object conforming to this schema: {json.dumps(schema)}"
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": full_prompt
                            }
                        ],
                    }
                ],
            )
            
            content = response.content[0].text
            # Basic cost estimation for Claude 3.5 Sonnet
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            logger.info(f"Anthropic Usage: In={input_tokens}, Out={output_tokens}")
            
            # Extract JSON from potential conversational filler
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            return json.loads(content[json_start:json_end])
            
        except Exception as e:
            logger.error(f"Anthropic Extraction Error: {e}")
            raise
