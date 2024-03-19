from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
#from kivy.adapters.listadapter import RecycleDataAdapter
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
import sqlite3
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty


Builder.load_string('''
<InventoryManagement>:
    orientation: 'vertical'
    padding: 10

    BoxLayout:
        size_hint_y: None
        height: 30

        Label:
            text: 'Name'
            size_hint_x: 0.2

        Label:
            text: 'Quantity'
            size_hint_x: 0.4

        Label:
            text: 'Price'
            size_hint_x: 0.4

    BoxLayout:
        size_hint_y: None
        height: 30

        TextInput:
            id: name_input
            size_hint_x: 0.2

        TextInput:
            id: quantity_input
            size_hint_x: 0.4

        TextInput:
            id: price_input
            size_hint_x: 0.4

    BoxLayout:
        size_hint_y: None
        height: 30

        Button:
            text: 'Add Product'
            on_press: root.add_product()

        Button:
            text: 'Update Product'
            on_press: root.update_product()

        Button:
            text: 'Delete Product'
            on_press: root.delete_product()

    BoxLayout:
        size_hint_y: 0.8

        RecycleView:
            id: RV
            viewclass: 'Label'
            data: [{'text': key} for key in root.products_list] if root.products_list is not None else ['Empty']
            RecycleBoxLayout:
                default_size: None, 26
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

    BoxLayout:
        size_hint_y: None
        height: 30

        Label:
            id: message_label
            text: ''
            size_hint_x: 0.7

        Button:
            text: 'View Products'
            size_hint_x: 0.3
            on_press: root.view_product()
''')

class RV(RecycleDataViewBehavior, FocusBehavior, BoxLayout):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class InventoryManagement(BoxLayout):
    products_list = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create database and product table
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products 
                     (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price INTEGER)''')
        conn.commit()
        #products_list = ObjectProperty()
        self.view_db()

    def add_product(self):
        name_input = self.ids.name_input
        quantity_input = self.ids.quantity_input
        price_input = self.ids.price_input
        message_label = self.ids.message_label

        if not name_input.text or not quantity_input.text or not price_input.text:
            message_label.text = 'Please fill all fields'
        else:
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name_input.text, quantity_input.text, price_input.text))
            conn.commit()
            self.clear_entries()
            self.view_product()
            message_label.text = 'Product added successfully'

    def view_product(self):
        #products_list = self.ids.products_list
        message_label = self.ids.message_label

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        #products_list.item_strings = [f"{row[0]} | {row[1]} | {row[2]} | {row[3]}" for row in rows]
        self.view_db()
        message_label.text = ''

        #self.ids.data = [{'text': key} for key in products_list.item_strings]

        content = BoxLayout(orientation='vertical')

        product_description = Label(text=f"Product Description: {self.products_list[0]}", size_hint_y=None, height=30)
        content.add_widget(product_description)

        close_button = Button(text="Close", size_hint_y=None, height=30)
        content.add_widget(close_button)

        popup = Popup(title="Product Details", content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

        close_button.bind(on_press=popup.dismiss)

    def update_product(self):
        name_input = self.ids.name_input
        quantity_input = self.ids.quantity_input
        price_input = self.ids.price_input
        message_label = self.ids.message_label
        products_list = self.ids.products_list

        if not name_input.text or not quantity_input.text or not price_input.text:
            message_label.text = 'Please fill all fields'
        else:
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            #selected_product_id = int(products_list.adapter.selection[0].split('|')[0].strip())
            c.execute("UPDATE products SET name=?, quantity=?, price=? WHERE name = ?", (name_input.text, quantity_input.text, price_input.text, name_input.text))
            conn.commit()
            self.clear_entries()
            self.view_product()
            message_label.text = 'Product updated successfully'

    def delete_product(self):
        message_label = self.ids.message_label
        #products_list = self.ids.products_list
        name_input = self.ids.name_input

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        #selected_product_id = int(products_list.adapter.selection[0].split('|')[0].strip())
        c.execute("DELETE FROM products WHERE name=?", (name_input.text,))
        conn.commit()
        self.clear_entries()
        self.view_product()
        message_label.text = 'Product deleted successfully'

    def clear_entries(self):
        name_input = self.ids.name_input
        quantity_input = self.ids.quantity_input
        price_input = self.ids.price_input
        message_label = self.ids.message_label

        name_input.text = ''
        quantity_input.text = ''
        price_input.text = ''
        message_label.text = ''

    @property
    def prodcuts_list(self):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        self.products_list.append(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        #return [f"{row[0]} | {row[1]} | {row[2]} | {row[3]}" for row in rows]

    def view_db(self):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        for row in rows:
            self.products_list.append(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}") 

class InventoryManagementApp(App):
    def build(self):
        return InventoryManagement()

if __name__ == '__main__':
    InventoryManagementApp().run()