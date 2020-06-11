import gramatica as g
import tablasimbolos as TABLASIMBOLOS
from expresiones import *
from instrucciones import *
from cola import *

class Analizador():

    def __init__(self):
        self.cola = None
        self.main = None
        self.salida = ""
        self.id_debug = 0
        self.ast = None
        self.etiqueta_debug=""

    def run(self,entrada):
        self.cola = Cola()
        self.main = g.parse(entrada)
        self.tablasimbolos = TABLASIMBOLOS.TablaDeSimbolos({})
        self.salida = ""
        self.id_debug = 0
        self.procesar_main()


#=================================================Instrucciones=================================
    def procesar_array(self,instruccion,ambito):
        variable=self.tablasimbolos.obtener(instruccion.variable.valor)
        valor = self.resolver_expresion(instruccion.valor)
        if isinstance(valor,ExpresionArrayDeclare): valor = None
        if variable == None:
            array = self.crear_indice_array(instruccion.indices,valor,None)
            self.crear_variable(instruccion.variable,array,ambito)
        elif variable.tipo == TABLASIMBOLOS.TIPO_DATO.ARRAY:
            # if isinstance(valor,ExpresionArrayDeclare): 
            #     self.resetear_indice(instruccion.indices,variable)
            #     return
            array = self.crear_indice_array(instruccion.indices,valor,variable)

    # def resetear_indice(indices,variable):


    def procesar_exit(self,instruccion):
        # exit()
        self.salida +="==============================FIN DEL PROGRAMA==============================\n"
        return -1

    def procesar_read(self,instruccion):
        val = print("simula")
        # crear_variable(instruccion.id,val,tablasimbolos)

    def procesar_unset(self,instruccion):
        simbolo = self.tablasimbolos.obtener(instruccion.variable.valor)
        if(simbolo==None):
            self.salida +="Error sematico:La variable: \'"+str(instruccion.variable.valor)+"\' no esta definida \n"
        else:
            self.tablasimbolos.eliminar(simbolo)
            self.salida +=">Variable eliminada \n"

    def procesar_print(self,instruccion) :
        resultado = self.resolver_expresion(instruccion.cadena)
        if resultado != None:
            if type(resultado) == dict:
                self.salida +="Error sematico: No se puede imprimir un vector.\n"
            elif ord(str(resultado)[0]) == 92:
                self.salida += ">\n"
            else:
                self.salida += ">"+str(resultado)+"\n"

    def procesar_asignacion(self,instruccion,ambito):
        val = self.resolver_expresion(instruccion.expresionAsignacion)
        if val != None:
            self.crear_variable(instruccion.expresionVariable,val,ambito)

    def procesar_etiqueta(self,instruccion,ambito,index_cola):
        self.agregar_simbolo(instruccion.nombre,
        TABLASIMBOLOS.TIPO_DATO.ETIQUETA,index_cola,ambito)

    def procesar_goto(self,instruccion):
        etiqueta = self.tablasimbolos.obtener(instruccion.etiqueta)
        if etiqueta != None : return etiqueta.valor

    def procesar_if(self,instruccion):
        valor = self.resolver_expresion(instruccion.expresionValidar)
        etiqueta = self.tablasimbolos.obtener(instruccion.etiqueta)

        try:
            valor = int(valor)
        except ValueError:
            valor = 0

        if valor >= 1 :
            return etiqueta.valor
        return None

