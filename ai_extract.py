import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pypdf import PdfReader

# Load the .env file so ANTHROPIC_API_KEY becomes available
load_dotenv()

# Create a client - this is your "connection" to Claude's API
client = Anthropic()

# Read the invoice text (reusing our PDF-reading logic from earlier)
reader = PdfReader("sample_invoice.pdf")
page = reader.pages[0]
invoice_text = page.extract_text()

# Send it to Claude with clear instructions
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

# Convert Claude's JSON-formatted text into an actual Python dictionary
raw_text = response.content[0].text

# Remove markdown code block formatting if present
if raw_text.startswith("```"):
    raw_text = raw_text.strip("`")       # remove backticks from both ends
    raw_text = raw_text.replace("json", "", 1)  # remove the "json" language tag
    raw_text = raw_text.strip()          # clean any leftover whitespace/newlines

extracted_data = json.loads(raw_text)

print(extracted_data)
print("Vendor:", extracted_data["vendor"])
print("Amount Due:", extracted_data["amount_due"])

import csv

# Save the extracted data to a CSV file
with open("extracted_invoices.csv", "a", newline="") as csvfile:
    fieldnames = ["invoice_number", "date", "due_date", "vendor", "amount_due"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # If the file is empty, write the header row first
    if csvfile.tell() == 0:
        writer.writeheader()

    writer.writerow(extracted_data)

print("Saved to extracted_invoices.csv")