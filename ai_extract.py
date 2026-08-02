import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pypdf import PdfReader
import csv
import logging

# Configure logging: write errors to a file, with timestamps
logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

load_dotenv()
client = Anthropic()

def extract_invoice_data(pdf_path):
    """Reads one PDF invoice and returns extracted data as a dictionary."""
    reader = PdfReader(pdf_path)
    # Combine text from every page, not just the first
    invoice_text = ""
    for page in reader.pages:
        invoice_text += page.extract_text() + "\n"

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Extract the following fields from this invoice text and return ONLY a valid JSON object, nothing else:
- invoice_number
- date
- due_date
- vendor
- vendor_gst_number (the GST number, if present; use null if not found)
- amount_due
- line_items (a list of objects, each with "description", "quantity", "unit_price", and "total" — use an empty list if none found)

Invoice text:
{invoice_text}"""
            }
        ]
    )

    raw_text = response.content[0].text
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1)
        raw_text = raw_text.strip()

    return json.loads(raw_text)

def is_duplicate(invoice_number, csv_path="extracted_invoices.csv"):
    """Checks if an invoice number already exists in the CSV file."""
    if not os.path.exists(csv_path):
        return False

    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["invoice_number"] == invoice_number:
                return True

    return False

def format_line_items(line_items):
    """Converts a list of line item dictionaries into one readable text block."""
    if not line_items:
        return ""

    lines = []
    for item in line_items:
        line = f"{item.get('description', '')} (qty: {item.get('quantity', '')}, price: {item.get('unit_price', '')}, total: {item.get('total', '')})"
        lines.append(line)

    return " | ".join(lines)


def save_to_csv(data, csv_path="extracted_invoices.csv"):
    """Appends one row of extracted data to the CSV file."""
    fieldnames = ["invoice_number", "date", "due_date", "vendor", "vendor_gst_number", "amount_due", "line_items"]
    file_exists = os.path.exists(csv_path)

    # Make a copy of the data with line_items converted to a readable string
    row_data = data.copy()
    row_data["line_items"] = format_line_items(data.get("line_items", []))

    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(csv_path) == 0:
            writer.writeheader()
        writer.writerow(row_data)

# Process every PDF in the "invoices" folder
invoice_folder = "invoices"

for filename in os.listdir(invoice_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(invoice_folder, filename)
        print(f"Processing {filename}...")
        try:
            data = extract_invoice_data(pdf_path)

            if is_duplicate(data["invoice_number"]):
                print(f"  -> Skipped (already processed): {data['invoice_number']}")
            else:
                save_to_csv(data)
                print(f"  -> Saved: {data}")
        except Exception as e:
            error_message = f"Failed to process {filename}: {e}"
            print(f"  -> {error_message}")
            logging.error(error_message)