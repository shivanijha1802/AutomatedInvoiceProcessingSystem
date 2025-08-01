import pandas as pd
import sqlite3
from openpyxl import Workbook


# === Function to save invoice data into excel ===
def save_to_excel(data, filename="invoices.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"[+] Invoice data saved to Excel: {filename}")


# === Function to save invoice data into sqlite ===
def save_to_sqlite(data, db_name="invoices.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoice (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_num TEXT,
                        date TEXT, amount TEXT, vendor TEXT, filename TEXT UNIQUE
                    )
    ''')

    # Insert data with duplicate check
    for entry in data:
        try:
            cursor.execute('''INSERT INTO invoice (invoice_num, date, amount, vendor, filename)
                           VALUES (?, ?, ?, ?, ?)
            ''', (
                entry["Invoice Number"],
                entry["Date"],
                entry["Amount"],
                entry["Vendor"],
                entry["Filename"]
            ))
        except sqlite3.IntegrityError:
            print(f"[!] Duplicate found: {entry['Filename']}")

    conn.commit()
    conn.close()
    print(f"[+] Invoice data saved to database: {db_name}")