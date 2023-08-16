
# Recetario de cocina

Proyecto integrador de la materia Programacion I de la carrera Tecnicatura Universitaria en Desarrollo de Software

## Installation
Instalar los siguientes modulos para su funcionamiento

```bash
  pip install tkcalendar
  pip install Pillow
  pip install watchdog
  pip install ttkthemes
```
## Modulos, submodulos y librerias utilizados

## tkinter

tkinter es un módulo estándar de Python para crear interfaces gráficas de usuario. Es una herramienta muy útil para crear ventanas, botones, cuadros de diálogo, entre otros elementos de la interfaz gráfica.

## ttk
ttk es un submódulo de tkinter que proporciona una serie de widgets y herramientas adicionales para crear interfaces gráficas de usuario con un aspecto más moderno y elegante.


## datetime

datetime es un módulo estándar de Python que proporciona clases para trabajar con fechas y horas. Es útil para formatear y manipular fechas y horas de manera sencilla.

## os

os es un módulo estándar de Python que proporciona una manera de interactuar con el sistema operativo. Es útil para realizar operaciones de entrada/salida en el sistema de archivos, como crear, mover o eliminar archivos y directorios.

## json

json es un módulo estándar de Python para trabajar con datos en formato JSON. Es útil para leer y escribir archivos JSON, y para convertir objetos de Python en JSON y viceversa.

## io

io es un módulo estándar de Python que proporciona herramientas para trabajar con flujos de datos en memoria, como bytes, cadenas y archivos. Es útil para leer y escribir archivos de manera eficiente.

## random

random es un módulo estándar de Python que proporciona herramientas para generar números aleatorios. Es útil para generar valores aleatorios para pruebas o simulaciones.

## watchdog

watchdog es una librería de Python que proporciona herramientas para observar cambios en los archivos y directorios de un sistema de archivos. Es útil para automatizar tareas cuando se detectan cambios en los archivos, como compilar o ejecutar código.

## ttkthemes
ttkthemes es una librería de Python que proporciona temas adicionales para los widgets de ttk. Es útil para personalizar la apariencia de las interfaces gráficas de usuario.

## PIL
PIL (Python Imaging Library) es una librería de Python para procesar imágenes. Es útil para abrir, manipular y guardar imágenes en diferentes formatos.

## tkcalendar
tkcalendar es una librería de Python que proporciona un widget de calendario para tkinter. Es útil para seleccionar fechas de manera sencilla en la interfaz gráfica de usuario.

## LabelFrame
LabelFrame es un submódulo de ttk que proporciona un widget para agrupar otros widgets relacionados bajo un título. Es útil para organizar la interfaz gráfica de usuario en secciones lógicas.

## messagebox
messagebox es un submódulo de tkinter que proporciona cuadros de diálogo para mostrar mensajes al usuario, como mensajes de error, advertencia o información.

## simpledialog
simpledialog es un submódulo de tkinter que proporciona cuadros de diálogo simples para obtener información del usuario, como una cadena de texto o un número.

## filedialog
un módulo de tkinter que proporciona diálogos comunes para abrir y guardar archivos

## recipe_new
(de recipe_new): un modulo creado por el usuario para poder crear recetas

## Observer y FileSystemEventHandler (de watchdog)

módulos que permiten observar cambios en el sistema de archivos y responder en consecuencia.

## ThemedStyle (de ttkthemes)
una clase que proporciona un control de estilo para widgets ttk en tkinter.

## END
 es una constante que se utiliza en la biblioteca de interfaz gráfica de usuario (GUI) de Python tkinter para indicar el final de un texto en un widget de texto.
## DateEntry
es una clase de widget de tkcalendar que proporciona una forma fácil de seleccionar una fecha a través de un widget de calendario. Permite al usuario seleccionar una fecha haciendo clic en un día en el calendario o navegando a través de los meses y años usando las flechas de navegación. El valor seleccionado se devuelve como un objeto de fecha de Python.

