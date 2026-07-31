# Invoice Reader

An AI-powered tool that extracts structured data (invoice number, date, vendor, amount due, etc.) from PDF invoices using Claude's API — built as the first step toward an AI automation toolkit for small businesses.

## What it does

1. Reads a PDF invoice
2. Extracts raw text from the PDF
3. Sends the text to Claude with instructions to pull out key fields
4. Saves the structured result to a CSV file for easy use in spreadsheets or accounting tools

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

🚧 In progress — currently extracts data from a single sample invoice. Next steps: support multiple invoices, handle scanned/image-based PDFs, build a simple interface.

## About

Part of a broader project building AI automation tools for small businesses in India (CA firms, clinics, restaurants).