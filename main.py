from analizador_ascendente import *
from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
from graphviz import Graph
from Editor import * 

ruta = "" # La utilizaremos para almacenar la ruta del fichero

#=======================================================VENTANAS
def createNewWindow():
    newWindow = Toplevel(root)
    newWindow.title("REPORTE DE ERRORES")
    texto = Text(newWindow,bg="#fff")
    texto.pack(side="left", fill="both", expand=1)
    texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))
    texto.delete(1.0,'end')
    # print()
    for index in analizadorAscendente.g.errores.errores:
        error = analizadorAscendente.g.errores.errores[index]
        text = "||"+error.tipo+"||"+error.descripcion+"||"+str(error.linea)+"\n"
        texto.insert('end', text)

def nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    contenedorEditor.Editor().delete(1.0, "end")
    root.title("EDITOR")

def abrir():
    global ruta
    mensaje.set("Abrir fichero")
    ruta = FileDialog.askopenfilename(
        initialdir='.', 
        filetypes=(("Ficheros de texto", "*.txt"),),
        title="Abrir un fichero de texto")

    if ruta != "":
        fichero = open(ruta, 'r')
        contenido = fichero.read()
        contenedorEditor.Editor().delete(1.0,'end')
        contenedorEditor.Editor().insert('insert',contenido)
        fichero.close()
        root.title(ruta + " - Mi editor")
    contenedorEditor.colorearTexto()

def guardar():
    mensaje.set("Guardar fichero")
    if ruta != "":
        contenido = contenedorEditor.Editor().get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        guardar_como()

def guardar_como():
    global ruta
    mensaje.set("Guardar fichero como")

    fichero = FileDialog.asksaveasfile(title="Guardar fichero", 
        mode="w", defaultextension=".txt")

    if fichero is not None:
        ruta = fichero.name
        contenido = contenedorEditor.Editor().get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""

def debugAsc():
    t = contenedorEditor.Editor().get(1.0,'end-1c')
    debugAscendente.run(t)
    debugAscendente.Debug()

def debugControl():
    debugAscendente.Debug()
    consola.delete(1.0,'end-1c')
    consola.insert("end",debugAscendente.salida)

def genearAst():
    analizadorAscendente.g.dot.view()

def ejecutar():
    t = contenedorEditor.Editor().get(1.0,'end-1c')
    # t = editor.getText()
    analizadorAscendente.run(t)
    analizadorAscendente.Ejecutar()
    consola.delete(1.0,'end-1c')
    consola.insert("end",analizadorAscendente.salida)
# Configuración de la raíz
root = Tk()
root.title("Mi editor")

# Menú superior
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=nuevo)
filemenu.add_command(label="Abrir", command=abrir)
filemenu.add_command(label="Guardar", command=guardar)
filemenu.add_command(label="Guardar como", command=guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(menu=filemenu, label="Archivo")

menuReportes = Menu(menubar, tearoff=0)
menuReportes.add_command(label="Arból AST", command=genearAst)
menuReportes.add_command(label="Errores", command=createNewWindow)
menuReportes.add_separator()
menubar.add_cascade(menu=menuReportes, label="Reportes")

toolbar = Frame(root, bg="#fff")
toolbar.pack(side="top", fill="x")

bold_btn = Button(toolbar, text="Ascendente",command=ejecutar)
bold_btn.pack(side="left")

bold_btn = Button(toolbar, text="Debug asc",command=debugAsc)
bold_btn.pack(side="left")

bold_btn = Button(toolbar, text="Siguiente",command=debugControl)
bold_btn.pack(side="left")

contenedorEditor = ContenedorEditor(root,bg="#fff")
contenedorEditor.pack(side="left", fill="both", expand=1)

#Mensaje
mensaje = StringVar()
mensaje.set("Bienvenido a tu Editor")
# Monitor inferior
consola = Text(root,bg="#003B74",fg="#fff")
consola.pack(side="right",fill="both")
#Debug ascendente
debugAscendente = Analizador()
analizadorAscendente = Analizador()
root.config(menu=menubar)
# Finalmente bucle de la apliación
root.mainloop()