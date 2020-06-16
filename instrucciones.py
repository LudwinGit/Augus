class Instruccion:
    '''Clase abstracta'''

class Print(Instruccion) :
    def __init__(self,  cadena,id_dot,linea) :
        self.cadena = cadena
        self.id_dot = id_dot
        self.linea = linea

class Asignacion(Instruccion) :
    def __init__(self, expresionVariable, expresionAsignacion,id_dot,linea) :
        self.expresionVariable = expresionVariable
        self.expresionAsignacion = expresionAsignacion
        self.id_dot = id_dot
        self.linea = linea

class Unset(Instruccion):
    def __init__(self,variable,id_dot,linea):
        self.variable = variable
        self.id_dot = id_dot
        self.linea = linea

class Read(Instruccion):
    def __init__(self,id,id_dot,linea):
        self.id = id
        self.id_dot = id_dot
        self.valor=0
        self.linea = linea

    def ingresar(self):
        self.valor = input('Ingrese el valor >')
        return self.valor

class Exit(Instruccion):
    '''Clase para la instruccion Exit'''
    def __init__(self,id_dot,linea):
        self.id_dot = id_dot
        self.linea = linea

class Array(Instruccion):
    def __init__(self,variable,indices,valor,id_dot,linea):
        self.variable = variable
        self.indices = indices
        self.valor = valor
        self.id_dot = id_dot
        self.linea = linea

class Etiqueta(Instruccion):
    def __init__(self,nombre,id_dot,linea):
        self.nombre = nombre
        self.id_dot = id_dot
        self.linea = linea
    
class EtiquetaMain(Instruccion):
    def __init__(self,nombre,instrucciones,id_dot,linea):
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.id_dot = id_dot
        self.linea = linea

class Goto(Instruccion):
    def __init__(self,etiqueta,id_dot,linea):
        self.etiqueta = etiqueta
        self.id_dot = id_dot
        self.linea = linea

class Ifgoto(Instruccion):
    def __init__(self,expresionValidar,etiqueta,id_dot,linea):
        self.expresionValidar = expresionValidar
        self.etiqueta = etiqueta
        self.id_dot = id_dot
        self.linea = linea