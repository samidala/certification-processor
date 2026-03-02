import openai
from tenacity import retry, stop_after_attempt, wait_exponential
from src.llm.base import LLMProvider
from src.utils.config import config
import json
import logging

logger = logging.getLogger(__name__)

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o"):
        self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract(self, image_path: str, prompt: str, schema: dict):
        base64_image = self.encode_image(image_path)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
                response_format={"type": "json_object"},
            )
            
            content = response.choices[0].message.content
            usage = response.usage
            
            logger.info(f"Token Usage: {usage.total_tokens} (Cost approx: ${usage.total_tokens * 0.00001:.4f})")
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"OpenAI Extraction Error: {e}")
            raise
