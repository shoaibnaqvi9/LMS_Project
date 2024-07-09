from tkinter import *
import pandas as pd
import pypyodbc as odbc

DRIVER_NAME="SQL SERVER"
SERVER_NAME="DESKTOP-OFOE4B8\SQLEXPRESS"
DATABASE_NAME="library"
connection_string=f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={{{DATABASE_NAME}}};
    Trust_Connection=yes;
"""
conn=odbc.connect(connection_string)
print(conn)

