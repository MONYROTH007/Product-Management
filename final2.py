import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, date
import sqlite3
from tkcalendar import DateEntry
from datetime import timedelta

CATEGORIES = ['Fruits', 'Vegetables', 'Canned Goods', 'Dairy', 'Meat',
              'Fish & Seafood', 'Seasoning','Snacks','Candy',  'Bakery', 'Beverages',
              'Rice', 'Frozen Foods', 'Personal Care', 'Health care', 'Household',
              'Baby', 'Pet Care']
# Database setup
# Database setup with categories
def setup_database():
    conn = sqlite3.connect('product_manager.db')
    cursor = conn.cursor()

    # Check and fix the table schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            category TEXT,
            type TEXT,
            imported_from TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    # Fetch data from the database
    
# Check login credentials
def check_credentials(username, password):
    conn = sqlite3.connect('product_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Add initial user (for demonstration)
def add_initial_user():
    conn = sqlite3.connect('product_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin')")
    conn.commit()
    conn.close()

# GUI Application Class
class ProductManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Manager")
        self.root.geometry('800x600')
        self.login_screen()
    
    def change_password_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Change Password", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Current Password").pack()
        self.current_password_entry = tk.Entry(self.root, show="*")
        self.current_password_entry.pack()

        tk.Label(self.root, text="New Password").pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack()

        tk.Label(self.root, text="Confirm New Password").pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack()

        tk.Button(self.root, text="Submit", command=self.update_password).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_screen).pack()

    def update_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate the current password
        conn = sqlite3.connect('product_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", ('admin',))  # Replace 'admin' if multi-user is added
        stored_password = cursor.fetchone()[0]

        if current_password != stored_password:
            messagebox.showerror("Error", "Current password is incorrect.")
            conn.close()
            return

        # Check if new passwords match
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            conn.close()
            return

        # Check if the new password is valid (e.g., not empty)
        if not new_password:
            messagebox.showerror("Error", "New password cannot be empty.")
            conn.close()
            return

        # Update the password in the database
        cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, 'admin'))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password updated successfully!")
        self.main_screen()


    # Login Screen
    def login_screen(self):
        self.clear_window()
        
        # Header Label with Branding
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=20)
        logo_label = tk.Label(header_frame, text="Product Manager", font=("Arial", 24, "bold"), fg="#004d99")
        logo_label.grid(row=0, column=0)

        # Login Form Frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Password", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Button(self.root, text="Login", command=self.authenticate_user, bg="#004d99", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)
        tk.Button(self.root, text="Change Password", command=self.change_password_screen, font=("Arial", 10), fg="#004d99", bd=0).pack(pady=5)


    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if check_credentials(username, password):
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
  
    # Main Screen
    def main_screen(self):
        self.clear_window()

        # Header Section
        header_frame = tk.Frame(self.root, bg="#004d99", height=60)
        header_frame.pack(fill="x", pady=10)
        header_label = tk.Label(header_frame, text="Product Manager", font=("Arial", 20, "bold"), fg="white", bg="#004d99")
        header_label.pack(pady=15)

        # Search and Filter Section
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(search_frame, text="Search Product by Name or Category", font=("Arial", 12)).pack(side="left", padx=10)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.pack(side="left", padx=10, fill="x", expand=True)

        tk.Label(search_frame, text="Category", font=("Arial", 12)).pack(side="left", padx=10)
        self.category_combobox = ttk.Combobox(search_frame, values=CATEGORIES + ["All"], state="readonly", font=("Arial", 12))
        self.category_combobox.set("All")
        self.category_combobox.pack(side="left", padx=10)

        self.create_product_list_widget()  # Ensure Treeview is created

        # Bind the search entry and category combo box to trigger the search
        self.search_entry.bind("<KeyRelease>", self.search_product)  # Trigger search as you type
        self.category_combobox.bind("<<ComboboxSelected>>", self.search_product)  # Trigger search when category changes

        # Button Section
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10, fill="x")

        tk.Button(button_frame, text="Add Product", command=self.add_product, bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=20).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Product", command=self.update_product, bg="#ffc107", fg="black", font=("Arial", 12, "bold"), width=20).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Product", command=self.delete_product, bg="#dc3545", fg="white", font=("Arial", 12, "bold"), width=20).pack(side="left", padx=10)

        self.load_products()  # Initially load all products

    # Predefined categories
    def add_product(self):
        self.clear_window()

        # Header Section
        tk.Label(self.root, text="Add New Product", font=("Arial", 18, "bold"), fg="#004d99").pack(pady=10)

        # Form Section
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(form_frame, text="Product Name", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Quantity", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.quantity_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.quantity_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Category", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.category_combobox = ttk.Combobox(form_frame, values=CATEGORIES, font=("Arial", 12), state="readonly")
        self.category_combobox.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Product Type", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.type_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.type_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Imported From", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.imported_from_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.imported_from_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Expiration Date", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.expiration_entry = DateEntry(form_frame, date_pattern="yyyy-mm-dd", font=("Arial", 12))
        self.expiration_entry.pack(fill="x", padx=10, pady=5)

        # Action Buttons
        tk.Button(self.root, text="Save Product", command=self.save_product, bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_screen, bg="#6c757d", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    def save_changes(self):
        # Ensure the treeview exists before using it
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            self.create_product_list_widget()  # Create the tree if it doesn't exist

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected.")
            return

        product_id = self.tree.item(selected_item[0])['values'][0]
        
        # Proceed with updating product
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        category = self.category_combobox.get()
        product_type = self.type_entry.get()
        imported_from = self.imported_from_entry.get()
        expiration_date = self.expiration_entry.get()  # Date from the DateEntry widget
        
        try:
            # Validate the date format
            datetime.strptime(expiration_date, "%Y-%m-%d")

            # Update product in the database
            conn = sqlite3.connect('product_manager.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name=?, quantity=?, expiration_date=?, category=?, type=?, imported_from=? WHERE id=?",
                (name, int(quantity), expiration_date, category, product_type, imported_from, product_id)
            )
            conn.commit()
            conn.close()

            self.load_products()  # Reload the products to reflect changes
            messagebox.showinfo("Success", "Product updated successfully!")

        except ValueError:
            # This will catch the ValueError if the date format is incorrect
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

    def update_product(self):
        # Ensure an item is selected from the treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected.")
            return

        # Fetch the product details based on the selected item
        product_id = self.tree.item(selected_item[0])['values'][0]
        conn = sqlite3.connect('product_manager.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        conn.close()

        if not product:
            messagebox.showerror("Error", "Product not found in the database.")
            return

        self.clear_window()

        # Header Section
        tk.Label(self.root, text="Update Product", font=("Arial", 18, "bold"), fg="#004d99").pack(pady=10)

        # Form Section
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Pre-fill fields with the product's details
        tk.Label(form_frame, text="Product Name", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.name_entry.insert(0, product[1])  # Pre-fill name
        self.name_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Quantity", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.quantity_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.quantity_entry.insert(0, product[2])  # Pre-fill quantity
        self.quantity_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Category", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.category_combobox = ttk.Combobox(form_frame, values=CATEGORIES, font=("Arial", 12), state="readonly")
        self.category_combobox.set(product[4])  # Pre-fill category
        self.category_combobox.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Product Type", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.type_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.type_entry.insert(0, product[5])  # Pre-fill product type
        self.type_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Imported From", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.imported_from_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.imported_from_entry.insert(0, product[6])  # Pre-fill imported from
        self.imported_from_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Expiration Date", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        self.expiration_entry = DateEntry(form_frame, date_pattern="yyyy-mm-dd", font=("Arial", 12))
        self.expiration_entry.set_date(product[3])  # Pre-fill expiration date
        self.expiration_entry.pack(fill="x", padx=10, pady=5)

        # Action Buttons
        tk.Button(self.root, text="Save Changes", command=lambda: self.save_updated_product(product_id), bg="#ffc107", fg="black", font=("Arial", 12, "bold"), width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_screen, bg="#6c757d", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    def save_updated_product(self, product_id):
        # Fetch the updated details from the entry fields
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        expiration_date = self.expiration_entry.get()  # Date from the Entry widget
        category = self.category_combobox.get()
        product_type = self.type_entry.get()
        imported_from = self.imported_from_entry.get()

        try:
            # Validate the date format
            datetime.strptime(expiration_date, "%Y-%m-%d")

            # Update the product in the database
            conn = sqlite3.connect('product_manager.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name=?, quantity=?, expiration_date=?, category=?, type=?, imported_from=? WHERE id=?",
                (name, int(quantity), expiration_date, category, product_type, imported_from, product_id)
            )
            conn.commit()
            conn.close()

            self.main_screen()
            messagebox.showinfo("Success", "Product updated successfully!")

        except ValueError:
            # This will catch the ValueError if the date format is incorrect
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")


    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected.")
            return
        product_id = self.tree.item(selected_item[0])['values'][0]

        conn = sqlite3.connect('product_manager.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        self.load_products()
        messagebox.showinfo("Success", "Product deleted successfully!")

    def search_product(self, event=None):
        search_text = self.search_entry.get().lower()  # Convert to lower case for case-insensitive search
        selected_category = self.category_combobox.get()
        
        # Connect to the database and fetch products based on search and category
        conn = sqlite3.connect('product_manager.db')
        cursor = conn.cursor()
        
        if selected_category == "All":
            cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ?", 
                        ('%' + search_text + '%', '%' + search_text + '%'))
        else:
            cursor.execute("SELECT * FROM products WHERE (name LIKE ? OR category LIKE ?) AND category=?",
                        ('%' + search_text + '%', '%' + search_text + '%', selected_category))
        
        products = cursor.fetchall()
        conn.close()
        
        # Clear existing tree items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        today = date.today()
        warning_date = today + timedelta(days=7)

        for product in products:
            exp_date = datetime.strptime(product[3], "%Y-%m-%d").date()

            # Determine the tag based on expiration date
            if exp_date < today:
                tag = "expired"
            elif exp_date <= warning_date:
                tag = "warning"
            else:
                tag = None

            # Insert the filtered product into the tree with the appropriate tag
            self.tree.insert("", "end", values=product, tags=(tag,))

        # Configure tags for highlighting
        self.tree.tag_configure("expired", background="red", foreground="white")
        self.tree.tag_configure("warning", background="yellow", foreground="black")



    def load_products(self):
        # Check if the tree exists, otherwise recreate it
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            self.create_product_list_widget()

        # Clear existing tree items
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('product_manager.db')
        cursor = conn.cursor()

        # Fetch products sorted by ID
        cursor.execute("SELECT * FROM products ORDER BY id ASC")
        products = cursor.fetchall()
        conn.close()

        today = date.today()
        warning_date = today + timedelta(days=7)

        for product in products:
            exp_date = datetime.strptime(product[3], "%Y-%m-%d").date()

            # Determine the tag based on expiration date
            if exp_date < today:
                tag = "expired"
            elif exp_date <= warning_date:
                tag = "warning"
            else:
                tag = None

            # Insert the product into the tree with the determined tag
            self.tree.insert("", "end", values=product, tags=(tag,))

        # Configure tags for highlighting
        self.tree.tag_configure("expired", background="red", foreground="white")
        self.tree.tag_configure("warning", background="yellow", foreground="black")

    def create_product_list_widget(self):
        # Create the Treeview widget for displaying products
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Quantity", "Expiration Date", "Category", "Type", "Imported From"), show="headings", height=15)
        self.tree.pack(pady=10, padx=20, fill="x")
        for col in ("ID", "Name", "Quantity", "Expiration Date", "Category", "Type", "Imported From"):
            self.tree.heading(col, text=col)

    def display_products(self, products):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for product in products:
            self.tree.insert("", "end", values=product)



    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Setup
setup_database()
add_initial_user()

# Run Application
root = tk.Tk()
app = ProductManagerApp(root)
root.mainloop()