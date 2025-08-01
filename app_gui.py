from data_storage import save_to_excel, save_to_sqlite
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from invoice_from_email import get_invoices_from_email
from invoice_from_folder import process_invoices


def invoice_processing():

    get_invoices_from_email()

    folder = "downloaded_invoices"
    
    invoice_data = process_invoices(folder)

    if invoice_data:
        save_to_excel(invoice_data)
        save_to_sqlite(invoice_data)
        messagebox.showinfo("Success", "Invoices precessed and saved.")
    else:
        messagebox.showwarning("No Data", "No PDF invoice found.")


def launch_app():
    root = tk.Tk()
    root.title("Automated Invoice Processing System")
    root.geometry("400x200")

    tk.Label(root, text="Automated Invoice Processor", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Download Invoices from Email", command=invoice_processing, font=("Arial", 12)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    launch_app()