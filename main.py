import gramatica as g
import tablasimbolos as TABLASIMBOLOS
from expresiones import *
from instrucciones import *
from cola import *
#=================================================Instrucciones=================================
def procesar_array(instruccion,tablasimbolos,ambito):
    variable=tablasimbolos.obtener(instruccion.variable.valor)
    valor = resolver_expresion(instruccion.valor,tablasimbolos)
    if variable == None:
        array = crear_indice_array(instruccion.indices,valor,tablasimbolos,None)
        crear_variable(instruccion.variable,array,tablasimbolos,ambito)
    elif variable.tipo == TABLASIMBOLOS.TIPO_DATO.ARRAY:
        array = crear_indice_array(instruccion.indices,valor,tablasimbolos,variable)

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
    resultado = resolver_expresion(instruccion.cadena, tablasimbolos)
    if resultado != None:
        print('> ', str(resultado))

def procesar_asignacion(instruccion,tablasimbolos,ambito):
    val = resolver_expresion(instruccion.expresionAsignacion, tablasimbolos)
    if val != None:
        crear_variable(instruccion.expresionVariable,val,tablasimbolos,ambito)

def procesar_etiqueta(instruccion,tablasimbolos,ambito,index_cola):
    agregar_simbolo(instruccion.nombre,
    TABLASIMBOLOS.TIPO_DATO.ETIQUETA,index_cola,tablasimbolos,ambito)

def procesar_goto(instruccion,tablasimbolos):
    etiqueta = tablasimbolos.obtener(instruccion.etiqueta)
    if etiqueta != None : return etiqueta.valor

def procesar_if(instruccion,tablasimbolos):
    valor = resolver_expresion(instruccion.expresionValidar,tablasimbolos)
    etiqueta = tablasimbolos.obtener(instruccion.etiqueta)

    try:
        valor = int(valor)
    except ValueError:
        valor = 0

    if valor >= 1 :
        return etiqueta.valor
    return None

#=================================================Expresiones====================================
def resolver_expresion(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNumerica):
        return resolver_numerica(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionCadena):
        return resolver_cadena(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionPuntero):
        return resolver_puntero(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionLogica):
        return resolver_logica(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionCasteo):
        return resolver_casteo(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionRelacional):
        return resolver_relacional(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionBit):
        return resolver_bit(expresion,tablasimbolos)
    elif isinstance(expresion,ExpresionArrayDeclare):
        return expresion
    elif isinstance(expresion,ExpresionArray):
        return resolver_array(expresion,tablasimbolos)
    return None

def resolver_array(expresion,tablasimbolos):
    variable = tablasimbolos.obtener(expresion.variable)
    if variable == None: return None
    indices = expresion.indices.copy()
    if variable.tipo == TABLASIMBOLOS.TIPO_DATO.ARRAY:
        raiz = resolver_expresion(indices.pop(0),tablasimbolos)
        array = {}
        
        if raiz in variable.valor: array = variable.valor[raiz];
        else: return None

        for i in indices:
            index = resolver_expresion(i,tablasimbolos)
            if index in array['subindices']: array = array['subindices'][index]
            else: 
                print("El indice:"+str(index)+" no existe en la variable: "+str(variable.id))
                return None
        return array['valor']
    elif variable.tipo == (TABLASIMBOLOS.TIPO_DATO.STRING or TABLASIMBOLOS.TIPO_DATO.CHAR):
        if len(expresion.indices)>1 :
            print("índice de la cadena fuera de rango")
            return None
        try:
            indice = resolver_expresion(indices.pop(0),tablasimbolos)
            return variable.valor[indice]
        except IndexError:
            print("índice de la cadena fuera de rango")

    return None

