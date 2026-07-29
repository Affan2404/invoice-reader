from pypdf import PdfReader

# Load the PDF file
reader = PdfReader("sample_invoice.pdf")
page = reader.pages[0]
text = page.extract_text()

# Split into lines
lines = text.split("\n")

# The exact labels we expect to find, based on looking at this invoice
known_labels = ["Invoice Number", "Date", "Due Date", "Bill To", "Amount Due"]

invoice_data = {}

for line in lines:
    for label in known_labels:
        if line.startswith(label):
            # Take everything after the label itself
            value = line[len(label):]
            # Remove a leading colon if there is one, then clean whitespace
            value = value.lstrip(":").strip()
            invoice_data[label] = value

print(invoice_data)