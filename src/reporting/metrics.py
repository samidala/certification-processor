import logging
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from src.utils.config import config
import json

class MetricsLogger:
    def __init__(self, log_dir: str = "data/outputs/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_file = self.log_dir / "metrics.jsonl"
        self.debug_file = self.log_dir / "debug.jsonl"
        self.logger = logging.getLogger("MetricsLogger")

    def log_extraction(self, 
                       doc_id: str, 
                       tokens: int, 
                       cost: float, 
                       latency: float, 
                       confidence: float,
                       status: str = "success",
                       error: Optional[str] = None):
        """Logs structured metrics for each extraction."""
        metric = {
            "timestamp": time.time(),
            "doc_id": doc_id,
            "tokens": tokens,
            "cost": cost,
            "latency": latency,
            "confidence": confidence,
            "status": status,
            "error": error
        }
        
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(metric) + "\n")
        
    def log_debug(self, doc_id: str, prompt: str, response: str):
        """Logs raw prompt and response for debugging."""
        debug_entry = {
            "timestamp": time.time(),
            "doc_id": doc_id,
            "prompt": prompt,
            "response": response
        }
        with open(self.debug_file, "a") as f:
            f.write(json.dumps(debug_entry) + "\n")

class AccuracyTracker:
    def __init__(self):
        self.total_docs = 0
        self.tp = 0 # True Positives (Valid & High Confidence)
        self.fp = 0 # False Positives (Should have been flagged but wasn't - hard to track without ground truth, so we use proxy)
        self.fn = 0 # False Negatives (Flagged but was actually valid)
        self.field_failures = {} # Track which fields fail most often

    def update(self, confidence: float, is_valid: bool, issues: Optional[List[str]] = None):
        self.total_docs += 1
        if is_valid:
            self.tp += 1
        else:
            self.fn += 1
            if issues:
                for issue in issues:
                    # Simple heuristic: extract field name from issue message
                    # e.g. "date_of_death cannot be before date_of_birth"
                    field = issue.split()[0]
                    self.field_failures[field] = self.field_failures.get(field, 0) + 1

    def get_summary(self) -> Dict[str, Any]:
        precision = self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0
        recall = self.tp / (self.total_docs) if self.total_docs > 0 else 0
        
        return {
            "total_documents": self.total_docs,
            "accuracy": self.tp / self.total_docs if self.total_docs > 0 else 0,
            "precision": precision,
            "recall": recall,
            "field_failure_rates": self.field_failures,
            "failure_rate": (self.total_docs - self.tp) / self.total_docs if self.total_docs > 0 else 0
        }
