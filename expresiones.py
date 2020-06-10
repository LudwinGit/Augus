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

class OPERACION_BIT(Enum):
    NOT = 1
    AND = 2
    OR  = 3
    XOR = 4
    SHIFTIZQ = 5
    SHIFTDER = 6

class ExpresionNumerica:
    '''Clase abstracta para las producciones numericas de variables'''

class ExpresionNumero(ExpresionNumerica) :
    def __init__(self,id_dot,valor = 0) :
        self.valor = valor
        self.id_dot = id_dot

class ExpresionNegativo(ExpresionNumerica) :
    def __init__(self, expresion,id_dot) :
        self.expresion = expresion
        self.id_dot = id_dot

class ExpresionIdentificador(ExpresionNumerica) :
    def __init__(self,id_dot, variable = "") :
        self.variable = variable
        self.id_dot = id_dot

class ExpresionAbsoluto(ExpresionNumerica):
    def __init__(self,expresion,id_dot):
        self.expresion = expresion
        self.id_dot = id_dot

class ExpresionBinaria(ExpresionNumerica) :
    def __init__(self, exp1, exp2, operador,id_dot) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.id_dot = id_dot

class ExpresionCadena :
    '''Clase abstracta para cadena'''

class ExpresionComilla(ExpresionCadena) :
    def __init__(self, cadena,id_dot) :
        self.valor = cadena
        self.id_dot = id_dot

class ExpresionPuntero():
    def __init__(self,variable,puntero,id_dot):
        self.variable = variable
        self.puntero = puntero
        self.id_dot = id_dot

class ExpresionVariable():
    def __init__(self,valor,id_dot):
        self.valor = valor
        self.id_dot = id_dot

class ExpresionLogica() :
    '''Clase abstracta para instrucciones logicas'''
    def __init__(self,expresion1,operador,expresion2,id_dot):
        self.expresion1 = expresion1
        self.operador = operador
        self.expresion2 = expresion2
        self.id_dot = id_dot

class ExpresionNot(ExpresionLogica):
    def __init__(self,expresionnumeria,id_dot):
        self.expresionnumeria = expresionnumeria
        self.id_dot = id_dot

class ExpresionCasteo():
    def __init__(self,tipo,expresiongeneral,id_dot):
        self.tipo = tipo
        self.expresiongeneral = expresiongeneral
        self.id_dot = id_dot

class ExpresionRelacional():
    def __init__(self,expg1,expg2,operador,id_dot):
        self.expresiongeneral1 = expg1
        self.expresiongeneral2 = expg2
        self.operador = operador
        self.id_dot = id_dot

class ExpresionBit():
    def __init__(self,expNum1,expNum2,operador):
        self.expresionNum1 = expNum1
        self.expresionNum2 = expNum2
        self.operador = operador

class ExpresionNotBit(ExpresionBit):
    def __init__(self,expNum,id_dot):
        self.expresionNum = expNum
        self.id_dot = id_dot


class ExpresionArrayDeclare():
    'Clase abstracta para declarar un nuevo array'

class ExpresionArray():
    'Clase abstracta para manejar arrays'
    def __init__(self,variable,indices):
        self.variable = variable
        self.indices = indices