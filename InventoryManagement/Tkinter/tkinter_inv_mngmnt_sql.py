from tkinter import *
import sqlite3

# create database and product table
conn = sqlite3.connect('inventory.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products 
             (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)''')
conn.commit()

# create tkinter window
window = Tk()
window.title("Inventory Management System")
window.geometry('500x400')

# define functions
def add_product():
    if not name_entry.get() or not quantity_entry.get() or not price_entry.get():
        message_label.config(text="Please fill all fields", fg="red")
    else:
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name_entry.get(), quantity_entry.get(), price_entry.get()))
        conn.commit()
        clear_entries()
        view_product()
        message_label.config(text="Product added successfully", fg="green")

def view_product():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    products_list.delete(0, END)
    for row in rows:
        products_list.insert(END, row)

def update_product():
    selected_product = products_list.get(ANCHOR)
    if not selected_product:
        message_label.config(text="Please select a product", fg="red")
        return
    new_quantity = int(quantity_entry.get())
    new_price = float(price_entry.get())
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("UPDATE products SET quantity=?, price=? WHERE id=?", (new_quantity, new_price, selected_product[0]))
    conn.commit()
    clear_entries()
    view_product()
    message_label.config(text="Product updated successfully", fg="green")

def delete_product():
    selected_product = products_list.get(ANCHOR)
    if not selected_product:
        message_label.config(text="Please select a product", fg="red")
        return
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (selected_product[0],))
    conn.commit()
    clear_entries()
    view_product()
    message_label.config(text="Product deleted successfully", fg="green")

def clear_entries():
    name_entry.delete(0, END)
    quantity_entry.delete(0, END)
    price_entry.delete(0, END)

# create labels
name_label = Label(window, text="Name", font=("Arial", 12))
name_label.grid(column=0, row=0, padx=10, pady=10)

quantity_label = Label(window, text="Quantity", font=("Arial", 12))
quantity_label.grid(column=1, row=0, padx=10, pady=10)

price_label = Label(window, text="Price", font=("Arial", 12))
price_label.grid(column=2, row=0, padx=10, pady=10)

# create entries
name_entry = Entry(window, font=("Arial", 12))
name_entry.grid(column=0, row=1, padx=10, pady=10)

quantity_entry = Entry(window, font=("Arial", 12))
quantity_entry.grid(column=1, row=1, padx=10, pady=10)

price_entry = Entry(window, font=("Arial", 12))
price_entry.grid(column=2, row=1, padx=10, pady=10)

# create buttons
add_button = Button(window, text="Add Product", font=("Arial", 12), command=add_product)
add_button.grid(column=0, row=2, padx=10, pady=10)

update_button = Button(window, text="Update Product", font=("Arial", 12), command=update_product)
update_button.grid(column=1, row=2, padx=10, pady=10)

delete_button = Button(window, text="Delete Product", font=("Arial", 12), command=delete_product)
delete_button.grid(column=2, row=2, padx=10, pady=10)

clear_button = Button(window, text="Clear Entries", font=("Arial", 12), command=clear_entries)
clear_button.grid(column=3, row=2, padx=10, pady=10)

view_button = Button(window, text="View Products", font=("Arial", 12), command=view_product)
view_button.grid(column=4, row=2, padx=10, pady=10)

# create products listbox
products_list = Listbox(window, font=("Arial", 12), width=70, height=10)
products_list.grid(column=0, row=3, columnspan=5, padx=10, pady=10)

# create message label
message_label = Label(window, font=("Arial", 12))
message_label.grid(column=0, row=4, columnspan=5, padx=10, pady=10)

# call view_product function to display initial data in products listbox
view_product()

# start the application
window.mainloop()

# close the database connection
conn.close()