def resolver_bit(expresion,tablasimbolos):
    #Las operaciones unitarias bit solo se pueden aplicar a numeros
    if isinstance(expresion,ExpresionNotBit):
        if isinstance(expresion.expresionNum,ExpresionNumerica):
            valor = resolver_numerica(expresion.expresionNum,tablasimbolos)
            if type(valor) == int:
                return ~valor
        print("No se puede realizar la operación ~ a un tipo diferente de numero entero")
        return None
    
    valor1 = resolver_numerica(expresion.expresionNum1,tablasimbolos)
    valor2 = resolver_numerica(expresion.expresionNum2,tablasimbolos)

    if type(valor1) != int or type(valor2) != int:
        print("No se puede realizar operaciones bit a un tipo diferente de numero entero")
        return None
    
    if valor1 < 0 or valor2 < 0:
        print("No se puede realizar operaciones bit a un numero negativo")
        return None
    
    if expresion.operador == OPERACION_BIT.AND:
        return  valor1 & valor2
    elif expresion.operador == OPERACION_BIT.OR:
        return  valor1 | valor2
    elif expresion.operador == OPERACION_BIT.XOR:
        return  valor1 ^ valor2
    elif expresion.operador == OPERACION_BIT.SHIFTIZQ:
        return valor1 << valor2
    elif expresion.operador == OPERACION_BIT.SHIFTDER:
        return valor1 >> valor2
    return None

def resolver_relacional(expresion,tablasimbolos):
    expresion1 = resolver_expresion(expresion.expresiongeneral1,tablasimbolos)
    expresion2 = resolver_expresion(expresion.expresiongeneral2,tablasimbolos)

    if expresion1 == None or expresion2 == None:
        return None

    if expresion.operador == OPERACION_RELACIONAL.IGUAL:
        if int(expresion1) == int(expresion2):return 1
        else: return 0
    elif expresion.operador == OPERACION_RELACIONAL.DIFERENTE:
        if int(expresion1) != int(expresion2): return 1
        else: return 0
    elif expresion.operador == OPERACION_RELACIONAL.MAYOR_IGUAL:
        if int(expresion1)  >= int(expresion2): return 1
        else: return 0
    elif expresion.operador == OPERACION_RELACIONAL.MENOR_IGUAL:
        if int(expresion1)  <= int(expresion2): return 1
        else: return 0
    elif expresion.operador == OPERACION_RELACIONAL.MAYOR:
        if int(expresion1)  >  int(expresion2): return 1
        else: return 0
    elif expresion.operador == OPERACION_RELACIONAL.MENOR:
        if int(expresion1)  <  int(expresion2): return 1
        else: return 0
    return None
    
def resolver_casteo(expresion,tablasimbolos):
    if isinstance(expresion.expresiongeneral,ExpresionNumerica):
        valor = resolver_numerica(expresion.expresiongeneral,tablasimbolos)
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
    elif expresion.tipo == "char":
        if type(valor) == int:
            if valor < 0 : valor *= -1
            if valor > 255: valor = chr(valor%256)
            else: valor = chr(valor)
        elif type(valor) == float:
            valor = int(valor)
            if valor < 0 : valor *= -1
            if valor > 255: valor = chr(valor%256)
            else: valor = chr(valor)
        elif type(valor) == str:
            valor = valor[0]
    return valor

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
        return resolver_numerica(expresion, tablasimbolos)
    else :
        print('Error: Expresión cadena no válida')

def resolver_numerica(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNumero):
        return expresion.valor
    elif isinstance(expresion,ExpresionNegativo):
        return resolver_numerica(expresion.expresion,tablasimbolos) * -1
    elif isinstance(expresion,ExpresionIdentificador):
        if(tablasimbolos.obtener(expresion.variable.valor)==None):
            print("La variable: \'"+expresion.variable.valor+"\' no esta definida. ")
            return None
        else:
            return tablasimbolos.obtener(expresion.variable.valor).valor
    elif isinstance(expresion,ExpresionBinaria):
        exp1 = resolver_numerica(expresion.exp1, tablasimbolos)
        exp2 = resolver_numerica(expresion.exp2, tablasimbolos)
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
        return abs(resolver_numerica(expresion.expresion,tablasimbolos))

