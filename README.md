# StockMate
A Python-based command-line inventory management system, based on OOP principles, that tracks products, suppliers, and orders with a SQL database backend.

## Features

- **Product Management**: Add, remove, update, and display product information, including ID, name, quantity, and price.
- **Supplier Management**: Add, remove, update, and display supplier details, including supplier ID, name, and contact information.
- **Order Management**: Create, update, and display orders, including placing orders for products, calculating totals, and marking orders as completed.
- **Data Validation**: Ensure data integrity with unique ID checks, non-negative quantity and price validation, and contact number validation.
- **Database Integration**: Store all data in an SQLite database for persistence and retrieval.


## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/srijaniroy/StockMate
   ```

2. Navigate to the project directory in your terminal or command prompt.

3. You can run the application directly from the command line by executing the following command:

   ```bash
   python3 main.py
   ```

4. The application will create and use an SQLite database (`inventory.db`) to store data. The database will be automatically created if it doesn't exist.

## Technologies Used

- **Python**: Core programming language for building the application logic.
- **SQLite**: Lightweight, serverless relational database to store products, suppliers, and order details.
- **Regular Expressions (Regex)**: Used for validating contact numbers and product details.
- **Object-Oriented Programming (OOP)**: Application built using classes to represent Products, Suppliers, Orders, and Inventory management.

## Database Schema

The database consists of the following tables:

1. **Products**: Stores information about products in the inventory.
   - Columns: `id`, `name`, `quantity`, `price`

2. **Suppliers**: Stores supplier information.
   - Columns: `id`, `name`, `contact`

3. **Orders**: Stores orders placed with suppliers.
   - Columns: `order_id`, `supplier_id`, `status`

4. **Order_Items**: Stores the details of products included in each order.
   - Columns: `order_id`, `product_id`, `quantity`


## Future Improvements

- **User Authentication**: Add an authentication system for users to log in and have different levels of access.
- **Web Interface**: Build a web-based interface using frameworks like Flask or Django for ease of use.
- **Reporting**: Implement detailed reporting and analytics features, such as inventory turnover, order histories, and supplier performance.
- **API Integration**: Develop an API to integrate with external systems or mobile applications.
- **Error Handling**: Add advanced error handling for edge cases such as database connection issues or invalid data.
