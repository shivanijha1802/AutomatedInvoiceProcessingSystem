import os
import re
import pdfplumber


# === Function to extract invoice fields using Regex ===
def extract_invoice_fields(text):
    invoice_num = re.search(r"Invoice\s*(Number)?[:\-]?\s*([\w\-]+)", text, re.IGNORECASE)

    date_patterns = [
        r"(?:Date|Invoice Date|Dated)[:\-]?\s*([\d]{2}/[\d]{2}/[\d]{4})",   
        r"(?:Date|Invoice Date|Dated)[:\-]?\s*([\d]{2}-[\d]{2}-[\d]{4})",   
        r"(?:Date|Invoice Date|Dated)[:\-]?\s*([\d]{4}-[\d]{2}-[\d]{2})",
    ]
    date  = None
    for pattern in date_patterns:
        match  = re.search(pattern, text, re.IGNORECASE)
        if match:
            date = match.group(1)
            break

    amount = re.search(r"Total\s*Amount[:\-]?\s*₹?\s*([\d,]+\.\d{2})", text, re.IGNORECASE)
    vendor = re.search(r"Vendor[:\-]?\s*(.+)", text, re.IGNORECASE)

    return{
        "Invoice Number": invoice_num.group(2) if invoice_num else "Not Found",
        "Date": date if date else "Not Found",
        "Amount": amount.group(1) if amount else "Not Found",
        "Vendor": vendor.group(1).strip() if vendor else "Not Found"
    }


# === Function to read all pdf in folder and extract the data ===
def process_invoices(folder_path):
    invoice_data = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)

            try:
                with pdfplumber.open(file_path) as pdf:
                    text = ''
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + '\n'

                    fields = extract_invoice_fields(text)
                    fields['Filename'] = file
                    invoice_data.append(fields)
                    
            except Exception as e:
                print(f"[!] Error reading {file}: {e}")

    return invoice_data