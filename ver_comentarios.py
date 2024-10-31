import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Comentarios(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="gray60", height=700, width=1350)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.inicio()

    def inicio(self):
        # Crear el buscador
        self.search_label = tk.Label(root, text="Buscar Proyecto:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(root)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(root, text="Buscar", command=self.buscar_proyecto)
        self.search_button.pack(pady=5)

        # Crear la tabla
        self.tree = ttk.Treeview(root, columns=("Proyecto", "Comentario"), show='headings')
        self.tree.heading("Proyecto", text="Proyecto")
        self.tree.heading("Comentario", text="Comentario")
        self.tree.pack(pady=20)

        # Botón para ver comentario completo
        self.view_button = tk.Button(root, text="Ver Comentario Completo", command=self.ver_comentario_completo)
        self.view_button.pack(pady=5)

        # Conectar a la base de datos
        self.conn = sqlite3.connect('bd.sql')
        self.cursor = self.conn.cursor()

    def buscar_proyecto(self):
        proyecto = self.search_entry.get()
        self.cursor.execute("SELECT proyecto, comentario FROM comentarios WHERE proyecto LIKE ?", ('%' + proyecto + '%',))
        rows = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def ver_comentario_completo(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un comentario.")
            return
        comentario = self.tree.item(selected_item, 'values')[1]
        self.mostrar_ventana_comentario(comentario)

    def mostrar_ventana_comentario(self, comentario):
        top = tk.Toplevel(self.root)
        top.title("Comentario Completo")
        text = tk.Text(top, wrap='word')
        text.insert(tk.END, comentario)
        text.pack(expand=True, fill='both')

ventana = Tk()
ventana.title("Comentarios dejados")
ventana.resizable(False,False)
ventana.geometry("+0+0")
root = Comentarios(ventana)
ventana.mainloop()