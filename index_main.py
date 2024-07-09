from tkinter import *
import pandas as pd
import pypyodbc as odbc

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

conn = get_connection()
print(conn)



def create_book(conn, title, isbn, publish, publish_year, category_ID, quantity):
    cursor = conn.cursor()
    query = """
    INSERT INTO Books (Title, ISBN, Publisher, PublicationYear, CategoryID, Quantity)
    VALUES (?, ?, ?)
    """
    cursor.execute(query, (title, isbn, publish, publish_year, category_ID, quantity))
    conn.commit()
    cursor.close()


def read_books(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM Books"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()


def update_book(conn, book_id, title=None, author=None, isbn=None):
    cursor = conn.cursor()
    query = "UPDATE Books SET"
    params = []
    if title:
        query += " Title = ?,"
        params.append(title)
    if isbn:
        query += " ISBN = ?,"
        params.append(isbn)

    # Remove trailing comma
    query = query.rstrip(',')
    query += " WHERE BookID = ?"
    params.append(book_id)

    cursor.execute(query, params)
    conn.commit()
    cursor.close()


def delete_book(conn, book_id):
    cursor = conn.cursor()
    query = "DELETE FROM Books WHERE BookID = ?"
    cursor.execute(query, (book_id,))
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    conn = get_connection()

    # Create a book
    create_book(conn,"To Kill a Mockingbird", "9780060935467", "Harper Perennial", 1960, 1, 5)

    # Read all books
    print("Books in the library:")
    read_books(conn)

    # Update a book
    update_book(conn, 1, title='The Great Gatsby Revised')

    # Read all books again to see the update
    print("Books in the library after update:")
    read_books(conn)

    # Delete a book
    delete_book(conn, 1)

    # Read all books again to see the deletion
    print("Books in the library after deletion:")
    read_books(conn)

    conn.close()
