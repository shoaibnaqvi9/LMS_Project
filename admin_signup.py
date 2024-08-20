from tkinter import *
from tkinter import messagebox
import pypyodbc as odbc
from datetime import datetime
import hashlib
import admin_login

def get_connection():
    DRIVER_NAME = "SQL SERVER"
    SERVER_NAME = r"DESKTOP-OFOE4B8\SQLEXPRESS"
    DATABASE_NAME = "library"
    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={{{SERVER_NAME}}};
        DATABASE={{{DATABASE_NAME}}};
        Trust_Connection=yes;
        """
    try:
        conn = odbc.connect(connection_string)
        return conn
    except odbc.Error as e:
        messagebox.showerror("Connection Error", f"Error connecting to the database: {e}")
        exit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def new_admin_signup(conn, FirstName, LastName, Email, Phone, Password, LibrariansAdmissionDate):
    cursor = conn.cursor()
    query = """
    INSERT INTO Librarians (FirstName, LastName, Email, Phone, Password, LibrariansAdmissionDate)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    hashed_password = hash_password(Password)
    cursor.execute(query, (FirstName, LastName, Email, Phone, hashed_password, LibrariansAdmissionDate))
    conn.commit()
    cursor.close()
    messagebox.showinfo("Success", "Librarian added successfully")

def add_admin():
    if Password.get() != ConfirmPassword.get():
        messagebox.showerror("Error", "Passwords do not match!")
        return

    LibrariansAdmissionDate = datetime.now()
    new_admin_signup(conn, FirstName.get(), LastName.get(), Email.get(), Phone.get(), Password.get(), LibrariansAdmissionDate)

def login_gui():
    admin_login.main()

def exit():
    conn.close()
    root.destroy()

def main():
    global root, conn, FirstName, LastName, Email, Phone, Password, ConfirmPassword
    root = Tk()
    root.geometry("500x350")
    root.title("Library Management System - Admin Signup")
    root.columnconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)

    Label(root, text="FirstName").grid(row=0)
    Label(root, text="LastName").grid(row=1)
    Label(root, text="Email").grid(row=2)
    Label(root, text="Phone").grid(row=3)
    Label(root, text="Password").grid(row=4)
    Label(root, text="ConfirmPassword").grid(row=5)

    FirstName = Entry(root)
    LastName = Entry(root)
    Email = Entry(root)
    Phone = Entry(root)
    Password = Entry(root, show="*")
    ConfirmPassword = Entry(root, show="*")

    FirstName.grid(row=0, column=1)
    LastName.grid(row=1, column=1)
    Email.grid(row=2, column=1)
    Phone.grid(row=3, column=1)
    Password.grid(row=4, column=1)
    ConfirmPassword.grid(row=5, column=1)

    Button(root, text='Register', fg='white', bg='black', width='10', command= add_admin).grid(row=7, column=0, sticky=W, pady=2)
    Button(root, text='Login', fg='white', bg='black', width='10', command= login_gui).grid(row=7, column=1, sticky=W, pady=2)
    Button(root, text='Exit', fg='white', bg='black', width='10', command= exit).grid(row=7, column=2, sticky=W, pady=2)

    conn = get_connection()
    root.mainloop()

main()