def resolver_logica(expresion,tablasimbolos):
    if isinstance(expresion,ExpresionNot):
        resultado = resolver_numerica(expresion.expresionnumeria,tablasimbolos)
        if resultado == 0:
            return 1
        elif resultado == 1:
            return 0
        else:
            print("Los valores aceptados para el NOT son 1 y 0")
            return None
    else:
        expresion1 = resolver_numerica(expresion.expresion1,tablasimbolos)
        expresion2 = resolver_numerica(expresion.expresion2,tablasimbolos)

        if expresion1 == None or expresion2 == None:
            return None

        if str(expresion1) != "0" and str(expresion1) != "1":
            print("Los valores permitidos para la operaciones logicas son 1 y 0")
            return None
        if str(expresion2) != "0" and str(expresion2) != "1":
            print("Los valores permitidos para la operaciones logicas son 1 y 0")
            return None

        if expresion.operador == "&&":
            return int(expresion1) and int(expresion2)
        elif expresion.operador == "||":
            return int(expresion1) or int(expresion2)
        elif expresion.operador == "xor":
            if(int(expresion1)!=int(expresion2)) : return 1
            else:return 0

#=================================================Funciones extras=================================
def crear_indice_array(indices,valor,tablasimbolos,variable,subindices=None):
    array = {}
    if variable == None:
        subindice = {}
        ultimo_indice = None
        for i in reversed(indices):
            if ultimo_indice != None: valor = None
            indice = resolver_expresion(i,tablasimbolos)
            ultimo_indice = indice
            if type(indice) == int:
                array[indice] = {'tipo':'Numerico','valor':valor,'subindices':subindice}
                if subindices != None: subindice = subindices
                else:subindice = {indice:array[indice]}
            elif type(indice) == str:
                array[indice] = {'tipo':'Asociativo','valor':valor,'subindices':subindice}
                subindice = {indice:array[indice]}
                if subindices != None: subindice = subindices
                else:subindice = {indice:array[indice]}

        array = {ultimo_indice:array[ultimo_indice]}
    else:
        indice_raiz = resolver_expresion(indices[0],tablasimbolos)
        if indice_raiz in variable.valor:
            if not validar_indice_array(indices,variable,valor,tablasimbolos):
                print("No se puede usar un valor escalar como una matriz.")
                return {}
            #se elimina todo el indice y se crea de nuevo todo lo que tiene, 
            #agregando lo nuevo que viene
            array = crear_sub_indice_array(indices,variable,valor,tablasimbolos)
        else:
            #cuando el indice principal para el nuevo no existe
            array = crear_indice_array(indices,valor,tablasimbolos,None)
            variable.valor.update(array)
    return array

def crear_sub_indice_array(indices,variable,valor,tablasimbolos):
    cp_indices = indices.copy()
    index = resolver_expresion(cp_indices.pop(0),tablasimbolos)
    array = variable.valor[index]

    #Obtengo el valor final donde se va adjuntar
    iteracion = 1;
    for i in cp_indices:
        indice = resolver_expresion(i,tablasimbolos)
        if 'subindices' in array:
            if indice not in array['subindices']:
                array = array['subindices']
                if iteracion == len(cp_indices):
                    nuevo = {indice:{'tipo':'Asociativo','valor':valor,'subindices':{}}}
                    array.update(nuevo)
                else:
                    nuevo = {indice:{'tipo':'Asociativo','valor':None,'subindices':{}}}
                    array.update(nuevo)
                    array = array[indice]
        iteracion += 1

def validar_indice_array(indices,array,valor,tablasimbolos):
    cp_indices = indices.copy()
    index = resolver_expresion(cp_indices.pop(0),tablasimbolos)
    var = array.valor[index]
    if var['valor'] != None:
        return False
    # print("aca",index,array.valor[index])
    # simbolo = tablasimbolos.obtener()
    for i in cp_indices:
        indice = resolver_expresion(i,tablasimbolos)
        if indice in var['subindices']:
            valor = var['subindices'][indice]['valor']
            if valor != None:
                return False
    
    return True

