import pytest
from src.validation.schema import DeathCertificateSchema
from datetime import date

def test_schema_validation():
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "date_of_death": "2023-01-01",
        "gender": "Female",
        "place_of_death": "New York",
        "cause_of_death": ["Heart Attack"],
        "confidence_score": 0.95
    }
    schema = DeathCertificateSchema(**data)
    assert schema.first_name == "Jane"

def test_date_validation_failure():
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_birth": "2024-01-01",
        "date_of_death": "2023-01-01", # Invalid: death before birth
        "gender": "Female",
        "place_of_death": "New York",
        "cause_of_death": ["Heart Attack"],
        "confidence_score": 0.95
    }
    with pytest.raises(ValueError):
        DeathCertificateSchema(**data)

def test_ssn_validation():
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_death": "2023-01-01",
        "gender": "Female",
        "place_of_death": "New York",
        "ssn_last_4": "12345", # Invalid: more than 4 digits
        "confidence_score": 0.95
    }
    with pytest.raises(ValueError):
        DeathCertificateSchema(**data)
