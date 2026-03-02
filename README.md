# Death Certificate Structured Extractor

A production-grade pipeline for extracting structured JSON data from death certificate images using OCR and LLMs (GPT-4o or Claude 3.5 Sonnet).

## 🏗 System Architecture

The system follows a modular pipeline designed for high accuracy and scalability:
1.  **OCR/Preprocessing Pipeline**: Image enhancement (contrast, denoising) to optimize vision LLM extraction.
2.  **LLM Integration Layer**: Supports OpenAI (GPT-4o) and Anthropic (Claude 3.5). Features versioned prompts and dynamic few-shot example loading.
3.  **Validation Engine**: Dual-layer validation (Pydantic schema constraints + logical cross-field rules like DOB < DOD).
4.  **Observability & Reporting**: Structured logging of extraction metrics, token usage, cost estimation, and granular accuracy tracking.

## 🚀 Setup and Run

### Prerequisites
- Python 3.9+
- OpenAI API Key (for GPT-4o)
- Anthropic API Key (for Claude 3.5)

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd death-certificate-extractor

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY)
```

### Usage

#### 1. Process a Single Image
```bash
python3 src/main.py --input data/samples/sample_1.jpg
```

#### 2. Batch Process a Directory
```bash
python3 src/main.py --dir data/samples/ --output data/outputs/
```

#### 3. Run Test Suite
```bash
python3 -m pytest tests/
```

## ⚙️ Configuration

Set these in your `.env` file:
- `DEFAULT_LLM_PROVIDER`: `openai` or `anthropic`
- `LLM_MODEL`: e.g., `gpt-4o` or `claude-3-5-sonnet-20240620`
- `CONFIDENCE_THRESHOLD`: Minimum score before flagging for human review (default: `0.85`)
- `ENABLE_RAW_LOGGING`: Set to `true` to log raw prompts and responses for debugging.

## 📈 Accuracy & Verification
- **Few-shot Prompting**: Managed via `config/examples/examples.yaml`.
- **Metrics Tracking**: Results are saved to `data/outputs/logs/metrics.jsonl` and summarized in `summary.json`.
- **Human-in-the-Loop**: Documents with confidence below the threshold are flagged in `data/outputs/` with reason codes.

## � Project Structure
- `src/main.py`: Main orchestrator.
- `src/llm/`: Providers (OpenAI, Anthropic) and Prompt Management.
- `src/validation/`: Pydantic schemas and business logic validation.
- `src/reporting/`: Accuracy and cost tracking.
- `config/`: Versioned prompts and few-shot examples.
- `tests/`: OCR, LLM (mocked), and Validation unit tests.
