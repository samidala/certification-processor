from pathlib import Path
import logging
from src.ocr.processor import ImagePreprocessor
from src.llm.openai_provider import OpenAIProvider
from src.llm.anthropic_provider import AnthropicProvider
from src.llm.prompts import PromptManager, ExampleManager
from src.validation.schema import DeathCertificateSchema
from src.utils.config import config
from src.validation.engine import ValidationEngine
from src.reporting.metrics import MetricsLogger, AccuracyTracker
import json
import time

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

class DeathCertificateExtractor:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        
        # Select Provider
        if config.DEFAULT_LLM_PROVIDER == "anthropic":
            self.llm_provider = AnthropicProvider(model=config.LLM_MODEL)
        else:
            self.llm_provider = OpenAIProvider(model=config.LLM_MODEL)
            
        self.prompt_manager = PromptManager()
        self.example_manager = ExampleManager()
        self.metrics_logger = MetricsLogger()
        self.accuracy_tracker = AccuracyTracker()

    def process_document(self, image_path: str):
        logger.info(f"Processing document: {image_path}")
        start_time = time.time()
        
        # 0. Preprocessing (Optional, for now we log it)
        # processed_img = self.preprocessor.process(image_path)
        
        # 1. Prompt Preparation
        base_prompt = self.prompt_manager.get_prompt(config.PROMPT_VERSION)
        examples = self.example_manager.get_few_shot_examples(count=1)
        full_prompt = f"{base_prompt}\n\n{examples}"
        
        schema = DeathCertificateSchema.model_json_schema()
        
        try:
            # 2. Extraction
            raw_extraction = self.llm_provider.extract(image_path, full_prompt, schema)
            latency = time.time() - start_time
            
            # Log raw for debugging if enabled
            if config.ENABLE_RAW_LOGGING:
                self.metrics_logger.log_debug(Path(image_path).name, full_prompt, json.dumps(raw_extraction))
            
            # 3. Validation & Scoring
            is_valid, confidence, issues = ValidationEngine.validate(raw_extraction)
            self.accuracy_tracker.update(confidence, is_valid, issues)
            
            # 4. Logging Metrics
            # In a real system, tokens/cost would come from the provider
            # OpenAI already logs them in its provider, but we need them here too
            # For simplicity, we'll use placeholders if not returned
            tokens = raw_extraction.get("usage", {}).get("total_tokens", 1000)
            cost = tokens * 0.00001 # Placeholder
            
            self.metrics_logger.log_extraction(
                doc_id=Path(image_path).name,
                tokens=tokens, 
                cost=cost, 
                latency=latency,
                confidence=confidence,
                status="success" if is_valid else "flagged",
                error=None if is_valid else "; ".join(issues)
            )
            
            if not is_valid:
                return ValidationEngine.flag_for_human_review(Path(image_path).name, raw_extraction, issues)
            
            return DeathCertificateSchema(**raw_extraction)
            
        except Exception as e:
            logger.error(f"Failed to process {image_path}: {e}")
            self.metrics_logger.log_extraction(
                doc_id=Path(image_path).name,
                tokens=0, cost=0, latency=time.time()-start_time,
                confidence=0.0, status="error", error=str(e)
            )
            return {"error": str(e)}

    def batch_process(self, input_dir: str, output_dir: str):
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        for img_file in input_path.glob("*"):
            if img_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".pdf"]:
                result = self.process_document(str(img_file))
                
                # Save individual result
                result_file = output_path / f"{img_file.stem}_result.json"
                with open(result_file, "w") as f:
                    if isinstance(result, DeathCertificateSchema):
                        f.write(result.model_dump_json(indent=2))
                    else:
                        json.dump(result, f, indent=2)
                
                results.append(result)
        
        # Log summary
        summary = self.accuracy_tracker.get_summary()
        with open(output_path / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)
            
        return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Death Certificate extractor")
    parser.add_argument("--input", help="Path to a single image")
    parser.add_argument("--dir", help="Path to a directory of images")
    parser.add_argument("--output", default="data/outputs", help="Output directory")
    
    args = parser.parse_args()
    config.validate() # Ensure env vars are set
    extractor = DeathCertificateExtractor()
    
    if args.input:
        res = extractor.process_document(args.input)
        print(res)
    elif args.dir:
        extractor.batch_process(args.dir, args.output)
