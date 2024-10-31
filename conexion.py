import mysql.connector
from tkinter import messagebox

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
                host="localhost",
                user="root", 
                password="", 
                database="devolucion_muestra")
        print("Conexión exitosa")
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None