import tkinter as tk
from tkinter import ttk


class InventoryApp:

    def __init__(self, master):

        self.master = master

        self.master.title('Inventory Management System')

        self.master.geometry('500x400')

        self.inventory = {}

        self.create_widgets()



    def create_widgets(self):

        style = ttk.Style()
        style.configure("TFrame", background="#ececec")
        style.configure("TButton", background="#4CAF50", foreground="black")

        # Create the UI elements

        ttk.Label(self.master, text='Product Name:').grid(row=0, column=0, padx=10, pady=10)

        self.product_entry = ttk.Entry(self.master)

        self.product_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.master, text='Quantity:').grid(row=1, column=0, padx=10, pady=10)

        self.quantity_entry = ttk.Entry(self.master)

        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.master, text='Price:').grid(row=2, column=0, padx=10, pady=10)

        self.price_entry = ttk.Entry(self.master)

        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.master, text='Add Product', command=self.add_product)

        self.add_button.grid(row=3, column=0, padx=10, pady=10)

        self.remove_button = ttk.Button(self.master, text='Remove Product', command=self.remove_product)

        self.remove_button.grid(row=3, column=1, padx=10, pady=10)

        self.update_button = ttk.Button(self.master, text='Update Product', command=self.update_product)

        self.update_button.grid(row=4, column=0, padx=10, pady=10)

        self.view_button = ttk.Button(self.master, text='View Inventory', command=self.view_inventory)

        self.view_button.grid(row=4, column=1, padx=10, pady=10)

        self.inventory_text = tk.Text(self.master, height=10, width=50)

        self.inventory_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)



    def add_product(self):

        name = self.product_entry.get()

        quantity = int(self.quantity_entry.get())

        price = float(self.price_entry.get())

        if name in self.inventory:

            self.inventory[name]['quantity'] += quantity

            self.inventory[name]['price'] = price

        else:

            self.inventory[name] = {'quantity': quantity, 'price': price}

        self.product_entry.delete(0, 'end')



    def remove_product(self):

        name = self.product_entry.get()

        if name in self.inventory:

            del self.inventory[name]

        self.product_entry.delete(0, 'end')



    def update_product(self):

        name = self.product_entry.get()

        quantity = int(self.quantity_entry.get())

        price = float(self.price_entry.get())

        if name in self.inventory:

            self.inventory[name]['quantity'] = quantity

            self.inventory[name]['price'] = price

        self.product_entry.delete(0, 'end')



    def view_inventory(self):

        self.inventory_text.delete('1.0', 'end')

        for name, data in self.inventory.items():

            self.inventory_text.insert('end', f'{name}: {data["quantity"]} ({data["price"]}$)\n')



if __name__ == '__main__':

    root = tk.Tk()

    app = InventoryApp(root)

    root.mainloop()


