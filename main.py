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
        return resolver_numerico(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionCadena):
        return resolver_cadena(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionPuntero):
        return resolver_puntero(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionLogica):
        return resolver_logica(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionCasteo):
        return resolver_casteo(expresion,tablasimbolos)
    return None

def resolver_casteo(expresion,tablasimbolos):
    if isinstance(expresion.expresiongeneral,ExpresionNumerica):
        valor = resolver_numerico(expresion.expresiongeneral,tablasimbolos)
    elif isinstance(expresion.expresiongeneral,ExpresionCadena):
        valor = resolver_cadena(expresion.expresiongeneral,tablasimbolos)
    else: return None

    if expresion.tipo == "int":
        if type(valor) == float: valor=int(valor)
        elif type(valor) == str:
            if len(valor) == 1:
                valor = ord(valor)
            else:
                valor = ord(valor[0])
    elif expresion.tipo == "float":
        if type(valor) == int: valor=float(valor)
        elif type(valor) == str:
            if len(valor) == 1:
                valor = ord(valor)
            else:
                valor = ord(valor[0])
            valor = float(valor)
    return valor

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
        return resolver_numerico(expresion, tablasimbolos)
    else :
        print('Error: Expresión cadena no válida')

def resolver_numerico(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNumero):
        return expresion.valor
    elif isinstance(expresion,ExpresionNegativo):
        return resolver_numerico(expresion.expresion,tablasimbolos) * -1
    elif isinstance(expresion,ExpresionIdentificador):
        if(tablasimbolos.obtener(expresion.variable.valor)==None):
            print("La variable: \'"+expresion.variable.valor+"\' no esta definida. ")
            return None
        else:
            return tablasimbolos.obtener(expresion.variable.valor).valor
    elif isinstance(expresion,ExpresionBinaria):
        exp1 = resolver_numerico(expresion.exp1, tablasimbolos)
        exp2 = resolver_numerico(expresion.exp2, tablasimbolos)
        if type(exp1)==str and type(exp2)==str and expresion.operador == OPERACION_ARITMETICA.MAS: return (str(exp1)+str(exp2))
        if type(exp1)==str or type(exp2)==str: 
            print("No se puede realizar la operación entre una cadena y un numero.")
            return None
        if expresion.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
        if expresion.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if expresion.operador == OPERACION_ARITMETICA.MUL : return exp1 * exp2
        if expresion.operador == OPERACION_ARITMETICA.DIV : return exp1 / exp2
        if expresion.operador == OPERACION_ARITMETICA.RESIDUO : return exp1 / exp2
    elif isinstance(expresion,ExpresionAbsoluto):
        return abs(resolver_numerico(expresion.expresion,tablasimbolos))

def resolver_logica(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNot):
        resultado = resolver_numerico(expresion.expresionnumeria,tablasimbolos)
        if resultado == 0:
            return 1
        elif resultado == 1:
            return 0
        else:
            print("Los valores aceptados para el NOT son 1 y 0")
            return None
    else:
        expresion1 = resolver_numerico(expresion.expresion1,tablasimbolos)
        expresion2 = resolver_numerico(expresion.expresion2,tablasimbolos)

        if expresion1 == None or expresion2 == None:
            return None

        if expresion1 != 0 and expresion1 != 1:
            print("Los valores permitidos para la operaciones logicas son 1 y 0")
            return None
        if expresion2 != 0 and expresion2 != 1:
            print("Los valores permitidos para la operaciones logicas son 1 y 0")
            return None

        if expresion.operador == "&&":
            return expresion1 and expresion2
        elif expresion.operador == "||":
            return expresion1 or expresion2
        elif expresion.operador == "xor":
            if(expresion1!=expresion2) :
                return 1
            else:
                return 0


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
    print("==================================TABLA SIMBOLOS====================================")
    for s in tablasimbolos.simbolos:
        simbolo = tablasimbolos.obtener(s)
        print("id:"+str(simbolo.id) +" valor:"+str(simbolo.valor)+" puntero:"+str(simbolo.puntero))
    print("====================================================================================")

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