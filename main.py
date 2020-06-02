import gramatica as g
import tablasimbolos as TABLASIMBOLOS
from expresiones import *
from instrucciones import *

def procesar_print(instruccion, tablasimbolos) :
    print('> ', resolver_cadena(instruccion.cadena, tablasimbolos))

def procesar_asignacion(instruccion,tablasimbolos):
    val = resolver_expresion_asignacion(instruccion.expresionAsignacion, tablasimbolos)    
    if(val != None):
        if(type(val)==int): simbolo = TABLASIMBOLOS.Simbolo(instruccion.id, TABLASIMBOLOS.TIPO_DATO.NUMERO, val)
        elif(type(val)==float): simbolo = TABLASIMBOLOS.Simbolo(instruccion.id, TABLASIMBOLOS.TIPO_DATO.FLOAT, val)
        elif(type(val)==str):
            if(len(val) == 1):
                simbolo = TABLASIMBOLOS.Simbolo(instruccion.id, TABLASIMBOLOS.TIPO_DATO.CHAR, val)
            else:
                simbolo = TABLASIMBOLOS.Simbolo(instruccion.id, TABLASIMBOLOS.TIPO_DATO.STRING, val)
        if(tablasimbolos.obtener(simbolo.id) == None):
            tablasimbolos.agregar(simbolo)
        else:
            tablasimbolos.actualizar(simbolo)
        print(">>>"+str(tablasimbolos.obtener(instruccion.id).valor))

def resolver_expresion_asignacion(expresionAsignacion,tablasimbolos):
    if isinstance(expresionAsignacion,ExpresionNumero):
        return expresionAsignacion.valor
    elif isinstance(expresionAsignacion,ExpresionComilla):
        return expresionAsignacion.valor
    elif isinstance(expresionAsignacion,ExpresionIdentificador):
        if(tablasimbolos.obtener(expresionAsignacion.id)==None):
            print("La variable: \'"+expresionAsignacion.id+"\' no esta definida ")
            return None
        else:
            return tablasimbolos.obtener(expresionAsignacion.id).valor

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
        elif isinstance(instruccion, Asignacion) : procesar_asignacion(instruccion, tablasimbolos)
        else : print('Error: instrucción no válida')

f = open("./entrada.txt", "r")
input = f.read()
#instrucciones contiene el arbol AST
instrucciones = g.parse(input)
tablasimbolos_global = TABLASIMBOLOS.TablaDeSimbolos()
procesar_instrucciones(instrucciones, tablasimbolos_global)