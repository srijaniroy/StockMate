import sqlite3

class Inventory:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create tables for Product, Supplier, and Orders if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER,
                price REAL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                contact TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                supplier_id INTEGER,
                status TEXT,
                FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY(order_id) REFERENCES orders(order_id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')

        self.conn.commit()

    def get_valid_integer(self):
        while True:
            try:
                value = int(input())
                if value < 0:
                    print("Please enter a non-negative integer: ")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a valid integer: ")

    def get_valid_double(self):
        while True:
            try:
                value = float(input())
                if value < 0:
                    print("Please enter a non-negative number: ")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a valid number: ")

    def add_product(self):
        print("Enter product ID: ", end="")
        id = self.get_valid_integer()

        print("Enter product name: ", end="")
        name = input()

        print("Enter product quantity: ", end="")
        quantity = self.get_valid_integer()

        print("Enter product price: ", end="")
        price = self.get_valid_double()

        self.cursor.execute('''
            INSERT INTO products (id, name, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (id, name, quantity, price))

        self.conn.commit()
        print("Product added successfully!")

    def add_supplier(self):
        print("Enter supplier ID: ", end="")
        id = self.get_valid_integer()

        print("Enter supplier name: ", end="")
        name = input()

        print("Enter supplier contact (10 digits): ", end="")
        contact = input()

        self.cursor.execute('''
            INSERT INTO suppliers (id, name, contact)
            VALUES (?, ?, ?)
        ''', (id, name, contact))

        self.conn.commit()
        print("Supplier added successfully!")

    def place_order(self):
        print("Enter supplier ID for the order: ", end="")
        supplier_id = self.get_valid_integer()

        print("Enter order ID: ", end="")
        order_id = self.get_valid_integer()

        self.cursor.execute('''
            INSERT INTO orders (order_id, supplier_id, status)
            VALUES (?, ?, ?)
        ''', (order_id, supplier_id, 'Pending'))

        self.conn.commit()

        while True:
            print("Enter product ID to order: ", end="")
            product_id = self.get_valid_integer()

            print("Enter quantity to order: ", end="")
            quantity = self.get_valid_integer()

            # Check if the product exists and update inventory
            self.cursor.execute('''
                SELECT * FROM products WHERE id = ?
            ''', (product_id,))
            product = self.cursor.fetchone()

            if product:
                available_quantity = product[2]
                if available_quantity >= quantity:
                    new_quantity = available_quantity - quantity
                    self.cursor.execute('''
                        UPDATE products SET quantity = ? WHERE id = ?
                    ''', (new_quantity, product_id))

                    # Add to order items
                    self.cursor.execute('''
                        INSERT INTO order_items (order_id, product_id, quantity)
                        VALUES (?, ?, ?)
                    ''', (order_id, product_id, quantity))

                    self.conn.commit()
                    print("Product added to the order.")
                else:
                    print("Insufficient quantity in stock!")
            else:
                print("Product not found!")

            choice = input("Do you want to add more products to the order? (y/n): ").strip()
            if choice.lower() != 'y':
                break

        print("Order placed successfully!")

    def complete_order(self):
        print("Enter order ID to mark as completed: ", end="")
        order_id = self.get_valid_integer()

        self.cursor.execute('''
            UPDATE orders SET status = ? WHERE order_id = ?
        ''', ('Completed', order_id))

        self.conn.commit()
        print("Order marked as completed successfully!")

    def remove_product(self):
        print("Enter product ID to remove: ", end="")
        id = self.get_valid_integer()

        self.cursor.execute('''
            DELETE FROM products WHERE id = ?
        ''', (id,))
        self.conn.commit()

        print("Product removed successfully!")

    def display_inventory(self):
        self.cursor.execute('''
            SELECT * FROM products
        ''')
        products = self.cursor.fetchall()

        if products:
            print("\nCurrent Inventory:")
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: Rs. {product[3]:.2f}")
        else:
            print("Inventory is empty.")

    def display_orders(self, status='Pending'):
        self.cursor.execute('''
            SELECT * FROM orders WHERE status = ?
        ''', (status,))
        orders = self.cursor.fetchall()

        if orders:
            for order in orders:
                print(f"\n--- Order ID: {order[0]} ---")
                print(f"Supplier ID: {order[1]}, Status: {order[2]}")
                self.cursor.execute('''
                    SELECT products.id, products.name, order_items.quantity
                    FROM order_items
                    JOIN products ON products.id = order_items.product_id
                    WHERE order_items.order_id = ?
                ''', (order[0],))
                items = self.cursor.fetchall()
                for item in items:
                    print(f"Product ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
        else:
            print(f"No {status} orders.")

def main():
    inventory = Inventory()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Place Order")
        print("4. Complete Order")
        print("5. Display Inventory")
        print("6. Display Pending Orders")
        print("7. Display Completed Orders")
        print("8. Exit")
        print("Enter your choice: ", end="")

        choice = inventory.get_valid_integer()

        if choice == 1:
            inventory.add_product()
        elif choice == 2:
            inventory.remove_product()
        elif choice == 3:
            inventory.place_order()
        elif choice == 4:
            inventory.complete_order()
        elif choice == 5:
            inventory.display_inventory()
        elif choice == 6:
            inventory.display_orders('Pending')
        elif choice == 7:
            inventory.display_orders('Completed')
        elif choice == 8:
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
