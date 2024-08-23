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
    query = """
    SELECT b.BookID, b.Title, b.ISBN, b.Publisher, b.PublicationYear, c.CategoryName, b.Quantity
    FROM Books b
    JOIN Categories c ON b.CategoryID = c.CategoryID
    """
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
    delete_window.configure(bg="#2c3e50")
    
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

def create_category(conn, CategoryName):
    cursor = conn.cursor()
    query = """
    INSERT INTO Categories (CategoryName)
    VALUES (?)
    """
    cursor.execute(query, (CategoryName))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "New category added successfully")

def add_category_gui():
    add_window = Toplevel(root)
    add_window.title("Add Category")
    add_window.configure(bg="#2c3e50")
    
    label_font = ("Arial", 12)
    entry_bg = "#ecf0f1"
    entry_fg = "#2c3e50"
    button_bg = "#3498db"
    button_fg = "white"
    button_font = ("Arial", 10, "bold")
    Label(add_window, text="Category", fg="white", bg="#2c3e50", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Category = Entry(add_window, bg=entry_bg, fg=entry_fg, width=30)
    Category.grid(row=0, column=1, padx=10, pady=5)
    def add_category():
        CategoryName = Category.get().strip()
        
        if not CategoryName:
            messagebox.showwarning("Input Error", "Please fill in the field.")
            return
        try:
            create_category(conn, CategoryName)
            messagebox.showinfo("Success", "New Category added successfully.")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add category:\n{e}")
    def add_back():
        add_window.destroy()
    Button(add_window, text='Add Category', width=15, command=add_category).grid(row=6, column=0, columnspan=2, pady=15)
    Button(add_window, text='Back', command=add_back).grid(row=6, column=2, sticky=W, pady=4)

def search_books(conn, search_term):
    cursor = conn.cursor()
    query = """
    SELECT b.BookID, b.Title, b.ISBN, b.Publisher, b.PublicationYear, c.CategoryName, b.Quantity
    FROM Books b
    JOIN Categories c ON b.CategoryID = c.CategoryID
    WHERE Title LIKE ? OR ISBN LIKE ? OR Publisher LIKE ? OR PublicationYear LIKE ? OR c.CategoryName LIKE ?
    """
    search_term = f"%{search_term}%"
    cursor.execute(query, (search_term, search_term, search_term, search_term, search_term))
    rows = cursor.fetchall()
    cursor.close()
    return rows
def search_books_gui():
    search_term = search_entry.get().strip()
    if search_term:
        books = search_books(conn, search_term)
        for i in tree.get_children():
            tree.delete(i)
        for book in books:
            tree.insert("", "end", values=book)
    else:
        refresh_books_list()

def create_student(conn, first_name, last_name, email, phone, address, admission_date):
    cursor = conn.cursor()
    query = """
    INSERT INTO Students (S_FirstName, S_LastName, S_Email, S_Phone, S_address, S_AdmissionDate)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (first_name, last_name, email, phone, address, admission_date))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Student added successfully")

def add_student_gui():
    add_window = Toplevel(root)
    add_window.title("Add Student")
    add_window.configure(bg="#2c3e50")
    
    Label(add_window, text="First Name:", bg="#2c3e50", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Last Name:", bg="#2c3e50", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Email:", bg="#2c3e50", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Phone:", bg="#2c3e50", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Address:", bg="#2c3e50", fg="#ffffff").grid(row=4, column=0, padx=10, pady=5, sticky=W)
    
    first_name_entry = Entry(add_window)
    last_name_entry = Entry(add_window)
    email_entry = Entry(add_window)
    phone_entry = Entry(add_window)
    address_entry = Entry(add_window)

    first_name_entry.grid(row=0, column=1, padx=10, pady=5)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    phone_entry.grid(row=3, column=1, padx=10, pady=5)
    address_entry.grid(row=4, column=1, padx=10, pady=5)

    def add_student():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not first_name or not last_name or not email:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return
        create_student(conn, first_name, last_name, email, phone, address, admission_date)
    
    Button(add_window, text='Add Student', width=15, command=add_student).grid(row=6, column=0, columnspan=2, pady=15)
    Button(add_window, text='Back', command=add_window.destroy).grid(row=6, column=2, sticky=W, pady=4)

def create_reservation(conn, book_id, student_id, reservation_date, status):
    cursor = conn.cursor()
    query = """
    INSERT INTO Reservations (BookID, S_ID, ReservationDate, R_Status)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (book_id, student_id, reservation_date, status))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Reservation added successfully")

