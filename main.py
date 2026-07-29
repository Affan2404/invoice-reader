# Open and read the sample invoice
with open("sample_invoice.txt", "r") as file:
    content = file.read()

# Split the content into separate lines
lines = content.split("\n")

# Create an empty dictionary to store extracted data
invoice_data = {}

# Loop through every line
for line in lines:
    # Skip any blank lines
    if line.strip() == "":
        continue

    # Split each line into label and value using the colon
    parts = line.split(":", 1)
    label = parts[0].strip()
    value = parts[1].strip()

    # Store it in the dictionary
    invoice_data[label] = value

# Print the final result
print(invoice_data)
print("The amount due is:", invoice_data["Amount Due"])