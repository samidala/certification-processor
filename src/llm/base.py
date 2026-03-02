from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import base64
from pathlib import Path

class LLMProvider(ABC):
    @abstractmethod
    def extract(self, image_data: bytes, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Base method for LLM-based extraction."""
        pass

    @staticmethod
    def encode_image(image_path: Path) -> str:
        """Helper to encode image to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

class OCRResult:
    def __init__(self, raw_text: str, confidence: float, metadata: Optional[Dict[str, Any]] = None):
        self.raw_text = raw_text
        self.confidence = confidence
        self.metadata = metadata or {}
