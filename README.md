# Death Certificate Structured Extractor

A production-grade pipeline for extracting structured JSON data from death certificate images using OCR and LLMs (GPT-4o/Claude).

## 🏗 System Architecture

The system follows a modular pipeline:
1.  **OCR Pipeline**: Image preprocessing (rotation, contrast, denoising) followed by text extraction using either Tesseract or Vision LLMs.
2.  **LLM Integration**: Structured extraction into JSON using Pydantic models. Supports GPT-4o and Claude 3.5.
3.  **Validation Engine**: Field-level rules (regex, logical consistency) and confidence scoring.
4.  **Reporting**: Structured logging, token usage tracking, and cost estimation.

## 🚀 Setup and Run

### Prerequisites
- Python 3.9+
- Tesseract OCR (optional, if using Tesseract engine)
- OpenAI or Anthropic API Key

### Installation
```bash
git clone <repo-url>
cd death-certificate-extractor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Usage
```bash
# Process a single image
python src/main.py --input data/samples/cert_1.jpg

# Batch process a directory
python src/main.py --dir data/samples/
```

## 📈 Accuracy Strategy
- **Few-shot Prompting**: Dynamic selection of examples based on document layout.
- **Cross-field Validation**: DOB < DOD checks, numeric ID validation.
- **Confidence Scoring**: LLM-driven confidence + rule-based heuristic.
- **Human-in-the-Loop**: Flagging documents for manual review if confidence < threshold.

## 💰 Cost and Latency
- **Cost**: Tracked per document based on token usage and current API pricing.
- **Latency**: Parallelized batch processing for high throughput.

## 🛠 CI/CD
Automated testing and linting via GitHub Actions.
