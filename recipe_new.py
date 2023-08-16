import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter import  StringVar, ttk
from tkinter import messagebox
from tkcalendar import DateEntry 
from datetime import datetime
from PIL import  Image
import os.path
import json
import shutil

class Recipe(ttk.Frame):
    """Clase que representa una funcion para crear recetas"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.ruta_archivo = None
        self.grid(sticky=(tk.N, tk.S, tk.E, tk.W))
        self.parent.geometry("785x580+100+100")
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        self.recetas = []
        self.parent.title("Receta nueva")

        
        """Variable para usar campos de frame"""
        campos_frame = ttk.Frame(self)
        campos_frame.grid()
        
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        
        
        """Variable para insertar imagen"""
        self.path_imagen = StringVar()
        
        """Campo de nombre"""
        nombre_label = ttk.Label(campos_frame, text="Nombre:", font="Georgia", foreground="#ADADD8")
        nombre_label.grid(row=0, column=0, padx=5, pady=5,  sticky=tk.W)

        self.nombre_entry = ttk.Entry(campos_frame, width=50)
        self.nombre_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        
        """Campo de ingredientes"""
        ingredientes_label = ttk.Label(campos_frame, text="Ingredientes:", font="Georgia", foreground="#ADADD8")
        ingredientes_label.grid(row=1, column=0, padx=5, pady=5,  sticky=tk.W)

        self.ingredientes_entry = tk.Text(campos_frame, height=10, width=50)
        self.ingredientes_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        self.ingredientes_entry.configure(bg="#212121", fg="#F5F5F5")
        
        """Campo de preparacion"""
        preparacion_label = ttk.Label(campos_frame, text="Preparacion:", font="Georgia", foreground="#ADADD8")
        preparacion_label.grid(row=2, column=0, padx=5, pady=5,  sticky=tk.W)
       

        self.preparacion_entry = tk.Text(campos_frame, height=10, width=50)
        self.preparacion_entry.configure(bg="#212121", fg="#F5F5F5")
        self.preparacion_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5,  sticky=tk.W)
        
        """Campo de tiempo de preparacion"""
        tiempo_prep_label = ttk.Label(campos_frame, text="Tiempo de preparacion (en minutos):",font="Georgia", foreground="#ADADD8")
        tiempo_prep_label.grid(row=3, column=0, padx=5, pady=5,  sticky=tk.W)

        self.tiempo_prep_entry = ttk.Entry(campos_frame, width=50)
        self.tiempo_prep_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        
        """Campo de tiempo de coccion"""
        tiempo_cocc_label = ttk.Label(campos_frame, text="Tiempo de coccion (en minutos):", font="Georgia", foreground="#ADADD8")
        tiempo_cocc_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        self.tiempo_cocc_entry = ttk.Entry(campos_frame, width=50)
        self.tiempo_cocc_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        
        """Campo de fecha"""
        fecha_label = ttk.Label(campos_frame, text="Fecha:", font="Georgia", foreground="#ADADD8")
        fecha_label.grid(row=5, column=0, padx=5, pady=5,  sticky=tk.W)
       
        self.fecha_frame = tk.Frame(self.parent)
        self.fecha_frame.grid(row=0, column=0, padx=5, pady=5)
        
        self.fecha_entry = DateEntry(campos_frame, width=50, date_pattern='dd/mm/yyyy')
        self.fecha_entry.grid(row=5,column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)

        """Campo de etiquetas"""
        etiquetas_label = ttk.Label(campos_frame, text="Etiquetas (separadas por coma):", font="Georgia", foreground="#ADADD8")
        etiquetas_label.grid(row=6, column=0, padx=5, pady=5,  sticky=tk.W)

        self.etiquetas_entry = ttk.Entry(campos_frame, width=50)
        self.etiquetas_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        
        """Campo de imagen"""
        
        self.text_imagen= ttk.Label(campos_frame, text="URL de la imagen: ", font="Georgia", foreground="#ADADD8")
        self.text_imagen.grid(row=7, column=0, columnspan=3, padx=5, pady=5,  sticky=tk.W)
        
        self.url_imagen= ttk.Label(campos_frame, textvariable=self.path_imagen).grid(row=7, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
    
        """Variable para usar campos de frame"""
        btn_frame = ttk.Frame(self)
        btn_frame.grid()
        
        """Crear boton para guardar"""
        guardar_receta_btn = ttk.Button(btn_frame,text="Crear receta", command= self.guardar_receta)
        guardar_receta_btn.grid(row=8, column=2, columnspan=2)
        
        """Crear boton para cancelar"""
        cancelar_receta = ttk.Button(btn_frame, text="Cancelar", command=self.parent.destroy)
        cancelar_receta.grid(row=8, column=4, columnspan=2)
        
        """Crear boton para cargar imagenes"""
        cargar_imagen = ttk.Button(btn_frame, text="Cargar imagen", command=self.cargar_imagen)
        cargar_imagen.grid(row=8, column=6, columnspan=2)
        
    
    def cargar_imagen(self):
        """Funcion para cargar imagenes"""
        tipos = (('Archivos de texto', '*.jpg'),
                 ('Todos los archivos', '*.*'))
        self.ruta_archivo = askopenfilename(filetypes=tipos)
        if self.ruta_archivo:
             self.path_imagen.set(self.ruta_archivo)
             self.imagen_receta = self.ruta_archivo
    
    def guardar_receta(self):
        """Funcion para crear una receta"""
        fecha = self.fecha_entry.get_date()
        """Primero entra la fecha como un DateEntry con calendary y despues lo formateo como str usando datetime"""
        fecha_str = datetime.strftime(fecha, "%d/%m/%Y")
        
        """dict de las recetas que se iran creando"""
        nueva_receta = {
            
            "nombre": self.nombre_entry.get(),
            "fecha": fecha_str,
            "preparacion": self.preparacion_entry.get("1.0", "end-1c"),
            "tiempo_prep": self.tiempo_prep_entry.get(),
            "tiempo_cocc": self.tiempo_cocc_entry.get(),
            "ingredientes": self.ingredientes_entry.get("1.0", "end-1c"),
            "etiquetas": self.etiquetas_entry.get().split(","),
            "imagen": None
        }
        
        
        if not nueva_receta["nombre"] or not nueva_receta["ingredientes"] or not nueva_receta["preparacion"] or not nueva_receta["tiempo_prep"] or not nueva_receta["tiempo_cocc"] or not nueva_receta["fecha"] or not nueva_receta["etiquetas"]:
            """Si no esta completa todas las casillas saldra un mensaje de advertencia"""
            messagebox.showwarning("Campos incompletos", "Debe completar todas las casillas.")
            return
        
        try:
            """Si no se ingresa con numero entero saldra un mensaje de error"""
            tiempo_prep = int(self.tiempo_prep_entry.get())
            tiempo_cocc = int(self.tiempo_cocc_entry.get())
        
        except ValueError:
            messagebox.showwarning("Error", "El tiempo de preparación y cocción deben ser números enteros.")
            return  
        if not self.etiquetas_entry.get():
            """Si la casilla de etiquetas está vacía, se muestra un mensaje de advertencia"""
            messagebox.showwarning("Campos incompletos", "Debe ingresar al menos una etiqueta.")
            return
        
        
        if self.ruta_archivo is not None:
            nombre_imagen = nueva_receta["nombre"].lower().replace(" ", "_") + ".jpg"
            carpeta_imagenes = "imagenes"
            if not os.path.exists(carpeta_imagenes):
                os.makedirs(carpeta_imagenes)
            ruta_destino = os.path.join(carpeta_imagenes, nombre_imagen)
            shutil.copy(self.ruta_archivo, ruta_destino)
            with Image.open(self.ruta_archivo) as imagen:
                nueva_receta["imagen"] = ruta_destino

        
        
        if os.path.exists("recetas.json"):
            """Si el archivo ya existe, se carga su contenido en self.recetas"""
            with open("recetas.json", "r") as archivo:
                self.recetas = json.load(archivo)
        else:
            """Si el archivo no existe, se crea una lista vacía"""
            self.recetas = []
        
            
        self.recetas.append(nueva_receta)
        """Se agrega las recetas creadas al diccionario"""
        
        with open("recetas.json", "w") as archivo:
            json.dump(self.recetas, archivo)
    
        
        """Se limpia todas las casillas al terminar de crear"""
        self.nombre_entry.delete(0, tk.END)
        self.ingredientes_entry.delete("1.0",tk.END)
        self.preparacion_entry.delete("1.0",tk.END)
        self.tiempo_prep_entry.delete(0, tk.END)
        self.tiempo_cocc_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.etiquetas_entry.delete(0, tk.END)
        self.path_imagen.set("")
        
        """Se muestra un mensaje informando que se creo la receta"""
        messagebox.showinfo("Receta creada", "La receta ha sido creada exitosamente.")
        self.grid_forget()
        