import gramatica as g
import tablasimbolos as TABLASIMBOLOS
from expresiones import *
from instrucciones import *

def procesar_print(instruccion, tablasimbolos) :
    print('> ', resolver_cadena(instruccion.cadena, tablasimbolos))

def procesar_asignacion(instruccion,tablasimbolos):
    val = resolver_expresion_asignacion(instruccion.expresionAsignacion, tablasimbolos)    
    if(val != None):
        if(type(val)==int): agregar_simbolo(instruccion.id,TABLASIMBOLOS.TIPO_DATO.NUMERO,val,tablasimbolos)
        elif(type(val)==float): agregar_simbolo(instruccion.id,TABLASIMBOLOS.TIPO_DATO.FLOAT,val,tablasimbolos)
        elif(type(val)==str):
            if(len(val) == 1):
                agregar_simbolo(instruccion.id,TABLASIMBOLOS.TIPO_DATO.CHAR,val,tablasimbolos)
            else:
                agregar_simbolo(instruccion.id,TABLASIMBOLOS.TIPO_DATO.STRING,val,tablasimbolos)

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
    elif isinstance(expresionAsignacion,ExpresionNegativo):
        return resolver_expresion_asignacion(expresionAsignacion.expresion,tablasimbolos) * -1
    elif isinstance(expresionAsignacion,ExpresionPuntero):
        simboloPuntero = tablasimbolos.obtener(expresionAsignacion.puntero)
        if(simboloPuntero == None):
            print("La variable: \'"+expresionAsignacion.puntero+"\' no esta definida ")
            return None
        else: 
            agregar_simbolo(expresionAsignacion.id,TABLASIMBOLOS.TIPO_DATO.STRING,simboloPuntero.valor,tablasimbolos,simboloPuntero.id)
        return simboloPuntero.valor

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

def cambiar_valores_punteros(simbolo,tablasimbolos):
    TABLASIMBOLOS.Simbolo(instruccion.id, TABLASIMBOLOS.TIPO_DATO.FLOAT, val)
    # print(simbolo)
    if(tablasimbolos.obtener(simbolo.id) == None):
        tablasimbolos.agregar(simbolo)
    else:
        tablasimbolos.actualizar(simbolo)

    #buscar los identificadores donde se realizado un puntero al id actual
    # for s in tablasimbolos.simbolos:
    #     simboloActualizar = tablasimbolos.obtener(s)
    #     print(str(simboloActualizar.id_puntero)+" "+str(simbolo.id))
    #     if(simboloActualizar.id_puntero == simbolo.id):
    #         print(s+":");
    #         simboloActualizar = tablasimbolos.obtener(s)
    #         simboloActualizar.valor = simbolo.valor
    #         tablasimbolos.actualizar(simboloActualizar)

    #Buscar el identificador del puntero del id actual
    # if(str(simbolo.id_puntero) != "0"):
    #     simboloActualizar = tablasimbolos.obtener(simbolo.id_puntero)
    #     simboloActualizar.valor = simbolo.valor
    #     tablasimbolos.actualizar(simboloActualizar)

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

f = open("./entrada.txt", "r")
input = f.read()
#instrucciones contiene el arbol AST
instrucciones = g.parse(input)
tablasimbolos_global = TABLASIMBOLOS.TablaDeSimbolos()
procesar_instrucciones(instrucciones, tablasimbolos_global)
imprimirTabla(tablasimbolos_global)