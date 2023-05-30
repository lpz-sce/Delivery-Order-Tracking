import csv
from datetime import date
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path

def add_order():
    customer_name = entry_name.get()
    container_num = entry_container.get()
    date_received = entry_date.get()
    year, month, day = map(int, date_received.split('-'))

    order_date = date(year, month, day)

    with open("orders.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Customer Name", "Container Number", "Date Received"])
        writer.writerow([customer_name, container_num, order_date])
    messagebox.showinfo("Success", "Order added successfully.")

def display_orders():
    orders = []
    with open("orders.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            orders.append(row)
    messagebox.showinfo("Orders", orders)

def download_file():
    documents_dir = Path.home() / "Documents"
    file_path = filedialog.asksaveasfilename(initialdir=documents_dir, defaultextension=".csv")
    if file_path:
        with open("orders.csv", "r") as source_file, open(file_path, "w", newline="") as destination_file:
            destination_file.write(source_file.read())
        messagebox.showinfo("Success", "File downloaded successfully.")

def count_orders_by_customer():
    customer_counts = {}
    current_date = date.today()
    
    with open("orders.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            order_date = date.fromisoformat(row[2])
            if order_date == current_date:
                customer = row[0]
                if customer in customer_counts:
                    customer_counts[customer] += 1
                else:
                    customer_counts[customer] = 1

    if customer_counts:
        count_text = "\n".join([f"{customer}: {count}" for customer, count in customer_counts.items()])
    else:
        count_text = "No delivery orders for today."
    
    messagebox.showinfo("Delivery Order Counts", count_text)

# Create the main window
window = tk.Tk()
window.title("Order Management")

# Configure window resizing
window.resizable(width=True, height=True)

# Create input fields and labels
label_name = tk.Label(window, text="Customer Name:")
label_name.pack()
entry_name = tk.Entry(window)
entry_name.pack()

label_container = tk.Label(window, text="Container Number:")
label_container.pack()
entry_container = tk.Entry(window)
entry_container.pack()

# Bind Ctrl+C and Ctrl+V to allow copy and paste for container number field
entry_container.bind("<Control-c>", lambda event: window.clipboard_append(entry_container.selection_get()))
entry_container.bind("<Control-v>", lambda event: entry_container.insert(tk.END, window.clipboard_get()))

label_date = tk.Label(window, text="Date (YYYY-MM-DD):")
label_date.pack()
entry_date = tk.Entry(window)
entry_date.pack()

# Create buttons
button_add = tk.Button(window, text="Add Order", command=add_order)
button_add.pack()

button_display = tk.Button(window, text="Display Orders", command=display_orders)
button_display.pack()

button_download = tk.Button(window, text="Download File", command=download_file)
button_download.pack()

button_count = tk.Button(window, text="Count Orders by Customer", command=count_orders_by_customer)
button_count.pack()

# Start the GUI event loop
window.mainloop()
