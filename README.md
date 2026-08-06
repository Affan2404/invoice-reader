# Invoice Reader

An AI-powered invoice data extractor. Drop in PDF or image invoices, and it automatically extracts structured data — invoice number, dates, vendor, GST number, line items, and amount due — using Claude, validates the results, flags anything that needs a human look, and exports clean CSV and Excel reports.

Built as a portfolio project exploring AI-assisted document processing for small businesses (CA firms, clinics, restaurants) in India.

## Features

- **Reads both PDFs and images** (`.jpg`, `.png`) — image invoices are read directly by Claude's vision capability, no separate OCR step needed
- **Structured extraction** — invoice number, date, due date, vendor, GST number, amount due, and itemized line items, returned as clean JSON
- **Data validation** — flags missing fields or malformed amounts, so problem invoices are easy to spot rather than silently wrong
- **Duplicate detection** — won't re-process or double-count an invoice it's already seen
- **Formatted Excel export** — colour-coded, auto-sized `.xlsx` report alongside the raw CSV
- **Run history tracking** — every run logs a summary (files processed, duplicates skipped, failures, review flags) to build an accuracy trend over time
- **Error handling** — a single bad file never crashes a batch; failures are logged and the rest continue
- **Tested** — automated pytest suite covering the core logic, run automatically on every push via GitHub Actions CI
- **Containerized** — fully Dockerized with `docker-compose` for consistent, portable execution

## Tech stack

Python · Anthropic Claude API · pypdf · openpyxl · pytest · GitHub Actions · Docker

## Project structure

```
invoice-reader/
├── invoices/                  # drop PDF/image invoices here
├── ai_extract.py               # main script
├── test_ai_extract.py          # pytest test suite
├── extracted_invoices.csv      # extracted invoice data
├── extracted_invoices.xlsx     # formatted Excel export
├── run_history.csv             # per-run summary stats
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/tests.yml # CI pipeline
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Affan2404/invoice-reader.git
cd invoice-reader
```

### 2. Add your API key

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

Get a key from the [Anthropic Console](https://console.anthropic.com).

### 3. Run it — pick one option

**Option A — Locally with Python**

```bash
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# or: source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python ai_extract.py
```

**Option B — With Docker (no local Python setup needed)**

```bash
docker-compose up --build
```

For subsequent runs, once already built:

```bash
docker-compose run --rm invoice-reader
```

## Usage

1. Drop invoice files (`.pdf`, `.jpg`, `.png`) into the `invoices/` folder
2. Run the script (see above)
3. Check `extracted_invoices.xlsx` for a formatted report — rows needing review are highlighted
4. Check `run_history.csv` for a summary of every run over time

## Running tests

```bash
pytest
```

Tests cover the core data-processing logic (JSON parsing, formatting, validation) and don't require an API key or internet connection. The same suite runs automatically on every push via GitHub Actions.

## Roadmap

This project is intentionally kept one step short of live deployment — it's a complete, tested, containerized tool, but not hosted or exposed as a public service. Possible future directions:

- Web interface for drag-and-drop upload
- Multi-user support
- Hosted deployment for real client use

## License

Personal portfolio project — not currently licensed for reuse.