from analizador import *
from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
from graphviz import Graph

ruta = "" # La utilizaremos para almacenar la ruta del fichero

def nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("Mi editor")

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
        texto.delete(1.0,'end')
        texto.insert('insert', contenido)
        fichero.close()
        root.title(ruta + " - Mi editor")
    colorearTexto()

def colorearTexto():
    texto.tag_add("BOLD", "1.0", "end-1c")        
    t = texto.get(1.0,'end-1c')
    consola.delete(1.0,'end-1c')
    lineas = t.split('\n')

    reservadas = ['main','goto' ,'unset','print','read' ,'exit' ,'int'  ,'float','char' ,'abs',
                    'array','if'   ]

    palabra = ""
    l =0
    for linea in lineas:
        l += 1
        columna = 0
        linea = linea+" " #Agregamos un espacio para que reconozca la ultima palabra si no hay salto
        while columna < len(linea):
            if 96 < ord(linea[columna]) < 123 :
                palabra+=linea[columna]
            elif ord(linea[columna]) == 35:
                index1 = str(l)+"."+str(columna)
                index2 = str(l)+"."+str(len(linea))
                texto.tag_add("comentario", index1, index2)
                texto.tag_config("comentario", foreground="#849699")
                palabra =""
                columna = len(linea)
            elif ord(linea[columna]) == 36:
                index1 = str(l)+"."+str(columna)
                index2 = str(l)+"."+str(columna+1)
                texto.tag_add("variable", index1, index2)
                texto.tag_config("variable", foreground="#F00019")
            else:
                if palabra in reservadas:
                    index1 = str(l)+"."+str(columna-len(palabra))
                    index2 = str(l)+"."+str(columna)
                    texto.tag_add("reservada", index1, index2)
                    # texto.tag_config("reservada", background="#696962", foreground="#01087C")
                    texto.tag_config("reservada", foreground="#003B74")
                palabra = ""
            columna += 1

def guardar():
    mensaje.set("Guardar fichero")
    if ruta != "":
        contenido = texto.get(1.0,'end-1c')
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
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""

def ejecutar():
    t = texto.get(1.0,'end-1c')
    analizador = Analizador(t)
    consola.delete(1.0,'end-1c')
    consola.insert("end",analizador.salida)
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

toolbar = Frame(root, bg="#fff")
toolbar.pack(side="top", fill="x")

bold_btn = Button(toolbar, text="Ejecutar",command=ejecutar)
bold_btn.pack(side="left")

# Caja de texto central
texto = Text(root,bg="#fff")
texto.pack(fill="both", expand=1)
texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))


#Mensaje
mensaje = StringVar()
mensaje.set("Bienvenido a tu Editor")
# Monitor inferior
consola = Text(root,bg="#003B74",fg="#fff")
consola.pack(fil="both")

root.config(menu=menubar)
# Finalmente bucle de la apliación
root.mainloop()