## Documentacion de funciones
     def abrir(self):
     """Funcion que abre una ventana que pertenece al  modulo recipe_new  para poder acceder a
     los campos de frame y su respectivas funciones""
     
     def guardar_receta(self):
     """Funcion que guarda las recetas que se vayan escribiendo en los campos de
     frame que tiene la ventana secundaria.
     esta funcion permite guardar la informacion que se va ingresando en la ventana, 
     el nombre, fecha (usando tkcalendar), preparacion, ingredientes, tiempo de coccion,
     tiempo de preparacion (ambos deben ser pasados por enteros), etiquetas y opcionalmente
     una imagen. Al finalizar la creacion los campos que sirvieron
     para crear la receta seran borrados para poder crear la
     siguiente receta y cabe aclarar cada receta sera guardada en
     un archivo json llamada recetas.json"""
     
     def cargar_imagen(self):
     """permite cargar imagenes cuando el usuario vaya a clickear el boton cargar
     imagen esta funcion lo llevara al buscador de archivos asi podra poner la imagen en la 
     receta y guardarla al final de la creacion. Despues de haber puesto la imagen se mostrara
     la Ruta de la imagen"""
     

     def on_modified(self, event):
     """funcion que permite el monitoreo y modificacion de
     datos en este caso del archivo json"""
     
     def crear_widgets(self):
     """Funcion que tiene como tarea crear los diversos widgets
     que llevara la ventana principal, crea tanto como
     campos de frame, label, entry, treeview, y scrollbar"""

     def crear_ventana(self, event):
     """Funcion que crea una ventana para que muestre toda
     la informacion de la receta que escogio el usuario
     esta funcion se llama mediante el doble click de una
     receta en el treeview"""

     def aplicar_estilo(self):
     """Funcion que aplica un estilo en particular a los widgets del programa""

     def agregar_tema_adwark(self, ventana):
     """Funcion que escoge el tema awdark para la ventana"""
     
     def iniciar_watchdog(self):
     """Funcion que inicia el monitoreo y observacion del archivo en este caso del json"""

     def cargar_archivo_json(self):
     """Esta funcion sirve para poder cargar cualquier archivo json con recetas al treeview 
     de la ventana principal. Esta funcion se la puede llamar por el boton cargar_archivos de 
     la ventana en donde te llevara a un buscador de archivos para que puedas escoger el
     documento json"""

     def cargar_recetas(self):
     """Permite cargar las recetas ya existentes al treevie cuando vayas abrir el prorama estas
     recetas pueden ser manipulables como las demas"""

     def modifcar_recetas(self):
     """Esta funcion permite modificar las recetas que fueron elegidas por el usuario al haber
     hecho click en el boton modificar la misma te mandara a una ventana en donde tienen sus
     campos con la informacion recolectada de la receta, se puede editar toda
     la receta exceptuando la imagen que solo aparece como una vista previa
     al tocar el boton de guardar se podra ver el cambio en el treeview y en el json"""

     def mostrar_imagen(self, ruta_imagen):
     """Funcion que permite poder mostrar la imagen que sera cargada en la ventana modificar"""

     def guardar_modificacion(self):
     """Esta funcion sirve para poder guardar las modificaciones que se haran en el archivo json
     y en el treeview, puede ser llamada mediante el click del boton guardar de la ventana
     modificar"""

     def eliminar_receta(self):
     """Funcion que elimina la receta tanto del json como del treeview, esta funcion se activara
     siempre y cuando que el usuario haga un solo click en la receta y clickee el boton eliminar
     receta"""

     def buscar_receta(self):
     """Es un buscador que tiene como opciones buscar por el nombre y por la etiqueta, esta 
     puede ser activada tocando el boton buscar_receta la funcion buscara segun el nombre o 
     etiqueta de la receta tanto del treeview como del archivo json"""

     def mostrar_recetas_encontradas_en_treeview(self):
     """Funcion que muestra las recetas encontradas en el treeview"""

     def mostrar_receta_del_dia(self):
     """Funcion que permite abrir una receta con toda su informacion en otra ventana de manera aleatoria
     y con una interfaz diferente. Puede ser llamada tocando el boton receta del dia"""




