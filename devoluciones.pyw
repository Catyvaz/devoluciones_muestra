from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from conexion import obtener_conexion

class DEVOLUCION(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="gray60", height=700, width=1350)
        self.master = master
        self.pack_propagate(False)
        self.pack(expand=True)
        self.inicio()
        # Sobrescribe el protocolo de cierre de la ventana
        #self.master.protocol("WM_DELETE_WINDOW", lambda: None)

    def inicio(self):
        self.contenedor = Frame(self, bg="PeachPuff3")
        self.contenedor.pack(expand=True, fill="y")

        self.cont_texto=Frame(self.contenedor, bg="PeachPuff3", height=400, width=1200)
        self.cont_texto.pack(expand=True)

        Label(self.cont_texto, text="¡Gracias por venir!", font=("Arial", 25), bg="PeachPuff3").pack(pady=20)

        self.cont_devolucion=Frame(self.contenedor, bg="PeachPuff3", height=200, width=1200)
        self.cont_devolucion.pack(expand=True)

        cont_desplegable = Frame(self.cont_devolucion, bg="PeachPuff3", height=100, width=1200)
        cont_desplegable.pack(expand=True)
        Label(cont_desplegable, text="Proyecto: ", font=("Arial", 13), bg="PeachPuff3").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.proyectos = ttk.Combobox(cont_desplegable, state="readonly", width=50)
        self.proyectos.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        cont_desplegable.columnconfigure(2, weight=1)

        Label(self.cont_devolucion, text="Devolución: ", font=("Arial", 12), bg="PeachPuff3").pack(pady=10)
        self.texto = Text(self.cont_devolucion, height=5, width=60, wrap='word', font=("Robot", 12))
        self.texto.pack(padx=10) 

        self.cont_interesados=Frame(self.contenedor, bg="PeachPuff3", height=200, width=1200)
        self.cont_interesados.pack(expand=True)

ventana = Tk()
ventana.title("Devoluciones")
ventana.resizable(False,False)
ventana.geometry("+0+0")
root = DEVOLUCION(ventana)
ventana.mainloop()