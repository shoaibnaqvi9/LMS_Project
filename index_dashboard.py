from tkinter import *
from tkinter import messagebox, ttk
import pypyodbc as odbc
from datetime import datetime
def get_connection():
    DRIVER_NAME = "SQL SERVER"
    SERVER_NAME = "DESKTOP-OFOE4B8\SQLEXPRESS"
    DATABASE_NAME = "library"
    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={{{SERVER_NAME}}};
        DATABASE={{{DATABASE_NAME}}};
        Trust_Connection=yes;
        """
    return odbc.connect(connection_string)

def create_book(conn, title, isbn, publish, publish_year, category_ID, quantity):
    cursor = conn.cursor()
    query = """
    INSERT INTO Books (Title, ISBN, Publisher, PublicationYear, CategoryID, Quantity)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (title, isbn, publish, publish_year, category_ID, quantity))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Book added successfully")

def read_books(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM Books"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def update_book(conn, book_id, title=None, isbn=None, publish=None, publish_year=None, category_ID=None, quantity=None):
    cursor = conn.cursor()
    query = "UPDATE Books SET"
    params = []
    if title:
        query += " Title = ?,"
        params.append(title)
    if isbn:
        query += " ISBN = ?,"
        params.append(isbn)
    if publish:
        query += " Publisher = ?,"
        params.append(publish)
    if publish_year:
        query += " PublicationYear = ?,"
        params.append(publish_year)
    if category_ID:
        query += " CategoryID = ?,"
        params.append(category_ID)
    if quantity:
        query += " Quantity = ?,"
        params.append(quantity)

    query = query.rstrip(',')
    query += " WHERE BookID = ?"
    params.append(book_id)

    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Book updated successfully")

def delete_book(conn, book_id):
    cursor = conn.cursor()
    query = "DELETE FROM Books WHERE BookID = ?"
    cursor.execute(query, (book_id,))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Book deleted successfully")

def add_book_gui():
    add_window = Toplevel(root)
    add_window.title("Add Book")
    add_window.configure(bg="#2c3e50")
    
    label_font = ("Arial", 12)
    entry_bg = "#ecf0f1"
    entry_fg = "#2c3e50"
    button_bg = "#3498db"
    button_fg = "white"
    button_font = ("Arial", 10, "bold")

    Label(add_window, text="Title", fg="white", bg="#2c3e50", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="ISBN", fg="white", bg="#2c3e50", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Publisher", fg="white", bg="#2c3e50", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Publication Year", fg="white", bg="#2c3e50", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Category", fg="white", bg="#2c3e50", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Quantity", fg="white", bg="#2c3e50", font=label_font).grid(row=5, column=0, padx=10, pady=5, sticky=W)

    title_entry = Entry(add_window, bg=entry_bg, fg=entry_fg, width=30)
    isbn_entry = Entry(add_window, bg=entry_bg, fg=entry_fg, width=30)
    publisher_entry = Entry(add_window, bg=entry_bg, fg=entry_fg, width=30)
    pub_year_entry = Entry(add_window, bg=entry_bg, fg=entry_fg, width=30)
    quantity_entry = Entry(add_window, bg=entry_bg, fg=entry_fg, width=30)

    title_entry.grid(row=0, column=1, padx=10, pady=5)
    isbn_entry.grid(row=1, column=1, padx=10, pady=5)
    publisher_entry.grid(row=2, column=1, padx=10, pady=5)
    pub_year_entry.grid(row=3, column=1, padx=10, pady=5)
    quantity_entry.grid(row=5, column=1, padx=10, pady=5)

    cursor = conn.cursor()
    cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
    categories = cursor.fetchall()
    cursor.close()

    category_dict = {cat[1]: cat[0] for cat in categories}

    category_names = list(category_dict.keys())

    category_combobox = ttk.Combobox(add_window, values=category_names, state="readonly")
    category_combobox.grid(row=4, column=1)
    category_combobox.set("Select Category")

    def add_book():
        title = title_entry.get().strip()
        isbn = isbn_entry.get().strip()
        publisher = publisher_entry.get().strip()
        publication_year = pub_year_entry.get().strip()
        quantity = quantity_entry.get().strip()
        selected_category = category_combobox.get()

        if not title or not isbn or not publisher or not publication_year or not quantity or selected_category == "Select Category":
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if not publication_year.isdigit() or not quantity.isdigit():
            messagebox.showwarning("Input Error", "Publication Year and Quantity must be numeric.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Books WHERE ISBN = ?", (isbn,))
            result = cursor.fetchone()
            if result[0] > 0:
                messagebox.showerror("Duplicate ISBN", "The ISBN you entered already exists in the database.")
                cursor.close()
                return
            cursor.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to check ISBN uniqueness:\n{e}")
            return
        try:
            category_id = category_dict[selected_category]
            create_book(conn, title, isbn, publisher, int(publication_year), category_id, int(quantity))
            refresh_books_list()
            messagebox.showinfo("Success", "Book added successfully.")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add book:\n{e}")

    Button(add_window, text='Add Book', width=15, command=add_book).grid(row=6, column=0, columnspan=2, pady=15)
    def add_back():
        add_window.destroy()
    Button(add_window, text='Back', command=add_back).grid(row=6, column=2, sticky=W, pady=4)
def exit_program():
    root.destroy()
    
def refresh_books_list():
    books = read_books(conn)
    for i in tree.get_children():
        tree.delete(i)
    for book in books:
        tree.insert("", "end", values=book)

def update_book_gui():
    update_window = Toplevel(root)
    update_window.title("Update Book")
    update_window.configure(bg="#2c3e50")
      
    label_font = ("Arial", 12)
    entry_bg = "#ecf0f1"
    entry_fg = "#2c3e50"
    button_bg = "#3498db"
    button_fg = "white"
    button_font = ("Arial", 10, "bold")
    
    Label(update_window, text="Book ID", fg="white", bg="#2c3e50", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="Title", fg="white", bg="#2c3e50", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="ISBN", fg="white", bg="#2c3e50", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="Publisher", fg="white", bg="#2c3e50", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="Publication Year", fg="white", bg="#2c3e50", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="Category", fg="white", bg="#2c3e50", font=label_font).grid(row=5, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="Quantity", fg="white", bg="#2c3e50", font=label_font).grid(row=6, column=0, padx=10, pady=5, sticky=W)

    book_id_entry = Entry(update_window, bg=entry_bg, fg=entry_fg, width=30)
    title_entry = Entry(update_window, bg=entry_bg, fg=entry_fg, width=30)
    isbn_entry = Entry(update_window, bg=entry_bg, fg=entry_fg, width=30)
    publisher_entry = Entry(update_window, bg=entry_bg, fg=entry_fg, width=30)
    pub_year_entry = Entry(update_window, bg=entry_bg, fg=entry_fg, width=30)
    quantity_entry = Entry(update_window, bg=entry_bg, fg=entry_fg, width=30)

    book_id_entry.grid(row=0, column=1, padx=10, pady=5)
    title_entry.grid(row=1, column=1, padx=10, pady=5)
    isbn_entry.grid(row=2, column=1, padx=10, pady=5)
    publisher_entry.grid(row=3, column=1, padx=10, pady=5)
    pub_year_entry.grid(row=4, column=1, padx=10, pady=5)
    quantity_entry.grid(row=6, column=1, padx=10, pady=5)

    cursor = conn.cursor()
    cursor.execute("SELECT CategoryID, CategoryName FROM Categories")
    categories = cursor.fetchall()
    cursor.close()

    category_dict = {cat[1]: cat[0] for cat in categories}
    category_names = list(category_dict.keys())

    category_combobox = ttk.Combobox(update_window, values=category_names, state="readonly")
    category_combobox.grid(row=5, column=1)
    category_combobox.set("Select Category")

    def update_book_data():
        book_id = book_id_entry.get().strip()
        title = title_entry.get().strip()
        isbn = isbn_entry.get().strip()
        publisher = publisher_entry.get().strip()
        publication_year = pub_year_entry.get().strip()
        quantity = quantity_entry.get().strip()
        selected_category = category_combobox.get()

        if not book_id or selected_category == "Select Category":
            messagebox.showwarning("Input Error", "Please fill in all mandatory fields.")
            return

        if not book_id.isdigit() or (publication_year and not publication_year.isdigit()) or (quantity and not quantity.isdigit()):
            messagebox.showwarning("Input Error", "Book ID, Publication Year, and Quantity must be numeric.")
            return

        try:
            category_id = category_dict[selected_category]
            update_book(conn, int(book_id), title, isbn, publisher, int(publication_year) if publication_year else None, category_id, int(quantity) if quantity else None)
            refresh_books_list()
            messagebox.showinfo("Success", "Book updated successfully.")
            update_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update book:\n{e}")

    Button(update_window, text='Update Book', width=15, command=update_book_data, bg=button_bg, fg=button_fg, font=button_font).grid(row=7, column=0, columnspan=2, pady=15)
    Button(update_window, text='Back', command=update_window.destroy, bg=button_bg, fg=button_fg, font=button_font).grid(row=7, column=2, sticky=W, pady=4)

def delete_book_gui():
    delete_window = Toplevel(root)
    delete_window.title("Delete Book")
    delete_window.configure(bg="#2c3e50")  # Set background color
    
    label_font = ("Arial", 12)
    entry_bg = "#ecf0f1"
    entry_fg = "#2c3e50"
    button_bg = "#3498db"
    button_fg = "white"
    button_font = ("Arial", 10, "bold")

    Label(delete_window, text="Book ID", fg="white", bg="#2c3e50", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky=W)

    book_id_entry = Entry(delete_window, bg=entry_bg, fg=entry_fg, width=30)
    book_id_entry.grid(row=0, column=1, padx=10, pady=5)

    def delete_book_data():
        book_id = book_id_entry.get().strip()

        if not book_id:
            messagebox.showwarning("Input Error", "Please enter a Book ID.")
            return

        if not book_id.isdigit():
            messagebox.showwarning("Input Error", "Book ID must be numeric.")
            return

        try:
            delete_book(conn, int(book_id))
            refresh_books_list()
            delete_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete book:\n{e}")

    Button(delete_window, text='Delete Book', width=15, command=delete_book_data, bg=button_bg, fg=button_fg, font=button_font).grid(row=1, column=0, columnspan=2, pady=15)
    Button(delete_window, text='Back', command=delete_window.destroy, bg=button_bg, fg=button_fg, font=button_font).grid(row=1, column=2, sticky=W, pady=4)

def start_dashboard():
    global root, conn, tree
    root = Tk()
    root.title("Library Management Dashboard")
    root.configure(bg="#34495e")

    style = ttk.Style()
    style.configure("Treeview", background="#34495e", fieldbackground="#34495e", foreground="white")

    main_label_font = ("Arial", 16, "bold")
    button_bg = "#e74c3c"
    button_fg = "white"
    button_font = ("Arial", 12, "bold")

    Label(root, text="Library Management System", fg="white", bg="#34495e", font=main_label_font).pack(pady=10)

    Button(root, text='Add Book', command=add_book_gui, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
    Button(root, text='Update Book', command=update_book_gui, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
    Button(root, text='Delete Book', command=delete_book_gui, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)
    Button(root, text='Exit', command=exit_program, bg=button_bg, fg=button_fg, font=button_font).pack(pady=5)

    tree = ttk.Treeview(root, columns=("BookID", "Title", "ISBN", "Publisher", "PublicationYear", "CategoryID", "Quantity"), show="headings")
    tree.heading("BookID", text="BookID")
    tree.heading("Title", text="Title")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Publisher", text="Publisher")
    tree.heading("PublicationYear", text="PublicationYear")
    tree.heading("CategoryID", text="CategoryID")
    tree.heading("Quantity", text="Quantity")
    tree.pack(pady=20)

    conn = get_connection()
    refresh_books_list()
    root.mainloop()
