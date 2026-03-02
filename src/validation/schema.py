from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import date

class DeathCertificateSchema(BaseModel):
    # Personal Information
    first_name: str = Field(..., description="Legal first name of the deceased")
    last_name: str = Field(..., description="Legal last name of the deceased")
    date_of_birth: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format")
    date_of_death: date = Field(..., description="Date of death in YYYY-MM-DD format")
    gender: str = Field(..., description="Gender of the deceased")
    
    # Place and Cause
    place_of_death: str = Field(..., description="City, County, or State where death occurred")
    cause_of_death: List[str] = Field(default_factory=list, description="List of causes contributing to death")
    
    # Identification
    ssn_last_4: Optional[str] = Field(None, pattern=r"^\d{4}$", description="Last 4 digits of SSN")
    certificate_number: Optional[str] = Field(None, description="Official certificate or registration number")
    
    # Metadata for Confidence
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)
    extraction_notes: Optional[str] = Field(None, description="Notes on the extraction process or issues")

    @field_validator("date_of_death")
    @classmethod
    def validate_dates(cls, v, info):
        """Cross-field validation: DOB must be before DOD."""
        dob = info.data.get("date_of_birth")
        if dob and v and v < dob:
            raise ValueError("Date of death cannot be before date of birth")
        return v
