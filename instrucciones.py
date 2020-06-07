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

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones

class IfElse(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica, instrIfVerdadero = [], instrIfFalso = []) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso