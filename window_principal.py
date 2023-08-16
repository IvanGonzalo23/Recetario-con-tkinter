import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
from PIL import ImageTk, Image
import os
import json
import random
from recipe_new import Recipe
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatchdogHandler(FileSystemEventHandler):
    """Clase que activa el modulo watchdog"""

    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        """funcion que empieza el monitoreo de cambios que sufrira el json"""
        if event.src_path.endswith(".json"):
            self.app.cargar_recetas()


class Recetario(ttk.Frame):
    """Clase que representa un recetario de cocina mediante el uso de tkinter"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.config(bg="gray18")
        self.parent.title("Recetario de Cocina")
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.geometry("1450x500+100+100")
        self.recetas = []
        self.crear_widgets()
        self.imagen_tk = None

        self.iniciar_watchdog()
        self.agregar_tema_awdark(self.parent)

    def crear_widgets(self):
        """Funcion que crea widgets"""
        btn_frame = ttk.Frame(root)
        btn_frame.grid(row=1, column=0)

        """Crear los botones"""
        crear_boton = ttk.Button(btn_frame, text="Crear receta", command=self.abrir)
        crear_boton.grid(row=0, column=0, columnspan=2)
        modificar_boton = ttk.Button(
            btn_frame, text="Modificar receta", command=self.modificar_receta
        )
        modificar_boton.grid(row=0, column=2, columnspan=2)

        eliminar_boton = ttk.Button(
            btn_frame, text="Eliminar receta", command=self.eliminar_receta
        )
        eliminar_boton.grid(row=0, column=4, columnspan=2)

        buscar_boton = ttk.Button(
            btn_frame, text="Buscar receta", command=self.buscar_receta
        )
        buscar_boton.grid(row=0, column=6, columnspan=2)

        receta_del_dia_boton = ttk.Button(
            btn_frame, text="Receta del dia", command=self.mostrar_receta_del_dia
        )
        receta_del_dia_boton.grid(row=0, column=8, columnspan=2)

        cargar_recetas = ttk.Button(
            btn_frame, text="Cargar archivo", command=self.cargar_archivo_json
        )
        cargar_recetas.grid(row=0, column=10, columnspan=2)

        """Crear el frame del Treeview"""
        treeview_frame = ttk.Frame(root)
        treeview_frame.grid(row=0, column=0, pady=5, sticky="nsew")

        """Crear el marco del treeview"""

        treeview_frame_inner = ttk.Frame(root, borderwidth=20, relief="ridge")
        treeview_frame_inner.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        """Crear el Treeview"""

        columns = (
            "nombre",
            "fecha",
            "preparacion",
            "tiempo de preparacion",
            "tiempo de coccion",
            "ingredientes",
            "etiquetas",
            "imagen",
        )

        self.treeview = ttk.Treeview(
            treeview_frame_inner, columns=columns, show="headings"
        )

        """Crear sus columnas"""
        self.treeview.column("nombre", width=100)
        self.treeview.column("fecha", width=100)
        self.treeview.column("preparacion", width=80)
        self.treeview.column("tiempo de preparacion", width=50)
        self.treeview.column("tiempo de coccion", width=50)
        self.treeview.column("ingredientes", width=100)
        self.treeview.column("etiquetas", width=80)
        self.treeview.column("imagen", width=100)

        """Crear sus headings"""
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("fecha", text="Fecha")
        self.treeview.heading("preparacion", text="Preparacion")
        self.treeview.heading("tiempo de preparacion", text="Tiempo de preparacion")
        self.treeview.heading("tiempo de coccion", text="Tiempo de coccion")
        self.treeview.heading("ingredientes", text="Ingredientes")
        self.treeview.heading("etiquetas", text="Etiquetas")
        self.treeview.heading("imagen", text="imagen")

        """Crear su scrollbar"""
        scrollbar = ttk.Scrollbar(treeview_frame_inner, orient="vertical")
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.treeview.yview)

        """Ubicar Treeview y scrollbar"""
        self.treeview.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        treeview_frame_inner.grid_rowconfigure(0, weight=1)
        treeview_frame_inner.grid_columnconfigure(0, weight=1)

        """Condicion de que si se hace doble click se abra una ventana con la infromacion de la receta"""
        self.treeview.bind("<Double-1>", self.crear_ventana_receta)
        self.cargar_recetas()

    def abrir(self):
        """Funcion para abrir el modulo recipe_new para crear una receta"""
        recipe_window = tk.Toplevel(self.parent)
        recipe_app = Recipe(recipe_window)
        recipe_window.update_idletasks()
        width = recipe_window.winfo_width()
        height = recipe_window.winfo_height()
        x = (recipe_window.winfo_screenwidth() // 2) - (width // 2) - 132
        y = (recipe_window.winfo_screenheight() // 2) - (height // 2) - 75
        recipe_window.geometry("{}x{}+{}+{}".format(width, height, x, y))
        recipe_app.grid()

    def crear_ventana_receta(self, event):
        """Función para crear una ventana secundaria y mostrar la información completa de una receta"""
        """ Obtener la fila que se ha seleccionado con el doble clic"""
        item = self.treeview.selection()

        """Obtener la información completa de la receta"""
        (
            nombre,
            fecha,
            preparacion,
            tiempo_prep,
            tiempo_cocc,
            ingredientes,
            etiquetas,
            ruta_archivo,
        ) = self.treeview.item(item, "values")

        ventana_receta = tk.Toplevel(self)
        ventana_receta.title(nombre)
        ventana_receta.configure(background="#282C34")

        """Agregar los widgets necesarios a la ventana"""
        tk.Label(ventana_receta, text="Nombre: ").grid(row=0, column=0, sticky="w")
        tk.Label(ventana_receta, text=nombre).grid(row=0, column=1, sticky="w")
        tk.Label(ventana_receta, text="Fecha: ").grid(row=1, column=0, sticky="w")
        tk.Label(ventana_receta, text=fecha).grid(row=1, column=1, sticky="w")
        tk.Label(ventana_receta, text="Tiempo de preparación: ").grid(
            row=2, column=0, sticky="w"
        )
        tk.Label(ventana_receta, text=tiempo_prep + " minutos").grid(
            row=2, column=1, sticky="w"
        )
        tk.Label(ventana_receta, text="Tiempo de cocción: ").grid(
            row=3, column=0, sticky="w"
        )
        tk.Label(ventana_receta, text=tiempo_cocc + " minutos").grid(
            row=3, column=1, sticky="w"
        )

        tk.Label(ventana_receta, text="Ingredientes:").grid(row=4, column=0, sticky="w")
        texto_ingredientes = tk.Text(ventana_receta, width=50, height=10)
        texto_ingredientes.grid(row=5, column=0, columnspan=2, sticky="w")
        texto_ingredientes.insert("end", ingredientes)

        tk.Label(ventana_receta, text="Preparación:").grid(row=6, column=0, sticky="w")

        texto_preparacion = tk.Text(ventana_receta, width=50, height=10)
        texto_preparacion.grid(row=8, column=0, columnspan=2, sticky="w")
        texto_preparacion.insert("end", preparacion)

        tk.Label(ventana_receta, text="Etiquetas:").grid(row=12, column=0, sticky="w")
        tk.Label(ventana_receta, text=etiquetas).grid(row=12, column=1, sticky="w")

        self.aplicar_estilo(ventana_receta)

        """Condicion de que si encuentra una imagen que no sea compatible por la libreria tkinter
       la convierta para que sea adaptable a la libreria"""
        if ruta_archivo:
            try:
                imagen = Image.open(ruta_archivo).convert("RGBA")
                imagen = imagen.resize((200, 200), resample=Image.Resampling.LANCZOS)
                self.imagen_tk = ImageTk.PhotoImage(imagen)
                tk.Label(ventana_receta, image=self.imagen_tk).grid(
                    row=0, column=2, rowspan=9
                )
                tk.Label(ventana_receta, text="Imagen de la receta").grid(
                    row=14, column=2
                )
                self.aplicar_estilo(ventana_receta)
            except Exception as e:
                print("Error al abrir la imagen:", e)

    def aplicar_estilo(self, widget):
        """Funcion que aplica cierto estilo a los widgets"""
        # Aplicar estilo a los widgets de tipo Label
        if isinstance(widget, tk.Label):
            widget.config(bg="#272727", fg="white", font="Helvetica 10")
        # Aplicar estilo a los widgets de tipo Button
        elif isinstance(widget, tk.Button):
            widget.config(
                bg="#272727",
                fg="white",
                font="Helvetica 10",
                activebackground="#2d2d2d",
            )
        # Aplicar estilo a los widgets de tipo Entry y Text
        elif isinstance(widget, (tk.Entry, tk.Text)):
            widget.config(
                bg="#383838", fg="white", insertbackground="white", font="Helvetica 10"
            )
        # Aplicar estilo a los widgets de tipo Checkbutton y Radiobutton
        elif isinstance(widget, (tk.Checkbutton, tk.Radiobutton)):
            widget.config(bg="#272727", fg="white", font="Helvetica 10")
        # Recorrer los hijos del widget actual para aplicar el estilo a cada uno de ellos
        for child in widget.winfo_children():
            self.aplicar_estilo(child)

    def agregar_tema_awdark(self, ventana):
        """Funcion que agrega el theme de la ventana"""
        ventana.tk.call("lappend", "auto_path", "./themas")
        ventana.tk.call("package", "require", "awdark")
        estilo = ttk.Style(ventana)
        estilo.theme_use("awdark")

    def iniciar_watchdog(self):
        """Funcion que comienza la observacion del json"""
        event_handler = WatchdogHandler(self)
        observer = Observer()
        observer.schedule(
            event_handler,
            os.path.dirname(os.path.abspath("recetas.json")),
            recursive=False,
        )
        observer.start()

    def cargar_archivo_json(self):
        """Funcion que permite cargar archivos json con otras recetas"""
        ruta_archivo = filedialog.askopenfilename(
            defaultextension=".json", filetypes=[("Archivo JSON", "*.json")]
        )
        if ruta_archivo:
            with open(ruta_archivo, "r") as archivo:
                contenido = archivo.read()
            try:
                recetas = json.loads(contenido)
                self.recetas = recetas
                for i in self.treeview.get_children():
                    self.treeview.delete(i)
                for receta in self.recetas:
                    # Obtener la ruta completa a la imagen si existe
                    imagen = receta.get("imagen", None)
                    if imagen is not None:
                        imagen = os.path.join(os.path.dirname(ruta_archivo), imagen)

                        if not os.path.isfile(imagen):
                            print(f"Error al abrir la imagen: {imagen}")
                            continue
                    self.treeview.insert(
                        parent="",
                        index="end",
                        values=(
                            receta["nombre"],
                            receta["fecha"],
                            receta["preparacion"],
                            receta["tiempo_prep"],
                            receta["tiempo_cocc"],
                            receta["ingredientes"],
                            ", ".join(receta["etiquetas"]),
                            imagen,
                        ),
                    )
                """Configurar doble clic en el Treeview para mostrar información completa de la receta"""
                self.treeview.bind("<Double-1>", self.crear_ventana_receta)
            except ValueError:
                messagebox.showerror(
                    "Error", "El archivo no es un archivo JSON válido."
                )

    def cargar_recetas(self):
        """Función que permite cargar las recetas ya existentes del json y mostrarlas al iniciar el programa"""
        if os.path.exists("recetas.json"):
            """Si el archivo ya existe, se carga su contenido en self.recetas"""
            with open("recetas.json", "r") as archivo:
                self.recetas = json.load(archivo)
        else:
            """Si el archivo no existe, se crea una lista vacía"""
            self.recetas = []

        self.treeview.delete(
            *self.treeview.get_children()
        )  # borra todos los items del treeview antes de cargar las nuevas recetas
        for receta in self.recetas:
            # Si la receta no tiene imagen, se reemplaza el valor 'None' por un string vacío
            if not receta["imagen"]:
                receta["imagen"] = ""
            # Insertamos la receta en el Treeview
            self.treeview.insert(
                "",
                "end",
                text=receta["nombre"],
                values=(
                    receta["nombre"],
                    receta["fecha"],
                    receta["preparacion"],
                    receta["tiempo_prep"],
                    receta["tiempo_cocc"],
                    receta["ingredientes"],
                    receta["etiquetas"],
                    receta["imagen"],
                ),
            )

    def modificar_receta(self):
        """Funcion para modificar una receta seleccionada"""
        self.items_seleccionados = self.treeview.selection()
        """Sirve para poder seleccionar las recetas del treeview"""
        if not self.items_seleccionados:
            """Condicion, sirve para ver si se selecciono una receta o no"""
            messagebox.showwarning(
                "Error", "Por favor seleccione una receta para modificar."
            )
            """Si no se selecciono una receta sale un mensaje de error"""
            return

        """Al seleccionar toma los valores de la receta"""
        self.item_seleccionado = self.treeview.selection()[0]
        self.nombre_receta = self.treeview.item(self.item_seleccionado)["values"][0]
        """Se abre el json de manera de lectura"""
        with open("recetas.json", "r") as f:
            self.recetas = json.load(f)

        self.receta_seleccionada = next(
            (
                receta
                for receta in self.recetas
                if receta["nombre"] == self.nombre_receta
            ),
            None,
        )

        """Se recorre la lista de recetas para encontrar la receta seleccionada"""
        if not self.receta_seleccionada:
            """Si no se encuentra sale un mensaje de advertencia"""
            messagebox.showwarning("Error", "No se encontró la receta seleccionada.")
            return
        """Ventana secundaria para modificar la receta"""
        self.ventana_modificar = tk.Toplevel(self)
        self.ventana_modificar.title("Modificar Receta")
        self.ventana_modificar.configure(background="#282C34")
        """Crear campos de entrada para modificar la receta"""
        tk.Label(
            self.ventana_modificar,
            text="Nombre:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=0, column=0, sticky="w")
        self.nombre_entry1 = tk.Entry(
            self.ventana_modificar, bg="#272822", fg="#F8F8F2"
        )
        self.nombre_entry1.insert(0, self.receta_seleccionada["nombre"])
        self.nombre_entry1.grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(
            self.ventana_modificar,
            text="Fecha:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=1, column=0, sticky="w")
        self.fecha_entry1 = DateEntry(self.ventana_modificar)
        self.fecha_entry1.set_date(
            datetime.strptime(self.receta_seleccionada["fecha"], "%d/%m/%Y")
        )
        self.fecha_entry1.grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(
            self.ventana_modificar,
            text="Preparación:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=2, column=0, sticky="w")
        self.preparacion_entry1 = tk.Text(self.ventana_modificar, height=10)
        self.preparacion_entry1.insert("1.0", self.receta_seleccionada["preparacion"])
        self.preparacion_entry1.grid(row=2, column=1, sticky="w", padx=10)

        tk.Label(
            self.ventana_modificar,
            text="Tiempo de preparación:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=3, column=0, sticky="w")
        self.tiempo_prep_entry1 = tk.Entry(
            self.ventana_modificar, bg="#272822", fg="#F8F8F2"
        )
        self.tiempo_prep_entry1.insert(0, self.receta_seleccionada["tiempo_prep"])
        self.tiempo_prep_entry1.grid(row=3, column=1, sticky="w", padx=10)

        tk.Label(
            self.ventana_modificar,
            text="Tiempo de cocción:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=4, column=0, sticky="w")
        self.tiempo_cocc_entry1 = tk.Entry(
            self.ventana_modificar, bg="#272822", fg="#F8F8F2"
        )
        self.tiempo_cocc_entry1.insert(0, self.receta_seleccionada["tiempo_cocc"])
        self.tiempo_cocc_entry1.grid(row=4, column=1, sticky="w", padx=10)

        tk.Label(
            self.ventana_modificar,
            text="Ingredientes:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=5, column=0, sticky="w")
        self.ingredientes_entry1 = tk.Text(self.ventana_modificar, height=10)
        self.ingredientes_entry1.insert("1.0", self.receta_seleccionada["ingredientes"])
        self.ingredientes_entry1.grid(row=5, column=1, sticky="w", padx=10)

        tk.Label(
            self.ventana_modificar,
            text="Etiquetas:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=6, column=0, sticky="w")
        self.etiquetas_entry1 = tk.Entry(
            self.ventana_modificar, bg="#272822", fg="#F8F8F2"
        )
        self.etiquetas_entry1.insert(
            0, ", ".join(self.receta_seleccionada["etiquetas"])
        )
        self.etiquetas_entry1.grid(row=6, column=1, sticky="w", padx=10)
        self.imagen_entry1 = tk.Entry(self.ventana_modificar)

        if self.receta_seleccionada.get("imagen") is not None:
            self.imagen_entry1.insert(0, self.receta_seleccionada["imagen"])
        else:
            self.imagen_entry1.insert(0, "")

        """Boton para guardar la receta"""
        guardar_btn = tk.Button(
            self.ventana_modificar,
            text="Guardar",
            command=self.guardar_modificacion,
            bg="#3b3b3b",
            fg="#f0f0f0",
            activebackground="#4f4f4f",
            activeforeground="#f0f0f0",
            borderwidth=0,
        )
        guardar_btn.grid(row=0, column=3, sticky="e", padx=10, pady=10)

        tk.Label(
            self.ventana_modificar,
            text="Vista previa:",
            font="Georgia",
            fg="#ADADD8",
            bg="#282C34",
        ).grid(row=8, column=0, sticky="w")
        self.imagen_previa = tk.Label(self.ventana_modificar, width=190, height=190)
        self.imagen_previa.grid(row=8, column=1, sticky="w")

        # Mostrar la imagen de la receta seleccionada si existe
        if "imagen" in self.receta_seleccionada:
            self.imagen_actual = self.receta_seleccionada["imagen"]
            self.mostrar_imagen(self.imagen_actual)

    def mostrar_imagen(self, ruta_imagen):
        """Funcion para mostrar la imagen seleccionada en la ventana"""
        if ruta_imagen is not None:
            self.imagen = Image.open(ruta_imagen)
            self.imagen.thumbnail((190, 190))
            self.imagen = ImageTk.PhotoImage(self.imagen)
            self.imagen_previa.configure(image=self.imagen)
            self.imagen_previa.image = self.imagen

        else:
            # Creamos una imagen gris de 200x200 pixeles
            self.imagen = Image.new("RGB", (200, 200), color="#282C34")
            self.imagen = ImageTk.PhotoImage(self.imagen)
            self.imagen_previa.configure(image=self.imagen)
            self.imagen_previa.image = self.imagen

    def guardar_modificacion(self):
        """Funcion que guarda las modificaciones"""
        # Obtener los nuevos valores de la receta modificada
        nueva_receta = {
            "nombre": self.nombre_entry1.get(),
            "fecha": self.fecha_entry1.get_date().strftime("%d/%m/%Y"),
            "preparacion": self.preparacion_entry1.get("1.0", "end-1c"),
            "tiempo_prep": self.tiempo_prep_entry1.get(),
            "tiempo_cocc": self.tiempo_cocc_entry1.get(),
            "ingredientes": self.ingredientes_entry1.get("1.0", "end-1c"),
            "etiquetas": [
                etiqueta.strip() for etiqueta in self.etiquetas_entry1.get().split(",")
            ],
            "imagen": self.imagen_entry1.get() if self.imagen_entry1.get() else None,
        }
        # Actualizar los valores de la fila correspondiente en el treeview
        item_seleccionado = self.treeview.selection()[0]

        self.treeview.item(
            item_seleccionado,
            values=(
                nueva_receta["nombre"],
                nueva_receta["fecha"],
                nueva_receta["preparacion"],
                nueva_receta["tiempo_prep"],
                nueva_receta["tiempo_cocc"],
                nueva_receta["ingredientes"],
                ", ".join(nueva_receta["etiquetas"]),
                nueva_receta["imagen"],
            ),
        )

        # Reemplazar la receta antigua con la receta modificada en el archivo JSON
        with open("recetas.json", "r") as f:
            recetas = json.load(f)
        receta_seleccionada = next(
            (receta for receta in recetas if receta["nombre"] == self.nombre_receta),
            None,
        )

        if receta_seleccionada:
            index_receta = recetas.index(receta_seleccionada)
            recetas[index_receta] = nueva_receta

        with open("recetas.json", "w") as f:
            json.dump(recetas, f, indent=4)
        # Actualizar la receta modificada en el archivo JSON
        receta_seleccionada.update(nueva_receta)

        with open("recetas.json", "w") as f:
            json.dump(recetas, f, indent=4)

        # Actualizar la fila correspondiente en el treeview
        item_seleccionado = self.treeview.selection()[0]
        self.treeview.item(
            item_seleccionado,
            values=(
                nueva_receta["nombre"],
                nueva_receta["fecha"],
                nueva_receta["preparacion"],
                nueva_receta["tiempo_prep"],
                nueva_receta["tiempo_cocc"],
                nueva_receta["ingredientes"],
                ", ".join(nueva_receta["etiquetas"]),
                nueva_receta["imagen"],
            ),
        )

        # Mostrar mensaje de éxito
        messagebox.showinfo(
            title="Éxito", message="La receta se ha modificado correctamente."
        )
        self.ventana_modificar.destroy()

    def eliminar_receta(self):
        """Funcion que permite eliminar la receta que vaya a clickear el usuario para despues presionar el boton eliminar"""
        items_seleccionados = self.treeview.selection()
        if not items_seleccionados:
            """Si no se encuentra la receta sale un mensaje de advertencia"""
            messagebox.showwarning(
                "Error", "Por favor seleccione una o varias recetas para eliminar."
            )
            return
        nombres_recetas = [
            self.treeview.item(item)["values"][0] for item in items_seleccionados
        ]
        """Pide la confirmacion del usuario para eliminar"""
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar las {len(nombres_recetas)} recetas seleccionadas?",
        )

        if confirmacion:
            """Teniendo en cuenta la respuesta se leera el json"""
            with open("recetas.json", "r") as f:
                self.recetas = json.load(f)

            for item_seleccionado in items_seleccionados:
                """Se recorre la lista de recetas del treeview para obtener su valor"""
                nombre_receta = self.treeview.item(item_seleccionado)["values"][0]
                self.recetas = [
                    receta
                    for receta in self.recetas
                    if receta["nombre"] != nombre_receta
                ]
                """Se borra la receta teniendo en cuenta la informacion que tiene"""
                self.treeview.delete(item_seleccionado)

            """Se abre el json en escritura para poner los cambios"""
            with open("recetas.json", "w") as f:
                json.dump(self.recetas, f, indent=4)

            messagebox.showinfo(
                "Recetas eliminadas",
                f"Las {len(nombres_recetas)} recetas se han eliminado exitosamente.",
            )

    def buscar_receta(self):
        """Funcion para buscar las recetas"""
        with open("recetas.json") as f:
            self.recetas = json.load(f)
        opciones = ["nombre", "etiqueta"]
        """Opciones para buscar la receta"""
        seleccion = simpledialog.askstring(
            "Buscar receta", "¿Desea buscar por nombre o por etiqueta?"
        )
        """Uso de cuadro de dialogo para buscar la receta"""
        nombre = None
        if seleccion == "nombre":
            """Si el usuario escoge buscar por nombre se procede a buscar el nombre de la receta"""
            nombre = simpledialog.askstring(
                "Buscar receta", "Ingrese el nombre de la receta a buscar:"
            )
        if nombre:
            nombre = nombre.lower()
            recetas_encontradas = []
            """Cada receta encontrada por el nombre se la pasara a minuscula y sera almacenada en una lista"""
            for receta in self.recetas:
                """Se recorre las recentas preguntando si el nombre propuesto pertenece a la receta del json"""
                if nombre in receta["nombre"].lower():
                    """Si el nombre pertenece al json se agrega a la lista de recetas encontradas"""
                    recetas_encontradas.append(receta)
            if recetas_encontradas:
                """Luego se muestra la receta encontrada en el treeview
                mediante la funcion self.mostrar_recetas_encontradas_en_treview"""
                self.mostrar_recetas_encontradas_en_treeview(recetas_encontradas)
            else:
                """Si no esta el nombre propuesto en el json sale un mensaje de informacion diciendo que no encontro la receta"""
                messagebox.showinfo(
                    "Recetas no encontradas",
                    "No se encontraron recetas con ese nombre.",
                )
        elif seleccion == "etiqueta":
            """Se repite el mismo proceso pero escogiendo la opcion etiqueta"""
            etiqueta = simpledialog.askstring(
                "Buscar receta", "Ingrese la etiqueta que desea buscar:"
            )

            if etiqueta:
                etiqueta = etiqueta.lower()
                recetas_encontradas = []
                for receta in self.recetas:
                    if etiqueta in [e.lower() for e in receta["etiquetas"]]:
                        recetas_encontradas.append(receta)
                if recetas_encontradas:
                    self.mostrar_recetas_encontradas_en_treeview(recetas_encontradas)
                else:
                    messagebox.showinfo(
                        "Recetas no encontradas",
                        "No se encontraron recetas con esa etiqueta.",
                    )
        else:
            messagebox.showwarning("Opción inválida", "Opción de búsqueda inválida.")

    def mostrar_recetas_encontradas_en_treeview(self, recetas_encontradas):
        """Funcion para mostrar las recetas encontradas en el treeview"""
        self.treeview.delete(*self.treeview.get_children())
        for receta in recetas_encontradas:
            self.treeview.insert(
                "",
                "end",
                text=receta["nombre"],
                values=(
                    receta["nombre"],
                    receta["fecha"],
                    receta["preparacion"],
                    receta["tiempo_prep"],
                    receta["tiempo_cocc"],
                    receta["ingredientes"],
                    receta["etiquetas"],
                    receta["imagen"],
                ),
            )
        self.treeview.bind("<Double-1>", self.crear_ventana_receta)

    def mostrar_receta_del_dia(self):
        """Funcion para mostrar una receta aleatoria del dia"""
        receta_aleatoria = random.choice(self.recetas)
        ventana = tk.Toplevel(self)
        ventana.title("Receta del día")
        ventana.configure(background="gray25")
        """Creamos el marco para la imagen"""
        marco_imagen = tk.LabelFrame(ventana, text="Imagen",bg="gray25",fg="white")
        marco_imagen.grid(row=0, column=0, padx=5, pady=5)
        """Cargamos y redimensionamos la imagen"""
        imagen = None
        if receta_aleatoria.get("imagen"):
            imagen = Image.open(receta_aleatoria["imagen"])
            imagen = imagen.resize((250, 250), resample=Image.Resampling.LANCZOS)
            imagen = ImageTk.PhotoImage(imagen)
            """Creamos el widget para mostrar la imagen si existe"""
        if imagen:
            imagen_widget = tk.Label(marco_imagen, image=imagen,bg="gray25",fg="white")
            imagen_widget.grid()
        """Creamos el marco para los detalles de la receta"""
        marco_receta = tk.LabelFrame(
            ventana, text="Detalles de la receta", background="gray25", fg="white"
        )
        marco_receta.grid(row=0, column=1, padx=5, pady=5)
        """Creamos los widgets para mostrar los detalles de la receta"""
        nombre_label = tk.Label(marco_receta, text="Nombre:",bg="gray25",fg="white")
        nombre_label.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        nombre_entry = tk.Entry(marco_receta)

        nombre_entry.insert(0, receta_aleatoria["nombre"])
        nombre_entry.config(state="readonly")
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        fecha_label = tk.Label(marco_receta, text="Fecha:",bg="gray25",fg="white")
        fecha_label.grid(row=1, column=0, sticky="E", padx=5, pady=5)
        fecha_entry = tk.Entry(marco_receta)
        fecha_entry.insert(0, receta_aleatoria["fecha"])
        fecha_entry.config(state="readonly")
        fecha_entry.grid(row=1, column=1, padx=5, pady=5)

        prep_label = tk.Label(marco_receta, text="Preparación:",bg="gray25",fg="white")
        prep_label.grid(row=2, column=0, sticky="E", padx=5, pady=5)
        prep_entry = tk.Text(
            marco_receta, width=40, height=10, bg="gray25", fg="white"
        )
        prep_entry.grid(row=2, column=1, padx=5, pady=5)
        prep_entry.insert("1.0", receta_aleatoria["preparacion"])
        prep_entry.config(state="disabled")

        tiempo_prep_label = tk.Label(
            marco_receta, text="Tiempo de preparación (en minutos):",bg="gray25",fg="white"
        )
        tiempo_prep_label.grid(row=3, column=0, sticky="E", padx=5, pady=5)
        tiempo_prep_entry = tk.Entry(marco_receta)
        tiempo_prep_entry.insert(0, receta_aleatoria["tiempo_prep"])
        tiempo_prep_entry.grid(row=3, column=1, padx=5, pady=5)
        tiempo_prep_entry.configure(state="readonly")

        tiempo_cocc_label = tk.Label(
            marco_receta, text="Tiempo de cocción (en minutos):",bg="gray25",fg="white"
        )
        tiempo_cocc_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tiempo_cocc_entry = tk.Entry(marco_receta, width=30)
        tiempo_cocc_entry.grid(row=4, column=1, padx=5, pady=5)
        tiempo_cocc_entry.insert(0, receta_aleatoria["tiempo_cocc"])
        tiempo_cocc_entry.configure(state="readonly")
        """Creamos el widget para mostrar los ingredientes"""
        ingredientes_label = tk.Label(marco_receta, text="Ingredientes:",bg="gray25",fg="white")
        ingredientes_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ingredientes_entry = tk.Text(
            marco_receta, width=40, height=10, bg="gray25", fg="white"
        )
        ingredientes_entry.grid(row=5, column=1, padx=5, pady=5)
        ingredientes_entry.insert("1.0", receta_aleatoria["ingredientes"])
        ingredientes_entry.config(state="disabled")

        """Creamos el widget para mostrar las etiquetas"""
        etiquetas_label = tk.Label(marco_receta, text="Etiquetas:",bg="gray25",fg="white")
        etiquetas_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        etiquetas_entry = tk.Entry(marco_receta, width=30)
        etiquetas_entry.grid(row=6, column=1, padx=5, pady=5)
        etiquetas_entry.insert(0, ", ".join(receta_aleatoria["etiquetas"]))
        etiquetas_entry.configure(state="readonly")
        """Metodo para que no se pueda usar otra ventana hasta que la ventana de receta del dia se cierre"""
        ventana.transient(root)
        ventana.grab_set()
        root.wait_window(ventana)


root = tk.Tk()
Recetario(root).grid()
root.mainloop()
root.resizable(False, False)
