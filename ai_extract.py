import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pypdf import PdfReader
import csv

load_dotenv()
client = Anthropic()

def extract_invoice_data(pdf_path):
    """Reads one PDF invoice and returns extracted data as a dictionary."""
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    invoice_text = page.extract_text()

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
- amount_due

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


def save_to_csv(data, csv_path="extracted_invoices.csv"):
    """Appends one row of extracted data to the CSV file."""
    fieldnames = ["invoice_number", "date", "due_date", "vendor", "amount_due"]
    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(csv_path) == 0:
            writer.writeheader()
        writer.writerow(data)


# Process every PDF in the "invoices" folder
invoice_folder = "invoices"

for filename in os.listdir(invoice_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(invoice_folder, filename)
        print(f"Processing {filename}...")
        try:
            data = extract_invoice_data(pdf_path)
            save_to_csv(data)
            print(f"  -> Saved: {data}")
        except Exception as e:
            print(f"  -> Failed to process {filename}: {e}")