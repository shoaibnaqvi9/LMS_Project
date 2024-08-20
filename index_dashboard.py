from tkinter import *
from tkinter import messagebox, ttk
import pypyodbc as odbc
import admin_signup

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

    # Remove trailing comma
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

    Label(add_window, text="Title", fg="white", bg="black").grid(row=0)
    Label(add_window, text="ISBN").grid(row=1)
    Label(add_window, text="Publisher").grid(row=2)
    Label(add_window, text="PublicationYear").grid(row=3)
    Label(add_window, text="CategoryID").grid(row=4)
    Label(add_window, text="Quantity").grid(row=5)

    title = Entry(add_window)
    isbn = Entry(add_window)
    publish = Entry(add_window)
    publish_year = Entry(add_window)
    category_ID = Entry(add_window)
    quantity = Entry(add_window)

    title.grid(row=0, column=1)
    isbn.grid(row=1, column=1)
    publish.grid(row=2, column=1)
    publish_year.grid(row=3, column=1)
    category_ID.grid(row=4, column=1)
    quantity.grid(row=5, column=1)

    def add_book():
        create_book(conn, title.get(), isbn.get(), publish.get(), publish_year.get(), category_ID.get(), quantity.get())
        refresh_books_list()

    Button(add_window, text='Add', command=add_book).grid(row=6, column=1, sticky=W, pady=4)
    def add_back():
        add_window.destroy()
    Button(add_window, text='Back', command=add_back).grid(row=1, column=2, sticky=W, pady=3)
def exit():
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

    Label(update_window, text="Book ID").grid(row=0)
    Label(update_window, text="Title").grid(row=1)
    Label(update_window, text="ISBN").grid(row=2)
    Label(update_window, text="Publisher").grid(row=3)
    Label(update_window, text="Publication Year").grid(row=4)
    Label(update_window, text="Category ID").grid(row=5)
    Label(update_window, text="Quantity").grid(row=6)

    book_id = Entry(update_window)
    title = Entry(update_window)
    isbn = Entry(update_window)
    publish = Entry(update_window)
    publish_year = Entry(update_window)
    category_ID = Entry(update_window)
    quantity = Entry(update_window)

    book_id.grid(row=0, column=1)
    title.grid(row=1, column=1)
    isbn.grid(row=2, column=1)
    publish.grid(row=3, column=1)
    publish_year.grid(row=4, column=1)
    category_ID.grid(row=5, column=1)
    quantity.grid(row=6, column=1)

    def update_book_details():
        update_book(conn, book_id.get(), title.get(), isbn.get(), publish.get(), publish_year.get(), category_ID.get(), quantity.get())
        refresh_books_list()

    Button(update_window, text='Update', command=update_book_details).grid(row=7, column=1, sticky=W, pady=4)
    def upd_back():
        update_window.destroy()
    Button(update_window, text='Back', command=upd_back).grid(row=1, column=2, sticky=W, pady=3)


def delete_book_gui():
    delete_window = Toplevel(root)
    delete_window.title("Delete Book")

    Label(delete_window, text="Book ID").grid(row=0)

    book_id = Entry(delete_window)
    book_id.grid(row=0, column=1)

    def delete_book_details():
        delete_book(conn, book_id.get())
        refresh_books_list()

    Button(delete_window, text='Delete', command=delete_book_details).grid(row=1, column=1, sticky=W, pady=4)
    def del_back():
        delete_window.destroy()
    Button(delete_window, text='Back', command=del_back).grid(row=1, column=2, sticky=W, pady=3)

if __name__ == '__main__':
    
    root = Tk()
    root.geometry("1200x600")
    root.title("Library Management System")
    root.columnconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)
    Button(root, text='Add Book', fg='white', bg='black', width='10', command=add_book_gui).grid(row=3, column=0, sticky=W, pady=2)
    Button(root, text='Update Book', fg='white', bg='black', width='10', command=update_book_gui).grid(row=3, column=1, sticky=W, pady=2)
    Button(root, text='Delete Book', fg='white', bg='black', width='10', command=delete_book_gui).grid(row=3, column=2, sticky=W, pady=2)
    Button(root, text='Exit', fg='white', bg='black', width='10', command=exit).grid(row=3, column=3, sticky=W, pady=2)
    style = ttk.Style()
    style.configure("Treeview.Heading", foreground="black")

    tree = ttk.Treeview(root, columns=('BookID', 'Title', 'ISBN', 'Publisher', 'PublicationYear', 'CategoryID', 'Quantity'), show='headings')
    tree.heading('BookID', text='BookID')
    tree.heading('Title', text='Title')
    tree.heading('ISBN', text='ISBN')
    tree.heading('Publisher', text='Publisher')
    tree.heading('PublicationYear', text='PublicationYear')
    tree.heading('CategoryID', text='CategoryID')
    tree.heading('Quantity', text='Quantity')

    tree.column('BookID', width=100)
    tree.column('Title', width=200)
    tree.column('ISBN', width=150)
    tree.column('Publisher', width=150)
    tree.column('PublicationYear', width=100)
    tree.column('CategoryID', width=100)
    tree.column('Quantity', width=80)

    tree.grid(row=0, column=1, rowspan=3, sticky=NSEW)

    tree.configure(style="Treeview")

    conn = get_connection()
    refresh_books_list()

    root.mainloop()