def add_reservation_gui():
    add_window = Toplevel(root)
    add_window.title("Add Reservation")
    add_window.configure(bg="#2c3e50")

    Label(add_window, text="Book ID:", bg="#2c3e50", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Student ID:", bg="#2c3e50", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    Label(add_window, text="Status:", bg="#2c3e50", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    
    book_id_entry = Entry(add_window)
    student_id_entry = Entry(add_window)
    status_combobox = ttk.Combobox(add_window, values=["Pending", "Approved", "Cancelled"])
    status_combobox.set("Pending")

    book_id_entry.grid(row=0, column=1, padx=10, pady=5)
    student_id_entry.grid(row=1, column=1, padx=10, pady=5)
    status_combobox.grid(row=3, column=1, padx=10, pady=5)
    
    def add_reservation():
        book_id = book_id_entry.get()
        student_id = student_id_entry.get()
        reservation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = status_combobox.get()

        if not book_id or not student_id or not reservation_date:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return
        create_reservation(conn, book_id, student_id, reservation_date, status)
        messagebox.showinfo("Success", "Reservation added successfully.")
        add_window.destroy()

    Button(add_window, text='Add Reservation', width=15, command=add_reservation).grid(row=4, column=0, columnspan=2, pady=15)
    Button(add_window, text='Back', command=add_window.destroy).grid(row=4, column=2, sticky=W, pady=4)

def update_reservation(conn, r_id, book_id=None, student_id=None, reservation_date=None, status=None):
    cursor = conn.cursor()
    query = "UPDATE Reservations SET"
    params = []
    if book_id:
        query += " BookID = ?,"
        params.append(book_id)
    if student_id:
        query += " S_ID = ?,"
        params.append(student_id)
    if reservation_date:
        query += " ReservationDate = ?,"
        params.append(reservation_date)
    if status:
        query += " R_Status = ?,"
        params.append(status)
    
    query = query.rstrip(',')
    query += " WHERE R_ID = ?"
    params.append(r_id)
    
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Reservation updated successfully")

def delete_reservation(conn, r_id):
    cursor = conn.cursor()
    query = "DELETE FROM Reservations WHERE R_ID = ?"
    cursor.execute(query, (r_id,))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Reservation deleted successfully")

def update_reservation_gui():
    update_window = Toplevel(root)
    update_window.title("Update Reservation")
    update_window.configure(bg="#2c3e50")

    Label(update_window, text="Reservation ID:", bg="#2c3e50", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="New Book ID:", bg="#2c3e50", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="New Student ID:", bg="#2c3e50", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5, sticky=W)
    Label(update_window, text="New Status:", bg="#2c3e50", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    
    reservation_id_entry = Entry(update_window)
    book_id_entry = Entry(update_window)
    student_id_entry = Entry(update_window)
    status_combobox = ttk.Combobox(update_window, values=["Pending", "Approved", "Cancelled"])
    
    reservation_id_entry.grid(row=0, column=1, padx=10, pady=5)
    book_id_entry.grid(row=1, column=1, padx=10, pady=5)
    student_id_entry.grid(row=2, column=1, padx=10, pady=5)
    status_combobox.set("Pending")
    status_combobox.grid(row=3, column=1, padx=10, pady=5)
    
    def update_reservation_data():
        reservation_id = reservation_id_entry.get()
        book_id = book_id_entry.get()
        student_id = student_id_entry.get()
        reservation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = status_combobox.get()

        if not reservation_id or not book_id or not student_id:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return
        
        update_reservation(reservation_id, book_id, student_id, reservation_date, status)
        messagebox.showinfo("Success", "Reservation updated successfully.")
        update_window.destroy()

    Button(update_window, text='Update Reservation', width=15, command=update_reservation_data).grid(row=5, column=0, columnspan=2, pady=15)
    Button(update_window, text='Back', command=update_window.destroy).grid(row=5, column=2, sticky=W, pady=4)

def delete_reservation_gui():
    delete_window = Toplevel(root)
    delete_window.title("Delete Reservation")
    delete_window.configure(bg="#2c3e50")

    Label(delete_window, text="Reservation ID:", bg="#2c3e50", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    reservation_id_entry = Entry(delete_window)
    reservation_id_entry.grid(row=0, column=1, padx=10, pady=5)
    
    def delete_reservation_data():
        reservation_id = reservation_id_entry.get()
        if not reservation_id:
            messagebox.showwarning("Input Error", "Please provide the Reservation ID.")
            return
        delete_reservation(reservation_id)
        messagebox.showinfo("Success", "Reservation deleted successfully.")
        delete_window.destroy()

    Button(delete_window, text='Delete Reservation', width=15, command=delete_reservation_data).grid(row=1, column=0, columnspan=2, pady=15)
    Button(delete_window, text='Back', command=delete_window.destroy).grid(row=1, column=2, sticky=W, pady=4)


def start_dashboard():
    global root, conn, tree, search_entry
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

    search_frame = Frame(root, bg="#34495e")
    search_frame.pack(pady=5)

    search_label = Label(search_frame, text="Search", fg="white", bg="#34495e", font=("Arial", 12))
    search_label.pack(side=LEFT, padx=10)

    search_entry = Entry(search_frame, width=30)
    search_entry.pack(side=LEFT, padx=10)

    search_button = Button(search_frame, text="Search", command=search_books_gui, bg=button_bg, fg=button_fg, font=button_font)
    search_button.pack(side=LEFT)

    button_frame = Frame(root, bg="#34495e")
    button_frame.pack(pady=10)

    Button(button_frame, text='Add Book', command=add_book_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Add Category', command=add_category_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Update Book', command=update_book_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Delete Book', command=delete_book_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Add Student', command=add_student_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Add Reservation', command=add_reservation_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Update Reservation', command=update_reservation_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Delete Reservation', command=delete_reservation_gui, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)
    Button(button_frame, text='Exit', command=exit_program, bg=button_bg, fg=button_fg, font=button_font).pack(side='left', padx=5)

    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    tree = ttk.Treeview(root, columns=("BookID", "Title", "ISBN", "Publisher", "PublicationYear", "CategoryName", "Quantity"), show="headings")
    tree.heading("BookID", text="BookID")
    tree.heading("Title", text="Title")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Publisher", text="Publisher")
    tree.heading("PublicationYear", text="PublicationYear")
    tree.heading("CategoryName", text="CategoryName")
    tree.heading("Quantity", text="Quantity")
    tree.pack(pady=20)

    conn = get_connection()
    refresh_books_list()
    root.mainloop()
    