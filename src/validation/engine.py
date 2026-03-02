from src.validation.schema import DeathCertificateSchema
from src.utils.config import config
import logging

logger = logging.getLogger(__name__)

class ValidationEngine:
    @staticmethod
    def validate(data: dict) -> tuple[bool, float, list]:
        """
        Validates the extracted data and returns (is_valid, final_confidence, issues).
        """
        issues = []
        try:
            # Pydantic validation handles regex and cross-field logic (DOB < DOD)
            validated_data = DeathCertificateSchema(**data)
            
            # Additional heuristic confidence scoring
            base_confidence = validated_data.confidence_score
            
            # Penalty for missing optional but important fields
            if not validated_data.ssn_last_4:
                base_confidence *= 0.95
            if not validated_data.gender:
                base_confidence *= 0.98
            if not validated_data.place_of_death:
                base_confidence *= 0.90 # High penalty for missing place
            
            is_valid = base_confidence >= config.CONFIDENCE_THRESHOLD
            
            if not is_valid:
                issues.append(f"Confidence {base_confidence:.2f} below threshold {config.CONFIDENCE_THRESHOLD}")
                
            return is_valid, base_confidence, issues
            
        except Exception as e:
            logger.error(f"Validation Error: {e}")
            return False, 0.0, [str(e)]

    @staticmethod
    def flag_for_human_review(doc_id: str, data: dict, issues: list):
        """Generates a failure report for human-in-the-loop."""
        report = {
            "document_id": doc_id,
            "status": "FLAGGED_FOR_REVIEW",
            "issues": issues,
            "raw_data": data
        }
        logger.warning(f"Document {doc_id} flagged for human review: {issues}")
        return report
