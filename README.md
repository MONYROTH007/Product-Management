# Product-Management
Overview
The Product Manager is a simple inventory management application built using Python's Tkinter library for the graphical user interface (GUI) and SQLite for database management. This application allows users to manage products, including adding, updating, searching, and deleting products from an inventory.

Features
User Authentication: Secure login system using predefined username and password (admin/admin).
Product Management: Add, update, and delete products in the inventory.
Search & Filter: Search products by name or category and filter them by category.
Expiration Warning: Highlight products that are expired or nearing expiration within 7 days.
Category Management: Organize products into predefined categories like Fruits, Vegetables, Dairy, etc.
Password Change: Admin users can change their password securely.
Requirements
Python 3.x
Tkinter (usually comes with Python)
tkcalendar (for date picker)
sqlite3 (built-in with Python)
Database Schema
The application uses an SQLite database with two tables:

users: Stores user login credentials (username and password).
products: Stores product details such as name, quantity, expiration_date, category, type, and imported_from.
Setup & Usage
Initialize the Database: The setup_database() function initializes the database by creating the necessary tables if they don't exist.

Add Initial User: The add_initial_user() function adds a predefined user (admin/admin) for demonstration purposes.

Login Screen: The login screen is the first screen shown. The user must log in using valid credentials (admin/admin for the initial setup). Passwords can be changed by clicking the "Change Password" button.

Main Screen: After login, users are presented with the main screen where they can:

Add new products.
Update or delete existing products.
Search and filter products by name and category.
View products sorted by their expiration dates with color-coded warnings for expired or near-expiring products.
Product Details: The application allows users to input details such as:

Product Name
Quantity
Expiration Date
Category
Product Type
Imported From
Expiration dates are visually managed with color coding:

Red for expired products.
Yellow for products expiring in 7 days.
Code Explanation
Main Application (ProductManagerApp): Handles GUI elements, user authentication, product management, and database interaction.
Database Functions: Includes functions to set up the database, validate user credentials, and perform CRUD operations on products.
Search and Filter: Implements search functionality that allows users to filter products by name and category.

To Run
Simply run the script in a Python environment that supports Tkinter.
python product_manager.py
The application will launch the product manager GUI, where you can interact with it.

