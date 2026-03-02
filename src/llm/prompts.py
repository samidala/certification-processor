import yaml
from pathlib import Path
from src.utils.config import config
import logging
import json

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self, prompts_dir: Path = config.CONFIG_DIR / "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(parents=True, exist_ok=True)

    def get_prompt(self, version: str = "v1") -> str:
        """Loads prompt from YAML file based on version."""
        prompt_path = self.prompts_dir / f"extraction_{version}.yaml"
        if not prompt_path.exists():
            logger.warning(f"Prompt version {version} not found at {prompt_path}. Using default.")
            return self._get_default_prompt()
            
        try:
            with open(prompt_path, "r") as f:
                prompt_data = yaml.safe_load(f)
                system = prompt_data.get("system_prompt", "")
                user = prompt_data.get("user_prompt", "")
                return f"{system}\n{user}".strip()
        except Exception as e:
            logger.error(f"Error loading prompt {version}: {e}")
            return self._get_default_prompt()

    def _get_default_prompt(self) -> str:
        return """
        Extract structured data from the provided death certificate image.
        Return ONLY a JSON object conforming to the specified schema.
        Include a confidence score (0.0 to 1.0) and extraction notes.
        """

class ExampleManager:
    def __init__(self, examples_file: Path = config.CONFIG_DIR / "examples" / "examples.yaml"):
        self.examples_file = Path(examples_file)
        self.examples_file.parent.mkdir(parents=True, exist_ok=True)

    def get_few_shot_examples(self, count: int = 1) -> str:
        """Loads examples to be included in the prompt."""
        if not self.examples_file.exists():
            return ""
            
        try:
            with open(self.examples_file, "r") as f:
                examples_data = yaml.safe_load(f)
                examples = examples_data.get("examples", [])
                
                shot_text = "### Few-Shot Examples\n"
                for ex in examples[:count]:
                    shot_text += f"- Input: {ex.get('description', 'Document')}\n"
                    shot_text += f"  Output: {json.dumps(ex.get('output', {}))}\n"
                return shot_text
        except Exception as e:
            logger.error(f"Error loading examples: {e}")
            return ""