#=================================================Expresiones====================================
    def resolver_expresion(self,expresion):
        if isinstance(expresion,ExpresionNumerica):
            return self.resolver_numerica(expresion)
        elif isinstance(expresion,ExpresionCadena):
            return self.resolver_cadena(expresion)
        elif isinstance(expresion,ExpresionPuntero):
            return self.resolver_puntero(expresion)
        elif isinstance(expresion,ExpresionLogica):
            return self.resolver_logica(expresion)
        elif isinstance(expresion,ExpresionCasteo):
            return self.resolver_casteo(expresion)
        elif isinstance(expresion,ExpresionRelacional):
            return self.resolver_relacional(expresion)
        elif isinstance(expresion,ExpresionBit):
            return self.resolver_bit(expresion)
        elif isinstance(expresion,ExpresionArrayDeclare):
            return expresion
        elif isinstance(expresion,ExpresionArray):
            return self.resolver_array(expresion)
        return None

    def resolver_array(self,expresion):
        variable = self.tablasimbolos.obtener(expresion.variable)
        if variable == None: return None
        indices = expresion.indices.copy()
        if variable.tipo == TABLASIMBOLOS.TIPO_DATO.ARRAY:
            raiz = self.resolver_expresion(indices.pop(0))
            array = {}
            
            if raiz in variable.valor: array = variable.valor[raiz];
            else: return None

            for i in indices:
                index = self.resolver_expresion(i)
                if index in array['subindices']: array = array['subindices'][index]
                else: 
                    self.salida += "Error sematico: El indice \'"+str(index)+"\' no existe en la variable: "+str(variable.id) + "\n"
                    return None
            return array['valor']
        elif variable.tipo == (TABLASIMBOLOS.TIPO_DATO.STRING or TABLASIMBOLOS.TIPO_DATO.CHAR):
            if len(expresion.indices)>1 :
                self.salida += "Error sematico: índice de la cadena fuera de rango \'"+str(variable.id)+"\'"+ "\n"
                return None
            try:
                indice = self.resolver_expresion(indices.pop(0))
                return variable.valor[indice]
            except IndexError:
                self.salida += "Error sematico: índice de la cadena fuera de rango \'"+str(variable.id)+"\'"+ "\n"

        return None

    def resolver_bit(self,expresion):
        #Las operaciones unitarias bit solo se pueden aplicar a numeros
        if isinstance(expresion,ExpresionNotBit):
            if isinstance(expresion.expresionNum,ExpresionNumerica):
                valor = self.resolver_numerica(expresion.expresionNum)
                if type(valor) == int:
                    return ~valor
            self.salida += "Error sematico: No se puede realizar la operación ~ a un tipo diferente de numero entero\n"
            return None
        
        valor1 = self.resolver_numerica(expresion.expresionNum1)
        valor2 = self.resolver_numerica(expresion.expresionNum2)

        if type(valor1) != int or type(valor2) != int:
            self.salida += "Error sematico: No se puede realizar operaciones bit a un tipo diferente de numero entero\n"
            return None
        
        if valor1 < 0 or valor2 < 0:
            self.salida += "Error sematico: No se puede realizar operaciones bit a un numero negativo\n"
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

    def resolver_relacional(self,expresion):
        expresion1 = self.resolver_expresion(expresion.expresiongeneral1)
        expresion2 = self.resolver_expresion(expresion.expresiongeneral2)

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
        
    def resolver_casteo(self,expresion):
        if isinstance(expresion.expresiongeneral,ExpresionNumerica):
            valor = self.resolver_numerica(expresion.expresiongeneral)
        elif isinstance(expresion.expresiongeneral,ExpresionCadena):
            valor = self.resolver_cadena(expresion.expresiongeneral)
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

    def resolver_puntero(self,expresion):
        simboloPuntero = self.tablasimbolos.obtener(expresion.puntero.valor)
        if(simboloPuntero == None):
            self.salida += "Error semantico: la variable \'"+expresion.puntero.valor+"\' no esta definida\n"
            return None
        else: 
            self.agregar_simbolo(expresion.variable.valor,TABLASIMBOLOS.TIPO_DATO.STRING,simboloPuntero.valor,simboloPuntero.id)
            return simboloPuntero.valor

    def resolver_cadena(self,expresion) :
        if isinstance(expresion, ExpresionComilla) :
            return expresion.valor
        elif isinstance(expresion, ExpresionNumerica) :
            return self.resolver_numerica(expresion)
        else :
            self.salida += "Error semantico: Expresión cadena no válida\n"

    def resolver_numerica(self,expresion):
        if isinstance(expresion,ExpresionNumero):
            return expresion.valor
        elif isinstance(expresion,ExpresionNegativo):
            return self.resolver_numerica(expresion.expresion) * -1
        elif isinstance(expresion,ExpresionIdentificador):
            if(self.tablasimbolos.obtener(expresion.variable.valor)==None):
                self.salida += "Error semantico: la variable \'"+expresion.variable.valor+"\' no esta definida.\n"
                return None
            else:
                return self.tablasimbolos.obtener(expresion.variable.valor).valor
        elif isinstance(expresion,ExpresionBinaria):
            exp1 = self.resolver_numerica(expresion.exp1)
            exp2 = self.resolver_numerica(expresion.exp2)
            if type(exp1)==str and type(exp2)==str and expresion.operador == OPERACION_ARITMETICA.MAS: return (str(exp1)+str(exp2))
            if type(exp1)==str or type(exp2)==str: 
                self.salida += "Error semantico: No se puede realizar la operación aritmetica entre una cadena y un numero.\n"
                return None
            if expresion.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
            if expresion.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
            if expresion.operador == OPERACION_ARITMETICA.MUL : return exp1 * exp2
            if expresion.operador == OPERACION_ARITMETICA.DIV : return exp1 / exp2
            if expresion.operador == OPERACION_ARITMETICA.RESIDUO : return exp1 / exp2
        elif isinstance(expresion,ExpresionAbsoluto):
            return abs(self.resolver_numerica(expresion.expresion))

    def resolver_logica(self,expresion):
        if isinstance(expresion,ExpresionNot):
            resultado = self.resolver_numerica(expresion.expresionnumeria)
            if resultado == 0:
                return 1
            elif resultado == 1:
                return 0
            else:
                self.salida += "Error semantico: los valores aceptados para el NOT son 1 y 0\n"
                return None
        else:
            expresion1 = self.resolver_numerica(expresion.expresion1)
            expresion2 = self.resolver_numerica(expresion.expresion2)

            if expresion1 == None or expresion2 == None:
                return None

            if str(expresion1) != "0" and str(expresion1) != "1":
                self.salida += "Error semantico: los valores permitidos para la operaciones logicas son 1 y 0\n"
                return None
            if str(expresion2) != "0" and str(expresion2) != "1":
                self.salida += "Error semantico: los valores permitidos para la operaciones logicas son 1 y 0\n"
                return None

            if expresion.operador == "&&":
                return int(expresion1) and int(expresion2)
            elif expresion.operador == "||":
                return int(expresion1) or int(expresion2)
            elif expresion.operador == "xor":
                if(int(expresion1)!=int(expresion2)) : return 1
                else:return 0