def crear_variable(expresionVariable,val,tablasimbolos,ambito):
    if(val != None):
        if(type(val)==int): agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.NUMERO,val,tablasimbolos,ambito)
        elif(type(val)==float): agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.FLOAT,val,tablasimbolos,ambito)
        elif(type(val)==str):
            if(len(val) == 1): agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.CHAR,val,tablasimbolos,ambito)
            else: agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.STRING,val,tablasimbolos,ambito)
        elif(type(val)==ExpresionArrayDeclare):
            agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.ARRAY,{},tablasimbolos,ambito)
        elif(type(val)==dict):
            agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.ARRAY,val,tablasimbolos,ambito)

def agregar_simbolo(id,tipo_dato,val,tablasimbolos,ambito,puntero=0):
    simbolo=tablasimbolos.obtener(id)
    nuevoSimbolo=TABLASIMBOLOS.Simbolo(id, tipo_dato, val,puntero,ambito)
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
        print("id:"+str(simbolo.id)+" valor:"+str(simbolo.valor),"Ambito: "+str(simbolo.declarada_en))
    print("====================================================================================")

def procesar_main(cola,main, tablasimbolos) :
    cola.agregar(main)
    for instruccion in main.instrucciones :
        cola.agregar(instruccion)

    #Primer recorrido para llenar la lista de simbolos
    llenarTabla(cola,tablasimbolos)

    #Ejecutar instrucciones
    # print(len(cola.items))
    Ejecutar(cola,tablasimbolos)

def Ejecutar(cola,tablasimbolos):
    id_actual = 0
    #Etiqueta inicial
    etiqueta_ambito = None
    while id_actual < len(cola.items):
        instruccion = cola.items[id_actual]
        if isinstance(instruccion,Etiqueta) or isinstance(instruccion,EtiquetaMain): 
            etiqueta_ambito = instruccion.nombre
        salto =procesar_instruccion(instruccion,tablasimbolos,etiqueta_ambito,id_actual)
        if salto == None: id_actual +=1
        else: id_actual = salto

def llenarTabla(cola,tablasimbolos):
    id_actual = 0
    #Etiqueta inicial
    etiqueta_ambito = None
    while id_actual < len(cola.items):
        instruccion = cola.items[id_actual]
        if isinstance(instruccion,Etiqueta) or isinstance(instruccion,EtiquetaMain): 
            etiqueta_ambito = instruccion.nombre
            procesar_instruccion(instruccion,tablasimbolos,etiqueta_ambito,id_actual)
        # elif isinstance(instruccion,Asignacion):
        #     procesar_instruccion(instruccion,tablasimbolos,etiqueta_ambito,id_actual)
        id_actual += 1

def procesar_instruccion(instruccion,tablasimbolos,ambito,index):        
    if isinstance(instruccion, Print)       : procesar_print(instruccion, tablasimbolos)
    elif isinstance(instruccion,Asignacion) : procesar_asignacion(instruccion, tablasimbolos,ambito)
    elif isinstance(instruccion,Unset)      : procesar_unset(instruccion,tablasimbolos)
    elif isinstance(instruccion,Read)       : procesar_read(instruccion,tablasimbolos)
    elif isinstance(instruccion,Exit)       : procesar_exit(instruccion,tablasimbolos)
    elif isinstance(instruccion,Array)      : procesar_array(instruccion,tablasimbolos,ambito)
    elif isinstance(instruccion,Etiqueta)   : procesar_etiqueta(instruccion,tablasimbolos,'main',index)
    elif isinstance(instruccion,EtiquetaMain)   : procesar_etiqueta(instruccion,tablasimbolos,None,0)
    elif isinstance(instruccion,Goto)       : return procesar_goto(instruccion,tablasimbolos)
    elif isinstance(instruccion,Ifgoto)     : return procesar_if(instruccion,tablasimbolos)
    else : print('Error: instrucción no válida')
    return None

colaInstruccines = Cola()
f = open("./entrada_arrays.txt", "r")
input = f.read()
#instrucciones contiene el arbol AST
main = g.parse(input)
tablasimbolos_global = TABLASIMBOLOS.TablaDeSimbolos()
procesar_main(colaInstruccines,main, tablasimbolos_global)
imprimirTabla(tablasimbolos_global)