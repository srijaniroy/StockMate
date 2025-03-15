import sqlite3
import re

class Product:
    def __init__(self, _id, name, quantity, price):
        self.id = _id
        self.name = name
        self.quantity = quantity
        self.price = price

    def display_product(self):
        print(f"ID: {self.id}, Name: {self.name}, Quantity: {self.quantity}, Price: Rs. {self.price}")

class Supplier:
    def __init__(self, _id, name, contact):
        self.id = _id
        self.name = name
        self.contact = contact

    def display_supplier(self):
        print(f"Supplier ID: {self.id}, Name: {self.name}, Contact: {self.contact}")

class Order:
    def __init__(self, _order_id, supplier, products_ordered):
        self.order_id = _order_id
        self.supplier = supplier
        self.products_ordered = products_ordered
        self.status = "Pending"

    def calculate_total(self):
        total = 0.0
        for product in self.products_ordered:
            total += product.price * product.quantity
        return total

    def display_order(self):
        print(f"\n--- Order ID: {self.order_id} ---")
        self.supplier.display_supplier()
        print(f"Status: {self.status}")
        print("Products in this order:")
        for product in self.products_ordered:
            product.display_product()
        print(f"Total Amount: Rs. {self.calculate_total()}")

class Inventory:
    def __init__(self):
        self.connection = sqlite3.connect('inventory.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )''')

        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        )''')

        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            supplier_id INTEGER,
            status TEXT,
            FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
        )''')

        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS order_items (
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )''')

    def get_valid_integer(self, prompt):
        while True:
            try:
                value = int(input(prompt))
                if value >= 0:
                    return value
                else:
                    print("Please enter a non-negative integer.")
            except ValueError:
                print("Invalid input. Please enter a non-negative integer:")

    def get_valid_double(self, prompt):
        while True:
            try:
                value = float(input(prompt))
                if value >= 0.0:
                    return value
                else:
                    print("Please enter a non-negative number:")
            except ValueError:
                print("Invalid input. Please enter a non-negative number:")

    def is_id_unique(self, _id, table):
        self.cursor.execute(f"SELECT 1 FROM {table} WHERE id = ?", (_id,))
        return not self.cursor.fetchone()

    def add_product(self):
        _id = int(input("Enter the unique Product ID: "))
        while not self.is_id_unique(_id, 'products'):
            print("Product ID already exists. Please enter a unique ID: ")
            _id = int(input())

        name = input("Enter the product name: ")
        quantity = self.get_valid_integer("Enter the product quantity: ")
        price = self.get_valid_double("Enter the product price per unit: Rs. ")

        self.cursor.execute("INSERT INTO products (id, name, quantity, price) VALUES (?, ?, ?, ?)",
                            (_id, name, quantity, price))
        self.connection.commit()
        print("Product added successfully!")

    def remove_product(self):
        _id = int(input("Enter the Product ID to remove: "))
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (_id,))
        product_data = self.cursor.fetchone()

        if product_data:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (_id,))
            self.connection.commit()
            print(f"Product with ID {_id} removed successfully!")
        else:
            print("Product not found!")

    def update_product(self):
        _id = int(input("Enter the Product ID to update: "))
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (_id,))
        product_data = self.cursor.fetchone()

        if product_data:
            print("Current product details: ")
            Product(product_data[0], product_data[1], product_data[2], product_data[3]).display_product()

            name = input("Enter the new product name: ")
            quantity = self.get_valid_integer("Enter the new product quantity: ")
            price = self.get_valid_double("Enter the new product price: Rs. ")

            self.cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?",
                                (name, quantity, price, _id))
            self.connection.commit()
            print("Product details updated successfully!")
        else:
            print("Product not found!")

    def add_supplier(self):
        _id = int(input("Enter the unique Supplier ID: "))
        while not self.is_id_unique(_id, 'suppliers'):
            print("Supplier ID already exists. Please enter a unique ID: ")
            _id = int(input())

        name = input("Enter the supplier's name: ")
        contact = input("Enter the supplier's contact (10 digits): ")
        while not re.match(r"^\d{10}$", contact):
            print("Invalid contact number. Please enter exactly 10 digits.")
            contact = input("Enter supplier contact (10 digits): ")

        self.cursor.execute("INSERT INTO suppliers (id, name, contact) VALUES (?, ?, ?)", 
                            (_id, name, contact))
        self.connection.commit()
        print("Supplier added successfully!")

    def remove_supplier(self):
        _id = int(input("Enter the Supplier ID to remove: "))
        self.cursor.execute("SELECT * FROM suppliers WHERE id = ?", (_id,))
        supplier_data = self.cursor.fetchone()

        if supplier_data:
            self.cursor.execute("DELETE FROM suppliers WHERE id = ?", (_id,))
            self.connection.commit()
            print(f"Supplier with ID {_id} removed successfully!")
        else:
            print("Supplier not found!")

    def update_supplier(self):
        _id = int(input("Enter the Supplier ID to update: "))
        self.cursor.execute("SELECT * FROM suppliers WHERE id = ?", (_id,))
        supplier_data = self.cursor.fetchone()

        if supplier_data:
            print("Current supplier details: ")
            Supplier(supplier_data[0], supplier_data[1], supplier_data[2]).display_supplier()

            name = input("Enter the new supplier name: ")
            contact = input("Enter the new supplier contact: ")
            while not re.match(r"^\d{10}$", contact):
                print("Invalid contact number. Please enter exactly 10 digits.")
                contact = input("Enter supplier contact (10 digits): ")

            self.cursor.execute("UPDATE suppliers SET name = ?, contact = ? WHERE id = ?",
                                (name, contact, _id))
            self.connection.commit()
            print("Supplier details updated successfully!")
        else:
            print("Supplier not found!")

    def place_order(self):
        supplier_id = int(input("Enter the Supplier ID for this order: "))
        self.cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        supplier_data = self.cursor.fetchone()

        if not supplier_data:
            print("Supplier not found!")
            return

        order_id = int(input("Enter a unique Order ID: "))
        self.cursor.execute("INSERT INTO orders (order_id, supplier_id, status) VALUES (?, ?, ?)", 
                            (order_id, supplier_id, "Pending"))
        self.connection.commit()

        order_products = []
        while True:
            product_id = int(input("Enter the Product ID to order: "))
            self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product_data = self.cursor.fetchone()

            if not product_data:
                print("Product not found!")
                continue

            quantity = self.get_valid_integer("Enter the quantity to order: ")

            if product_data[2] >= quantity:
                self.cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", 
                                    (quantity, product_id))
                self.cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", 
                                    (order_id, product_id, quantity))
                self.connection.commit()
                order_products.append(Product(product_data[0], product_data[1], quantity, product_data[3]))
                print("Product added to the order.")
            else:
                print("Insufficient quantity in stock!")

            choice = input("Do you want to add more products to the order? (y/n): ").lower()
            if choice != 'y':
                break

        order = Order(order_id, Supplier(supplier_data[0], supplier_data[1], supplier_data[2]), order_products)
        order.display_order()

    def complete_order(self):
        order_id = int(input("Enter the Order ID to mark as completed: "))
        self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order_data = self.cursor.fetchone()

        if order_data:
            if order_data[2] == "Pending":
                self.cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", ("Completed", order_id))
                self.connection.commit()
                print("Order marked as completed successfully!")
            else:
                print("Order is already completed.")
        else:
            print(f"Order with ID {order_id} not found.")

    def display_inventory(self):
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()

        if not products:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory:")
        for product in products:
            Product(product[0], product[1], product[2], product[3]).display_product()

    def display_suppliers(self):
        self.cursor.execute("SELECT * FROM suppliers")
        suppliers = self.cursor.fetchall()

        if not suppliers:
            print("No suppliers found.")
            return

        print("\n--- All Suppliers ---")
        for supplier in suppliers:
            Supplier(supplier[0], supplier[1], supplier[2]).display_supplier()

    def display_pending_orders(self):
        self.cursor.execute("SELECT * FROM orders WHERE status = 'Pending'")
        orders = self.cursor.fetchall()

        if not orders:
            print("No pending orders.")
            return

        print("\n--- Pending Orders ---")
        for order in orders:
            self.cursor.execute("SELECT * FROM suppliers WHERE id = ?", (order[1],))
            supplier_data = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order[0],))
            order_items = self.cursor.fetchall()

            order_products = []
            for item in order_items:
                self.cursor.execute("SELECT * FROM products WHERE id = ?", (item[1],))
                product_data = self.cursor.fetchone()
                order_products.append(Product(product_data[0], product_data[1], item[2], product_data[3]))

            Order(order[0], Supplier(supplier_data[0], supplier_data[1], supplier_data[2]), order_products).display_order()

    def display_completed_orders(self):
        self.cursor.execute("SELECT * FROM orders WHERE status = 'Completed'")
        orders = self.cursor.fetchall()

        if not orders:
            print("No completed orders.")
            return

        print("\n--- Completed Orders ---")
        for order in orders:
            self.cursor.execute("SELECT * FROM suppliers WHERE id = ?", (order[1],))
            supplier_data = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order[0],))
            order_items = self.cursor.fetchall()

            order_products = []
            for item in order_items:
                self.cursor.execute("SELECT * FROM products WHERE id = ?", (item[1],))
                product_data = self.cursor.fetchone()
                order_products.append(Product(product_data[0], product_data[1], item[2], product_data[3]))

            Order(order[0], Supplier(supplier_data[0], supplier_data[1], supplier_data[2]), order_products).display_order()

def main():
    inventory = Inventory()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Product Details")
        print("4. Display Inventory")
        print("5. Add Supplier")
        print("6. Remove Supplier")
        print("7. Update Supplier Details")
        print("8. Display Suppliers")
        print("9. Place Order")
        print("10. Complete Order")
        print("11. Display Pending Orders")
        print("12. Display Completed Orders")
        print("13. Exit")

        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 13.")
            continue

        if choice == 1:
            inventory.add_product()
        elif choice == 2:
            inventory.remove_product()
        elif choice == 3:
            inventory.update_product()
        elif choice == 4:
            inventory.display_inventory()
        elif choice == 5:
            inventory.add_supplier()
        elif choice == 6:
            inventory.remove_supplier()
        elif choice == 7:
            inventory.update_supplier()
        elif choice == 8:
            inventory.display_suppliers()
        elif choice == 9:
            inventory.place_order()
        elif choice == 10:
            inventory.complete_order()
        elif choice == 11:
            inventory.display_pending_orders()
        elif choice == 12:
            inventory.display_completed_orders()
        elif choice == 13:
            print("Exiting program...")
            inventory.connection.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()