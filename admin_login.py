from tkinter import *
from tkinter import messagebox
import pypyodbc as odbc
import hashlib
import admin_signup, index_dashboard

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
    return odbc.connect(connection_string)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(conn, email, password):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM Librarians WHERE Email = ?"
        cursor.execute(query, (email.get(),))
        row = cursor.fetchone()
        
        if row is not None:
            stored_hashed_password = row[5]
            hashed_password = hash_password(password.get())
            
            print(f"Stored: {stored_hashed_password}")  # Debug: Print stored hashed password
            print(f"Entered: {hashed_password}")       # Debug: Print entered hashed password

            if stored_hashed_password == hashed_password:
                messagebox.showinfo("Success", "Login successful")
                root.destroy()
                index_dashboard.main()
            else:
                messagebox.showerror("Error", "Invalid email or password")
        else:
            messagebox.showerror("Error", "Invalid email or password")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()

def signup_gui():
    admin_signup.main()

def exit():
    root.destroy()

def main():
    global root, conn, email, password
    root = Tk()
    root.geometry("500x350")
    root.title("Library Management System - Admin Login")
    root.columnconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)

    Label(root, text="Email").grid(row=0)
    Label(root, text="Password").grid(row=1)

    email = Entry(root)
    password = Entry(root, show="*")

    email.grid(row=0, column=1)
    password.grid(row=1, column=1)
    conn = get_connection()
    
    Button(root, text='Login', fg='white', bg='black', width='10', command=lambda: login(conn, email, password)).grid(row=2, column=0, sticky=W, pady=2)
    Button(root, text='Signup', fg='white', bg='black', width='10', command=signup_gui).grid(row=2, column=1, sticky=W, pady=2)
    Button(root, text='Exit', fg='white', bg='black', width='10', command=exit).grid(row=2, column=2, sticky=W, pady=2)
    
    root.mainloop()

main()
