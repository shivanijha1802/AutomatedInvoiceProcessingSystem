import imaplib
import email
from email.header import decode_header
import os
import io
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = "imap.gmail.com"
SAVE_FOLDER = "downloaded_invoices"

# === Check if PDF contains invoice keywords ===
def is_invoice_pdf(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
        keywords = ["invoice number", "invoice no", "date", "total amount"]
        return any(keyword in text.lower() for keyword in keywords)

# === Extract and save invoice PDFs from email ===
def get_invoices_from_email():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    # Connect to IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    
    if not email_ids:
        print("No unread emails found.")
        return

    invoice_count = 0

    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["Subject"]
        decoded_subject, encoding = decode_header(subject)[0]
        if isinstance(decoded_subject, bytes):
            decoded_subject = decoded_subject.decode(encoding or "utf-8", errors="ignore")
        
        if "invoice" not in decoded_subject.lower():
            continue

        has_invoice = False

        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename and filename.lower().endswith(".pdf") and "invoice" in filename.lower():
                    pdf_data = part.get_payload(decode=True)
                    
                    if is_invoice_pdf(pdf_data):
                        filepath = os.path.join(SAVE_FOLDER, filename)
                        with open(filepath, "wb") as f:
                            f.write(pdf_data)
                        print(f"[✓] Invoice saved: {filename}")
                        invoice_count += 1
                        has_invoice = True
                    else:
                        print(f"[✗] Skipped: Not a valid invoice - {filename}")

        if has_invoice:
            mail.store(email_id, '+FLAGS', '\\Seen')
        else:
            print(f"[✗] No invoice PDF found in: '{decoded_subject}'")

    mail.logout()
    print(f"\n[✓] Done: {invoice_count} invoice(s) saved to '{SAVE_FOLDER}'")
