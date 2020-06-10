class Instruccion:
    '''Clase abstracta'''

class Print(Instruccion) :
    def __init__(self,  cadena,id_dot) :
        self.cadena = cadena
        self.id_dot = id_dot

class Asignacion(Instruccion) :
    def __init__(self, expresionVariable, expresionAsignacion,id_dot) :
        self.expresionVariable = expresionVariable
        self.expresionAsignacion = expresionAsignacion
        self.id_dot = id_dot

class Unset(Instruccion):
    def __init__(self,variable,id_dot):
        self.variable = variable
        self.id_dot = id_dot

class Read(Instruccion):
    def __init__(self,id,id_dot):
        self.id = id
        self.id = id_dot

class Exit(Instruccion):
    '''Clase para la instruccion Exit'''
    def __init__(self,id_dot):
        self.id_dot = id_dot

class Array(Instruccion):
    def __init__(self,variable,indices,valor,id_dot):
        self.variable = variable
        self.indices = indices
        self.valor = valor
        self.id_dot = id_dot

class Etiqueta(Instruccion):
    def __init__(self,nombre,id_dot):
        self.nombre = nombre
        self.id_dot = id_dot
    
class EtiquetaMain(Instruccion):
    def __init__(self,nombre,instrucciones,id_dot):
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.id_dot = id_dot

class Goto(Instruccion):
    def __init__(self,etiqueta,id_dot):
        self.etiqueta = etiqueta
        self.id_dot = id_dot

class Ifgoto(Instruccion):
    def __init__(self,expresionValidar,etiqueta,id_dot):
        self.expresionValidar = expresionValidar
        self.etiqueta = etiqueta
        self.id_dot = id_dot