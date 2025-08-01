# Automated Invoice Processing System

This project automatically processes invoice PDFs received via email. It extracts invoice details using regular expressions and stores them in both Excel and SQLite database formats through a simple GUI.

## 📁 Folder Structure
```
Automated_Invoice_Processing_System/
│
├── app_gui.py
├── .env                      # Containg email and password
├── invoice_from_email.py
├── invoice_from_folder.py
├── data_storage.py
├── downloaded_invoices/      # Folder to save invoice PDFs
├── invoices.xlsx             # Excel output
├── invoices.db               # SQLite DB output
└── README.md
```

## 💻 Features
- Downloads unread email attachments with subject "invoice"
- Extracts invoice number, date, vendor, and amount using regex
- Saves extracted data to:
  - Excel file (`invoices.xlsx`)
  - SQLite database (`invoices.db`)
- GUI built with Tkinter

## ⚙️ Technologies Used
- Python 3
- pdfplumber
- re (regex)
- pandas
- openpyxl
- sqlite3
- imaplib + email
- tkinter

## ▶️ How to Run
1. Set up your Gmail credentials using environment variables.
2. Run `app_gui.py` to start the app.
3. Click "Download Invoices from Email" button in the GUI.

## 📞 Author
- Shivani | Python Intern | 2025
