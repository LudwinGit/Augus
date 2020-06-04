import gramatica as g
import tablasimbolos as TABLASIMBOLOS
from expresiones import *
from instrucciones import *

def procesar_exit(instruccion,tablasimbolos):
    exit()

def procesar_read(instruccion,tablasimbolos):
    val = print("simula")
    # crear_variable(instruccion.id,val,tablasimbolos)

def procesar_unset(instruccion,tablasimbolos):
    simbolo = tablasimbolos.obtener(instruccion.variable.valor)
    if(simbolo==None):
        print("La variable: \'"+instruccion.id+"\' no esta definida ")
    else:
        tablasimbolos.eliminar(simbolo)
        print("Variable eliminada")

def procesar_print(instruccion, tablasimbolos) :
    resultado = resolver_cadena(instruccion.cadena, tablasimbolos)
    if resultado != None:
        print('> ', str(resultado))

def procesar_asignacion(instruccion,tablasimbolos):
    val = resolver_asignacion(instruccion.expresionAsignacion, tablasimbolos)
    if val != None:
        crear_variable(instruccion.expresionVariable,val,tablasimbolos)

def crear_variable(expresionVariable,val,tablasimbolos):
    if(val != None):
        if(type(val)==int): agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.NUMERO,val,tablasimbolos)
        elif(type(val)==float): agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.FLOAT,val,tablasimbolos)
        elif(type(val)==str):
            if(len(val) == 1):
                agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.CHAR,val,tablasimbolos)
            else:
                agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.STRING,val,tablasimbolos)

def resolver_asignacion(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNumerica):
        return resolver_aritmetica(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionCadena):
        return resolver_cadena(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionPuntero):
        return resolver_puntero(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionLogica):
        return resolver_logica(expresion,tablasimbolos)
    return None

def resolver_identificador(expresion,tablasimbolos):
    if(tablasimbolos.obtener(expresion.id)==None):
        print("La variable: \'"+expresion.id+"\' no esta definida ")
        return None
    else:
        return tablasimbolos.obtener(expresion.id).valor

def resolver_puntero(expresion,tablasimbolos):
    simboloPuntero = tablasimbolos.obtener(expresion.puntero.valor)
    if(simboloPuntero == None):
        print("La variable: \'"+expresion.puntero.valor+"\' no esta definida ")
        return None
    else: 
        agregar_simbolo(expresion.variable.valor,TABLASIMBOLOS.TIPO_DATO.STRING,simboloPuntero.valor,tablasimbolos,simboloPuntero.id)
        return simboloPuntero.valor

def resolver_cadena(expresion, tablasimbolos) :
    if isinstance(expresion, ExpresionComilla) :
        return expresion.valor
    elif isinstance(expresion, ExpresionNumerica) :
        return resolver_aritmetica(expresion, tablasimbolos)
    else :
        print('Error: Expresión cadena no válida')

def resolver_aritmetica(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNumero):
        return expresion.valor
    elif isinstance(expresion,ExpresionNegativo):
        return resolver_aritmetica(expresion.expresion,tablasimbolos) * -1
    elif isinstance(expresion,ExpresionIdentificador):
        if(tablasimbolos.obtener(expresion.variable.valor)==None):
            print("La variable: \'"+expresion.variable.valor+"\' no esta definida ")
            return None
        else:
            return tablasimbolos.obtener(expresion.variable.valor).valor
    elif isinstance(expresion,ExpresionBinaria):
        exp1 = resolver_aritmetica(expresion.exp1, tablasimbolos)
        exp2 = resolver_aritmetica(expresion.exp2, tablasimbolos)
        if expresion.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
        if expresion.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if expresion.operador == OPERACION_ARITMETICA.MUL : return exp1 * exp2
        if expresion.operador == OPERACION_ARITMETICA.DIV : return exp1 / exp2
        if expresion.operador == OPERACION_ARITMETICA.RESIDUO : return exp1 / exp2
    elif isinstance(expresion,ExpresionAbsoluto):
        return abs(resolver_aritmetica(expresion.expresion,tablasimbolos))

def resolver_logica(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNot):
        resultado = resolver_aritmetica(expresion.expresionnumeria,tablasimbolos)
        if resultado == 0:
            return 1
        elif resultado == 1:
            return 0
        else:
            print("Los valores aceptados para el NOT son 1 y 0")
            return None

def agregar_simbolo(id,tipo_dato,val,tablasimbolos,puntero=0):
    simbolo=tablasimbolos.obtener(id)
    nuevoSimbolo=TABLASIMBOLOS.Simbolo(id, tipo_dato, val,puntero)
    if(simbolo == None):
        tablasimbolos.agregar(nuevoSimbolo)
    else:
        if(str(simbolo.puntero)!="0"):
            nuevoSimbolo.puntero = simbolo.puntero
            actualizarvalorpuntero = tablasimbolos.obtener(simbolo.puntero)
            actualizarvalorpuntero.valor = val

        for s in tablasimbolos.simbolos:
            sim = tablasimbolos.obtener(s)
            if(str(sim.puntero)==str(id)):
                sim.valor = val
        tablasimbolos.actualizar(nuevoSimbolo)

def imprimirTabla(tablasimbolos):
    for s in tablasimbolos.simbolos:
        simbolo = tablasimbolos.obtener(s)
        print("id:"+str(simbolo.id) +" valor:"+str(simbolo.valor)+" puntero:"+str(simbolo.puntero))

def procesar_instrucciones(instrucciones, tablasimbolos) :
    for instruccion in instrucciones :
        if isinstance(instruccion, Print) : procesar_print(instruccion, tablasimbolos)
        elif isinstance(instruccion, Asignacion) : procesar_asignacion(instruccion, tablasimbolos)
        elif isinstance(instruccion,Unset) : procesar_unset(instruccion,tablasimbolos)
        elif isinstance(instruccion,Read) : procesar_read(instruccion,tablasimbolos)
        elif isinstance(instruccion,Exit) : procesar_exit(instruccion,tablasimbolos)
        else : print('Error: instrucción no válida')

f = open("./entrada.txt", "r")
input = f.read()
#instrucciones contiene el arbol AST
instrucciones = g.parse(input)
tablasimbolos_global = TABLASIMBOLOS.TablaDeSimbolos()
procesar_instrucciones(instrucciones, tablasimbolos_global)
imprimirTabla(tablasimbolos_global)