#=================================================Funciones extras=================================
    def crear_indice_array(self,indices,valor,variable,subindices=None):
        array = {}
        if variable == None:
            subindice = {}
            ultimo_indice = None
            for i in reversed(indices):
                if ultimo_indice != None: valor = None
                indice = self.resolver_expresion(i)
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
            indice_raiz = self.resolver_expresion(indices[0])
            if indice_raiz in variable.valor:
                if not self.validar_indice_array(indices,variable,valor):
                    self.salida += "Error semantico: no se puede usar un valor escalar como una matriz.\n"
                    return {}
                #se elimina todo el indice y se crea de nuevo todo lo que tiene, 
                #agregando lo nuevo que viene
                array = self.crear_sub_indice_array(indices,variable,valor)
            else:
                #cuando el indice principal para el nuevo no existe
                array = self.crear_indice_array(indices,valor,None)
                variable.valor.update(array)
        return array

    def crear_sub_indice_array(self,indices,variable,valor):
        cp_indices = indices.copy()
        index = self.resolver_expresion(cp_indices.pop(0))
        array = variable.valor[index]
        #Obtengo el valor final donde se va adjuntar
        if type(array['valor']) == str:
            if len(cp_indices) == 1:
                index = self.resolver_expresion(cp_indices.pop(0))
                if type(index) == int:
                    if len(array['valor']) >= index:
                        array['valor'] = array['valor'][:index]+str(valor)+array['valor'][index+1:]
                    else:
                        i = index - (len(array['valor'])-1)
                        while i >1:
                            array['valor']+=" "
                            i -= 1
                        array['valor'] += str(valor)
                    return
        elif array['valor'] == None and len(cp_indices) == 0:
            array['valor'] = valor
            return

        iteracion = 1;
        for i in cp_indices:
            index = self.resolver_expresion(i)
            if 'subindices' in array:
                if index not in array['subindices']:
                    if type(array['valor']) == str:
                        if type(index) == int:
                            if len(array['valor']) >= index:
                                array['valor'] = array['valor'][:index]+str(valor)+array['valor'][index+1:]
                            else:
                                i = index - (len(array['valor'])-1)
                                while i >1:
                                    array['valor']+=" "
                                    i -= 1
                                array['valor'] += str(valor)
                            return
                    array = array['subindices']
                    if iteracion == len(cp_indices):
                        nuevo = {index:{'tipo':'Asociativo','valor':valor,'subindices':{}}}
                        array.update(nuevo)
                    else:
                        nuevo = {index:{'tipo':'Asociativo','valor':None,'subindices':{}}}
                        array.update(nuevo)
                        array = array[index]
                else:
                    if iteracion == len(cp_indices):
                        array['subindices'][index]['valor'] =valor
                    else:
                        array = array['subindices'][index]

            iteracion += 1

    def validar_indice_array(self,indices,array,valor):
        cp_indices = indices.copy()
        index = self.resolver_expresion(cp_indices.pop(0))
        var = array.valor[index]
        if var['valor'] != None:
            if type(var['valor']) != str:
                return False
        # print("aca",index,array.valor[index])
        # simbolo =.obtener()
        count = len(cp_indices)
        for i in cp_indices:
            indice = self.resolver_expresion(i)
            if indice in var['subindices']:
                valor = var['subindices'][indice]['valor']
                if valor != None:
                    if type(valor) != str:
                        if count == 1:
                            return True
                    return False
            count -= 1
        return True

    def crear_variable(self,expresionVariable,val,ambito):
        if(val != None):
            if(type(val)==int): self.agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.NUMERO,val,ambito)
            elif(type(val)==float): self.agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.FLOAT,val,ambito)
            elif(type(val)==str):
                if(len(val) == 1): self.agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.CHAR,val,ambito)
                else: self.agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.STRING,val,ambito)
            elif(type(val)==ExpresionArrayDeclare):
                self.agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.ARRAY,{},ambito)
            elif(type(val)==dict):
                self.agregar_simbolo(expresionVariable.valor,TABLASIMBOLOS.TIPO_DATO.ARRAY,val,ambito)

    def agregar_simbolo(self,id,tipo_dato,val,ambito,puntero=0):
        simbolo=self.tablasimbolos.obtener(id)
        nuevoSimbolo=TABLASIMBOLOS.Simbolo(id, tipo_dato, val,puntero,ambito)
        if(simbolo == None):
            self.tablasimbolos.agregar(nuevoSimbolo)
        else:
            if(str(simbolo.puntero)!="0"):
                nuevoSimbolo.puntero = simbolo.puntero
                actualizarvalorpuntero = self.tablasimbolos.obtener(simbolo.puntero)
                actualizarvalorpuntero.valor = val

            for s in self.tablasimbolos.simbolos:
                sim = self.tablasimbolos.obtener(s)
                if(str(sim.puntero)==str(id)):
                    sim.valor = val
            self.tablasimbolos.actualizar(nuevoSimbolo)

    def imprimirTabla(self):
        print("==================================TABLA SIMBOLOS====================================")
        for s in self.tablasimbolos.simbolos:
            simbolo = self.tablasimbolos.obtener(s)
            print("id:"+str(simbolo.id)+" valor:"+str(simbolo.valor),"Ambito: "+str(simbolo.declarada_en))
        print("====================================================================================")

    def debugTablaPrint(self):
        self.salida = "=======================TABLA SIMBOLOS====================\n"
        for s in self.tablasimbolos.simbolos:
            simbolo = self.tablasimbolos.obtener(s)
            self.salida += "____________________________________________________"+"\n"
            self.salida += "||id:"+str(simbolo.id)+"||valor:"+str(simbolo.valor)+"||Ambito: "+str(simbolo.declarada_en)+"||\n"
            self.salida += "____________________________________________________"+"\n"
        self.salida += "=========================================================\n"

    def procesar_main(self) :
        self.cola.agregar(self.main)
        for instruccion in self.main.instrucciones :
            self.cola.agregar(instruccion)

        #Primer recorrido para llenar la lista de simbolos
        self.llenarTabla()

        #Ejecutar instrucciones
        # print(len(cola.items))
        # self.Ejecutar()

    def Ejecutar(self):
        id_actual = 0
        #Etiqueta inicial
        etiqueta_ambito = None
        while id_actual < len(self.cola.items):
            instruccion = self.cola.items[id_actual]
            if isinstance(instruccion,Etiqueta) or isinstance(instruccion,EtiquetaMain): 
                etiqueta_ambito = instruccion.nombre
            salto =self.procesar_instruccion(instruccion,etiqueta_ambito,id_actual)
            if salto == None: id_actual +=1
            elif salto ==-1: id_actual = len(self.cola.items)
            else: id_actual = salto
        self.imprimirTabla()
        g.dot.view()
    
    def Debug(self):
        if self.id_debug == len(self.cola.items): return False
        instruccion = self.cola.items[self.id_debug]
        if isinstance(instruccion,Etiqueta) or isinstance(instruccion,EtiquetaMain): 
            self.etiqueta_debug = instruccion.nombre
        salto =self.procesar_instruccion(instruccion,self.etiqueta_debug,self.id_debug)
        if salto == None: self.id_debug +=1
        elif salto ==-1: self.id_debug = len(self.cola.items)
        else: self.id_debug = salto
        self.debugTablaPrint()
        return True

    def llenarTabla(self):
        id_actual = 0
        #Etiqueta inicial
        etiqueta_ambito = None
        while id_actual < len(self.cola.items):
            instruccion = self.cola.items[id_actual]
            if isinstance(instruccion,Etiqueta) or isinstance(instruccion,EtiquetaMain): 
                etiqueta_ambito = instruccion.nombre
                self.procesar_instruccion(instruccion,etiqueta_ambito,id_actual)
            # elif isinstance(instruccion,Asignacion):
            #     procesar_instruccion(instruccion,tablasimbolos,etiqueta_ambito,id_actual)
            id_actual += 1

    def procesar_instruccion(self,instruccion,ambito,index):        
        if isinstance(instruccion, Print)       : self.procesar_print(instruccion)
        elif isinstance(instruccion,Asignacion) : self.procesar_asignacion(instruccion,ambito)
        elif isinstance(instruccion,Unset)      : self.procesar_unset(instruccion)
        elif isinstance(instruccion,Read)       : self.procesar_read(instruccion)
        elif isinstance(instruccion,Exit)       : return self.procesar_exit(instruccion)
        elif isinstance(instruccion,Array)      : self.procesar_array(instruccion,ambito)
        elif isinstance(instruccion,Etiqueta)   : self.procesar_etiqueta(instruccion,'main',index)
        elif isinstance(instruccion,EtiquetaMain)   : self.procesar_etiqueta(instruccion,None,0)
        elif isinstance(instruccion,Goto)       : return self.procesar_goto(instruccion)
        elif isinstance(instruccion,Ifgoto)     : return self.procesar_if(instruccion)
        else : self.salida += "Error semantico: instrucción no valida\n"
        return None

# analizador = Analizador("entrada.txt")
# print(analizador.salida)