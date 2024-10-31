from tkinter import *
from tkinter import messagebox, Radiobutton
from tkinter import ttk
from conexion import obtener_conexion
import mysql.connector

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
        self.contenedor = Frame(self, bg="LavenderBlush3", width= 1100)
        self.contenedor.pack_propagate(False)
        self.contenedor.pack(expand=True, fill="y", pady= 20)

        #TEXTO DEL INICIO
        self.cont_texto=Frame(self.contenedor, bg="LavenderBlush3", height=180, width=1200)
        self.cont_texto.pack(expand=True)

        Label(self.cont_texto, text="¡Gracias por venir!", font=("Arial", 30), bg="LavenderBlush3").pack()

        #donde esta el desplegable de proyectos y el long text para poner la devolucion
        self.cont_devolucion=Frame(self.contenedor, bg="LavenderBlush3", width=1200)
        self.cont_devolucion.pack(expand=True, fill = "x", padx= 180)
        self.datos_comentario = {}

        cont_desplegable = Frame(self.cont_devolucion, bg="LavenderBlush3")
        cont_desplegable.pack(expand=True, fill="x")
        style = ttk.Style()
        style.theme_use("default")
        style.map("Custom.TCombobox",  fieldbackground=[("active", "white")],   # Fondo blanco en modo de solo lectura
                                        background=[("active", "white")],          # Fondo blanco al desplegar el menú
                                        selectbackground=[("focus", "white")],     # Fondo blanco cuando una opción está seleccionada
                                        selectforeground=[("focus", "black")])
        Label(cont_desplegable, text="Proyecto: ", font=("Arial", 13), bg="LavenderBlush3",).grid(row=0, column=0, padx=10, sticky="w")
        self.proyectos = ttk.Combobox(cont_desplegable, state="readonly", width=50, font=("Arial", 13), style="Custom.TCombobox")
        self.proyectos["values"] = ["Todos", "Recupero de Obras sociales", "Peluquería", "Libreria", "Parrilla", "Liga de Handball", "Inscripción"]
        self.proyectos.current(0)
        self.proyectos.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.datos_comentario["proyecto"] = self.proyectos.get()
        cont_desplegable.columnconfigure(2, weight=1)

        Label(self.cont_devolucion, text="Devolución: ", font=("Arial", 13), bg="LavenderBlush3").pack(pady=5, padx=10, anchor="w")
        self.texto = Text(self.cont_devolucion, height=10, width=80, wrap='word', font=("Robot", 12))
        self.texto.pack(padx=10, anchor="w") 

        self.contador_label = Label(self.cont_devolucion, text="0/750 caracteres", font=("Arial", 10), bg="LavenderBlush3")
        self.contador_label.pack(pady=5, anchor="e", padx=10)
        # Vincular el evento KeyRelease al método limitar_texto
        self.texto.bind("<KeyRelease>", self.limitar_texto)
        self.datos_comentario["comentario"] = self.texto.get("1.0", "end-1c")

        #pregunta de interes, campos ingresados 
        self.cont_interesados=Frame(self.contenedor, bg="LavenderBlush3", width=1200)
        self.cont_interesados.pack(expand=True)

        contenedor_pregunta = Frame(self.cont_interesados, bg="LavenderBlush3")
        contenedor_pregunta.pack(expand=True, fill="x", ipady=20)
        Label(contenedor_pregunta, text="¿Interesado en ser estudiante de ISAUI?", font=("Arial", 14), bg="LavenderBlush3").grid(row=0, column=0, padx=10, sticky="w")
        self.respuesta = StringVar()
        self.respuesta.set(1)
        self.respuesta.trace("w", self.actualizar_estado_campos)
        Radiobutton(contenedor_pregunta, text="Sí", variable=self.respuesta, value=1, bg="LavenderBlush3", font=("Arial", 13)).grid(row=0, column=1, sticky="w")
        Radiobutton(contenedor_pregunta, text="No", variable=self.respuesta, value=2, bg="LavenderBlush3", font=("Arial", 13)).grid(row=0, column=2, sticky="w")

        #campos para poner los datos del interesado
        cont_campos = Frame(self.cont_interesados, bg="LavenderBlush3", height=100, width=1200)
        cont_campos.pack(expand=True, fill="x")
        campos_arriba = ["Nombre", "Apellido"]
        campos_abajo = ["Correo", "Carrera"]
        self.entradas = {}

        for i, campo in enumerate(campos_arriba):
            Label(cont_campos, text=campo, font=("Arial", 13), bg="LavenderBlush3").grid(row=1, column=i, padx=10, pady=5, sticky="w")
            self.entradas[campo] = Entry(cont_campos, font=("Arial", 12), width=30)
            self.entradas[campo].grid(row=2, column=i, padx=10, pady=5, sticky="w")
        for j, campo in enumerate(campos_abajo):
            Label(cont_campos, text=campo, font=("Arial", 13), bg="LavenderBlush3").grid(row=3, column=j, padx=10, pady=5, sticky="w")
            if campo == "Carrera":
                self.entradas[campo] = ttk.Combobox(cont_campos, state="readonly", width=29, font=("Arial", 12))
                self.entradas[campo]["values"] = ["Varias", "Desarrollo de Software", "Enfermería", "Diseño de Espacios", "Guía en Turismo", "Guía de Turismo y Hotelería", "Guía de Trekking y Guía de montaña"]
                self.entradas[campo].current(0)
                self.entradas[campo].grid(row=4, column=j, padx=10, pady=5, sticky="w")
            else:
                self.entradas[campo] = Entry(cont_campos, font=("Arial", 12), width=30)
                self.entradas[campo].grid(row=4, column=j, padx=10, pady=5, sticky="w")

        self.actualizar_estado_campos()
        
        #botones de guardar y cancelar
        contenedor_botones = Frame(self.contenedor, bg="LavenderBlush3")
        contenedor_botones.pack(pady=20)

        btn_guardar = Button(contenedor_botones, text="Guardar", font=("Arial", 15), bg="LightSteelBlue3", width=15, command=self.guardar)
        btn_guardar.grid(row=0, column=1, padx= 20)

        btn_cancelar = Button(contenedor_botones, text="Cancelar", font=("Arial", 15), bg="LightSteelBlue3", width=15, command=self.cancelar)
        btn_cancelar.grid(row=0, column=2, padx= 20)

    def limitar_texto(self, event= None):
        contenido = self.texto.get("1.0", "end-1c")
        if len(contenido) > 750:
            self.texto.delete("1.0", "end")
            self.texto.insert("1.0", contenido[:750])
        # Actualizar el contador de caracteres
        self.contador_label.config(text=f"{len(contenido)}/750 caracteres")
            
    def cancelar(self):
        self.proyectos.current(0)
        self.respuesta.set(1)
        self.texto.delete("1.0", "end")
        self.contador_label.config(text="0/750 caracteres")
        for campo in self.entradas:
            self.entradas[campo].delete(0, END)
    
    def guardar(self):
        envio = False
        conexion = obtener_conexion()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        
        proyecto = (self.datos_comentario["proyecto"]).upper()
        comentario = self.texto.get("1.0", "end-1c").upper()
        
        if len(comentario) > 0:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO comentario (proyecto, comentario) VALUES (%s, %s)"
                val = (proyecto, comentario)
                cursor.execute(sql, val)
                conexion.commit()
                cursor.close()
                conexion.close()
                messagebox.showinfo("Información", "Comentario agregado exitosamente")
                envio = True
            except mysql.connector.Error as error:
                    messagebox.showerror("Error", f"No se pudo agregar el comentario: {error}")
                    self.ventana_agregar.lift()
        else:
            pass
        
        if self.respuesta.get() == '1':
            nombre = self.entradas["Nombre"].get().upper()
            apellido = self.entradas["Apellido"].get().upper()
            correo = self.entradas["Correo"].get().upper
            carrera = self.entradas["Carrera"].get().upper
            print(nombre, apellido, correo, carrera)
            if nombre and apellido and correo and carrera:
                conexion = obtener_conexion()
                try:
                    cursor = conexion.cursor()
                    sql = "INSERT INTO ingresante (nombre, apellido, correo, carrera) VALUES (%s, %s, %s, %s)"
                    val = (nombre, apellido, correo, carrera)
                    cursor.execute(sql, val)
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    nombre.capitalize()
                    messagebox.showinfo("Información", "{nombre} agregado exitosamente")
                    envio = True
                except mysql.connector.Error as error:
                    messagebox.showerror("Error", f"No se pudo guardar el ingresante: {error}")
                    self.ventana_agregar.lift()
            else:
                messagebox.showerror("Error", "Los campos nombre, apellido, correo y carrera son obligatorios, complete los campos faltantes")
        if envio == False:
            messagebox.showerror("Error", "No se puede guardar la información, revise los campos")
        self.cancelar()

    def actualizar_estado_campos(self, *args):
        campos_arriba = ["Nombre", "Apellido"]
        campos_abajo = ["Correo", "Carrera"]
        if self.respuesta.get() == '1':
            for campo in campos_arriba + campos_abajo:
                self.entradas[campo].config(state="normal")
        elif self.respuesta.get() == '2':
            for campo in campos_arriba + campos_abajo:
                self.entradas[campo].config(state="disabled")

ventana = Tk()
ventana.title("Devoluciones")
ventana.resizable(False,False)
ventana.geometry("+0+0")
root = DEVOLUCION(ventana)
ventana.mainloop()