import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    year INTEGER
)''')

c.execute('''CREATE TABLE members (
    member_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT
)''')

c.execute('''CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    member_id INTEGER,
    issue_date TEXT,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES books (book_id),
    FOREIGN KEY (member_id) REFERENCES members (member_id)
)''')

conn.commit()
conn.close()