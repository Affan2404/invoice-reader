# Invoice Reader

An AI-powered tool that extracts structured data (invoice number, date, vendor, amount due, etc.) from PDF invoices using Claude's API — built as the first step toward an AI automation toolkit for small businesses.

## What it does

1. Reads a PDF invoice
2. Extracts raw text from the PDF
3. Sends the text to Claude with instructions to pull out key fields
4. Cleans up Claude's response (handles markdown-wrapped JSON)
5. Saves the structured result to a CSV file for easy use in spreadsheets or accounting tools

## Tech stack

- Python
- [pypdf](https://pypi.org/project/pypdf/) — PDF text extraction
- [Anthropic API](https://docs.anthropic.com/) (Claude) — AI-powered field extraction
- python-dotenv — secure API key management

## Setup

1. Clone this repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/Scripts/activate` (Windows Git Bash)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Anthropic API key:
ANTHROPIC_API_KEY=your_key_here
6. Run: `python ai_extract.py`

## Status

Working end-to-end — processes all PDF invoices in the `invoices/` folder, extracts key fields via Claude, and logs results to `extracted_invoices.csv`. Includes error handling so one bad file doesn't stop the batch.

## Potential future improvements

**Near-term**
- Multi-page invoice support (currently only reads page 1 of each PDF)
- OCR support for scanned/photographed invoices (many real small-business invoices are phone photos, not clean digital PDFs)
- Duplicate detection (avoid logging the same invoice twice)
- Extract additional fields (tax, GST number, line items, currency)
- Log failed extractions to a separate error log

**Medium-term**
- Validation checks to flag likely-incorrect extractions for human review
- Support image file uploads directly (`.jpg`, `.png`), not just PDFs
- Export to formatted Excel instead of plain CSV

**Longer-term (post-launch)**
- Simple web interface for drag-and-drop upload
- Multi-user support with separate client data
- Hosted deployment for real-world client use