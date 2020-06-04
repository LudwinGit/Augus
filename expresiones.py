from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    MUL = 3
    DIV = 4
    RESIDUO = 5

class OPERACION_LOGICA(Enum) :
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4

class OPERACION_RELACIONAL(Enum) :
    IGUAL = 1
    DIFERENTE = 2
    MAYOR_IGUAL = 3
    MENOR_IGUAL = 4
    MAYOR = 5
    MENOR = 6

class ExpresionNumerica:
    '''Clase abstracta para las producciones numericas de variables'''

class ExpresionNumero(ExpresionNumerica) :
    def __init__(self, valor = 0) :
        self.valor = valor

class ExpresionNegativo(ExpresionNumerica) :
    def __init__(self, expresion) :
        self.expresion = expresion

class ExpresionIdentificador(ExpresionNumerica) :
    def __init__(self, variable = "") :
        self.variable = variable

class ExpresionAbsoluto(ExpresionNumerica):
    def __init__(self,expresion):
        self.expresion = expresion

class ExpresionBinaria(ExpresionNumerica) :
    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionCadena :
    '''Clase abstracta para cadena'''

class ExpresionComilla(ExpresionCadena) :
    def __init__(self, cadena) :
        self.valor = cadena

class ExpresionPuntero():
    def __init__(self,variable,puntero):
        self.variable = variable
        self.puntero = puntero

class ExpresionVariable():
    def __init__(self,valor):
        self.valor = valor

class ExpresionLogica() :
    '''Clase abstracta para instrucciones logicas'''
    def __init__(self,expresion1,operador,expresion2):
        self.expresion1 = expresion1
        self.operador = operador
        self.expresion2 = expresion2

class ExpresionNot(ExpresionLogica):
    def __init__(self,expresionnumeria):
        self.expresionnumeria = expresionnumeria

class ExpresionCasteo():
    def __init__(self,tipo,expresiongeneral):
        self.tipo = tipo
        self.expresiongeneral = expresiongeneral

class ExpresionRelacional():
    def __init__(self,expg1,expg2,operador):
        self.expresiongeneral1 = expg1
        self.expresiongeneral2 = expg2
        self.operador = operador