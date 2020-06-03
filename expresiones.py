from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4

class OPERACION_LOGICA(Enum) :
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    DIFERENTE = 4


class ExpresionNumerica:
    '''Clase abstracta para las producciones numericas de variables'''

class ExpresionPuntero():
    def __init__(self,id,puntero):
        self.id = id
        self.puntero = puntero

class ExpresionNumero(ExpresionNumerica) :
    def __init__(self, valor = 0) :
        self.valor = valor

class ExpresionNegativo(ExpresionNumerica) :
    def __init__(self, expresion) :
        self.expresion = expresion

class ExpresionIdentificador(ExpresionNumerica) :
    def __init__(self, id = "") :
        self.id = id

class ExpresionBinaria() :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionCadena :
    '''Clase abstracta para cadena'''

class ExpresionComilla(ExpresionCadena) :
    def __init__(self, cadena) :
        self.valor = cadena

class ExpresionCadenaNumerico(ExpresionCadena) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionLogica() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador