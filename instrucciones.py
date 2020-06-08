class Instruccion:
    '''Clase abstracta'''

class Print(Instruccion) :
    def __init__(self,  cadena) :
        self.cadena = cadena

class Asignacion(Instruccion) :
    def __init__(self, expresionVariable, expresionAsignacion) :
        self.expresionVariable = expresionVariable
        self.expresionAsignacion = expresionAsignacion

class Unset(Instruccion):
    def __init__(self,variable):
        self.variable = variable

class Read(Instruccion):
    def __init__(self,id):
        self.id = id

class Exit(Instruccion):
    '''Clase para la instruccion Exit'''

class Array(Instruccion):
    def __init__(self,variable,indices,valor):
        self.variable = variable
        self.indices = indices
        self.valor = valor

class Etiqueta(Instruccion):
    def __init__(self,nombre):
        self.nombre = nombre
    
class EtiquetaMain(Instruccion):
    def __init__(self,nombre,instrucciones):
        self.nombre = nombre
        self.instrucciones = instrucciones

class Goto(Instruccion):
    def __init__(self,etiqueta):
        self.etiqueta = etiqueta

class Ifgoto(Instruccion):
    def __init__(self,expresionValidar,etiqueta):
        self.expresionValidar = expresionValidar
        self.etiqueta = etiqueta