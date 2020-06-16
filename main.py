from analizador_ascendente import *
from analizador_descendente import *
from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
from graphviz import Graph
from Editor import * 
from tablasimbolos import *

ruta = "" # La utilizaremos para almacenar la ruta del fichero

#=======================================================VENTANAS
def createNewWindow():
    global ascendente
    newWindow = Toplevel(root)
    newWindow.title("REPORTE DE ERRORES")
    texto = Text(newWindow,bg="#fff")
    texto.pack(side="left", fill="both", expand=1)
    texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))
    texto.delete(1.0,'end')
    
    if ascendente:
        for index in analizadorAscendente.g.errores.errores:
            error = analizadorAscendente.g.errores.errores[index]
            text = "||"+error.tipo+"||"+error.descripcion+"||"+str(error.linea)+"\n"
            texto.insert('end', text)
    else:
        for index in analizadorDescendente.g.errores.errores:
            error = analizadorDescendente.g.errores.errores[index]
            text = "||"+error.tipo+"||"+error.descripcion+"||"+str(error.linea)+"\n"
            texto.insert('end', text)

def windowGramatica():
    global ascendente
    newWindow = Toplevel(root)
    newWindow.title("REPORTE GRAMATICAL")
    texto = Text(newWindow,bg="#fff")
    texto.pack(side="left", fill="both", expand=1)
    texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))
    texto.delete(1.0,'end')
    # print()
    if ascendente:
        for index in reversed(analizadorAscendente.g.repgramatical):
            produccion = analizadorAscendente.g.repgramatical[index]
            text = produccion+"\n"
            texto.insert('end', text)
    else:
        for index in reversed(analizadorDescendente.g.repgramatical):
            produccion = analizadorDescendente.g.repgramatical[index]
            text = produccion+"\n"
            texto.insert('end', text)

def windowTablaSimbolos():
    global ascendente
    newWindow = Toplevel(root)
    newWindow.title("TABLA DE SIMBOLOS")
    texto = Text(newWindow,bg="#fff")
    texto.pack(side="left", fill="both", expand=1)
    texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))
    texto.delete(1.0,'end')

    texto.insert('end',"==================================TABLA SIMBOLOS=================\n")
    if ascendente:
        for s in analizadorAscendente.tablasimbolos.simbolos:
            simbolo = analizadorAscendente.tablasimbolos.obtener(s)
            texto.insert('end',"||Id:"+str(simbolo.id)+"||Ambito: "+str(simbolo.declarada_en)+"||Tipo: "+str(simbolo.tipo)+"||Dimsensión: "+str(simbolo.dimension)+"||Valor:"+str(simbolo.valor)+"\n")
            texto.insert('end',"=================================================================\n")
    else:
        for s in analizadorDescendente.tablasimbolos.simbolos:
            simbolo = analizadorDescendente.tablasimbolos.obtener(s)
            texto.insert('end',"||Id:"+str(simbolo.id)+"||Ambito: "+str(simbolo.declarada_en)+"||Tipo: "+str(simbolo.tipo)+"||Dimsensión: "+str(simbolo.dimension)+"||Valor:"+str(simbolo.valor)+"\n")
            texto.insert('end',"=================================================================\n")

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
    global linea_anterior
    t = contenedorEditor.Editor().get(1.0,'end-1c')
    analizadorAscendente.run(t)
    linea=analizadorAscendente.Debug()
    consola.delete(1.0,'end-1c')
    consola.insert("end",analizadorAscendente.salida)
    contenedorEditor.MarcarLinea(linea,linea_anterior)

def debugControl():
    global linea_anterior
    linea=analizadorAscendente.Debug()
    consola.delete(1.0,'end-1c')
    consola.insert("end",analizadorAscendente.salida)
    contenedorEditor.MarcarLinea(linea,linea_anterior)
    linea_anterior = linea

def genearAst():
    global ascendente
    if ascendente:
        analizadorAscendente.g.dot.view()
    else:
        analizadorDescendente.g.dot.view()

def ejecutar():
    global ascendente
    t = contenedorEditor.Editor().get(1.0,'end-1c')
    ascendente = True
    # t = editor.getText()
    analizadorAscendente.run(t)
    analizadorAscendente.Ejecutar()
    consola.delete(1.0,'end-1c')
    consola.insert("end",analizadorAscendente.salida)

def ejecutarDescendente():
    global ascendente
    ascendente = False
    t = contenedorEditor.Editor().get(1.0,'end-1c')
    # t = editor.getText()
    analizadorDescendente.run(t)
    analizadorDescendente.Ejecutar()
    consola.delete(1.0,'end-1c')
    consola.insert("end",analizadorDescendente.salida)
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
menuReportes.add_command(label="Tabla simbolos", command=windowTablaSimbolos)
menuReportes.add_command(label="Gramatica",command=windowGramatica)
menuReportes.add_separator()
menubar.add_cascade(menu=menuReportes, label="Reportes")

toolbar = Frame(root, bg="#fff")
toolbar.pack(side="top", fill="x")

bold_btn = Button(toolbar, text="Ascendente",command=ejecutar)
bold_btn.pack(side="left")

bold_btn = Button(toolbar, text="Descendente",command=ejecutarDescendente)
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
#linea anterior para el debug
linea_anterior=1
# Monitor inferior
consola = Text(root,bg="#003B74",fg="#fff")
consola.pack(side="right",fill="both")
ascendente = True
#Debug ascendente
debugAscendente = AnalizadorAscendente()
analizadorAscendente = AnalizadorAscendente()
analizadorDescendente = AnalizadorDescendente()
root.config(menu=menubar)
# Finalmente bucle de la apliación
root.mainloop()