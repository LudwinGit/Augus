import gramatica as g
import tablasimbolos as TABLASIMBOLOS
from expresiones import *
from instrucciones import *

def procesar_print(instruccion, tablasimbolos) :
    print('> ', resolver_cadena(instruccion.cadena, tablasimbolos))

def resolver_cadena(expresionCadena, tablasimbolos) :
    if isinstance(expresionCadena, ExpresionComilla) :
        return expresionCadena.valor
    # elif isinstance(expresionCadena, ExpresionCadenaNumerico) :
    #     return str(resolver_expresion_aritmetica(expresionCadena.exp, tablasimbolos))
    else :
        print('Error: Expresión cadena no válida')

def procesar_instrucciones(instrucciones, tablasimbolos) :
    for instruccion in instrucciones :
        if isinstance(instruccion, Print) : procesar_print(instruccion, tablasimbolos)
        else : print('Error: instrucción no válida')

f = open("./entrada.txt", "r")
input = f.read()
#instrucciones contiene el arbol AST
instrucciones = g.parse(input)
tablasimbolos_global = TABLASIMBOLOS.TablaDeSimbolos()
procesar_instrucciones(instrucciones, tablasimbolos_global)