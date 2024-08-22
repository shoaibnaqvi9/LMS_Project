from tkinter import *
from tkinter import messagebox
import pypyodbc as odbc
from datetime import datetime
import index_dashboard

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

def new_admin_signup(conn, FirstName, LastName, Email, Phone, Password, LibrariansAdmissionDate):
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Librarians (FirstName, LastName, Email, Phone, Password, LibrariansAdmissionDate)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (FirstName, LastName, Email, Phone, Password, LibrariansAdmissionDate))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Success", "Librarian added successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def add_admin():
    try:
        if Password.get() != ConfirmPassword.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return

        LibrariansAdmissionDate = datetime.now()
        new_admin_signup(conn, FirstName.get(), LastName.get(), Email.get(), Phone.get(), Password.get(), LibrariansAdmissionDate)
    except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def login(conn, email, password):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM Librarians WHERE Email = ? AND Password = ?"
        cursor.execute(query, (email.get(),password.get()))
        row = cursor.fetchone()
        
        if row is not None:
            messagebox.showinfo("Success", "Login successful")
            root.destroy()
            index_dashboard.start_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()

def exit_program():
    try:
        if conn is not None:
            conn.close()
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while closing the program: {str(e)}")
conn = None
def admin_login():
    global root, conn, email, password
    conn = get_connection()
    try:
        root = Tk()
        root.geometry("450x250")
        root.title("Library Management System - Admin Login")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)
        root.configure(bg="#2c3e50")

        header_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        entry_bg = "#ecf0f1"
        entry_fg = "#2c3e50"
        button_bg = "#3498db"
        button_fg = "white"
        button_font = ("Arial", 10, "bold")

        Label(root, text="Admin Login", font=header_font, bg="#2c3e50", fg="white").grid(row=0, columnspan=3, pady=10)
        Label(root, text="Email Address", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=1, column=0, sticky=W, padx=10, pady=10)
        Label(root, text="Password", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=2, column=0, sticky=W, padx=10, pady=10)
        
        email = Entry(root, bg=entry_bg, fg=entry_fg)
        password = Entry(root, show="*", bg=entry_bg, fg=entry_fg)
        
        email.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        password.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        
        Button(root, text='Login', fg=button_fg, bg=button_bg, font=button_font, width='10', command=lambda: login(conn, email, password)).grid(row=3, column=0, padx=10, pady=20, sticky=W)
        Button(root, text='Signup', fg=button_fg, bg=button_bg, font=button_font, width='10', command=admin_signup).grid(row=3, column=1, padx=10, pady=20, sticky=W)
        Button(root, text='Exit', fg=button_fg, bg=button_bg, font=button_font, width='10', command=exit_program).grid(row=3, column=2, padx=10, pady=20, sticky=E)
        
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred during initialization: {str(e)}")

def admin_signup():
    global root, conn, FirstName, LastName, Email, Phone, Password, ConfirmPassword
    conn = get_connection()
    try:
        root = Tk()
        root.geometry("450x350")
        root.title("Library Management System - Admin Signup")
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)
        root.configure(bg="#2c3e50")

        header_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        entry_bg = "#ecf0f1"
        entry_fg = "#2c3e50"
        button_bg = "#3498db"
        button_fg = "white"
        button_font = ("Arial", 10, "bold")

        Label(root, text="Admin Signup", font=header_font, bg="#2c3e50", fg="white").grid(row=0, columnspan=2, pady=10)
        Label(root, text="First Name:", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Label(root, text="Last Name:", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Label(root, text="Email:", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=3, column=0, sticky=W, padx=10, pady=5)
        Label(root, text="Phone:", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=4, column=0, sticky=W, padx=10, pady=5)
        Label(root, text="Password:", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=5, column=0, sticky=W, padx=10, pady=5)
        Label(root, text="Confirm Password:", font=label_font, bg="#2c3e50", fg="white", anchor="w").grid(row=6, column=0, sticky=W, padx=10, pady=5)

        FirstName = Entry(root, bg=entry_bg, fg=entry_fg)
        LastName = Entry(root, bg=entry_bg, fg=entry_fg)
        Email = Entry(root, bg=entry_bg, fg=entry_fg)
        Phone = Entry(root, bg=entry_bg, fg=entry_fg)
        Password = Entry(root, show="*", bg=entry_bg, fg=entry_fg)
        ConfirmPassword = Entry(root, show="*", bg=entry_bg, fg=entry_fg)

        FirstName.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        LastName.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        Email.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        Phone.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        Password.grid(row=5, column=1, padx=10, pady=5, sticky=W)
        ConfirmPassword.grid(row=6, column=1, padx=10, pady=5, sticky=W)

        Button(root, text='Register', fg=button_fg, bg=button_bg, font=button_font, width=10, command=add_admin).grid(row=7, column=0, padx=10, pady=20, sticky=W)
        Button(root, text='Login', fg=button_fg, bg=button_bg, font=button_font, width=10, command=admin_login).grid(row=7, column=1, padx=10, pady=20, sticky=W)
        Button(root, text='Exit', fg=button_fg, bg=button_bg, font=button_font, width=10, command=exit_program).grid(row=7, column=2, padx=10, pady=20, sticky=E)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred during initialization: {str(e)}")
admin_login()
