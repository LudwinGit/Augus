from graphviz import Graph
from errores import *

i=0

def inc():
    global i
    i += 1
    return i

def addGramatical(produccion):
    global repgramatical
    global indiceGramatical #la key para la pila donde se ingreara las producciones
    repgramatical[indiceGramatical] = produccion
    indiceGramatical+=1
#
# Ludwin Romario Burrión Imuchac
# 01-06-2020
#

reservadas = {
    'main'  :   'MAIN',
    'goto'  :   'GOTO',
    'unset' :   'UNSET',
    'print' :   'PRINT',
    'read'  :   'READ',
    'exit'  :   'EXIT',
    'int'   :   'INT',
    'float' :   'FLOAT',
    'char'  :   'CHAR',
    'abs'   :   'ABS',
    'array' :   'ARRAY',
    'if'    :   'IF'
}

tokens = [
    'LABEL',

    #VARIABLES
    'TEMPORAL','PARAMETRO','RETURN','RA','PILA','PUNTEROPILA',

    #TIPOS
    'ENTERO','DECIMAL','CADENA','CARACTER',

    #SIMBOLOS
    'DOSPUNTOS','PUNTOCOMA','IGUAL','ABREPARENTESIS','CIERRAPARENTESIS','MENOS',
    'MAS','MUL','DIV','AMPERSAN','RESIDUO','NOT','AND','OR','XOR','COMPARACION',
    'DIFERENTE','MAYORIGUAL','MENORIGUAL','MAYOR','MENOR','NOTBIT','ORBIT','XORBIT',
    'SHIFTIZQ','SHIFTDER','ABRECORCHETE','CIERRACORCHETE'
] + list(reservadas.values())

# Tokens
t_TEMPORAL=             r'\$t[0-9]+'
t_PARAMETRO=            r'\$a[0-9]+'
t_RETURN=               r'\$v[0-9]+'
t_RA=                   r'\$ra'
t_PILA=                 r'\$s[0-9]'
t_PUNTEROPILA=          r'\$sp'
t_DOSPUNTOS=            r'\:'
t_PUNTOCOMA=            r'\;'
t_IGUAL=                r'\='
t_ABREPARENTESIS =      r'\('
t_CIERRAPARENTESIS =    r'\)'
t_MENOS =               r'\-'
t_MAS =                 r'\+'
t_MUL =                 r'\*'
t_DIV =                 r'\/'
t_RESIDUO =             r'\%'
t_AND =                 r'&&'
t_AMPERSAN =            r'&'
t_NOT =                 r'\!'
t_OR =                  r'\|\|'
t_XOR =                 r'xor'
t_COMPARACION=          r'\=\='
t_DIFERENTE=            r'\!\='
t_MAYORIGUAL=           r'\>\='
t_MENORIGUAL=           r'\<\='
t_MAYOR=                r'\>'
t_MENOR=                r'\<'
t_NOTBIT=               r'\~'
t_ORBIT=                r'\|'
t_XORBIT=               r'\^'
t_SHIFTIZQ=             r'\<\<'
t_SHIFTDER=             r'\>\>'
t_ABRECORCHETE=         r'\['
t_CIERRACORCHETE=       r'\]'
# Caracteres ignorados
t_ignore = " \t"

def t_LABEL(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'LABEL')    # Check for reserved words
     return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("DEMASIADO GRANDER PARA CONVERTIR A FLOAT %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("DEMASIADO GRANDE PARA CONVERTIR A INT %d", t.value)
        t.value = 0
    return t

def t_CARACTER(t):
    r'\'.\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADENA(t):
    r'\'.*?\'|\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO(t):
    r'\#.*(\n)?'
    t.lexer.lineno += 1

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    # print("Caracter no reconocido '%s'" % t.value[0])
    error = Error("LEXICO","Caracter no reconocido '%s'" % t.value[0],t.lexer.lineno)
    errores.agregar(error)
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','ABSOLUTO'),
    ('left','MAS','MENOS'),
    ('left','MUL','DIV'),
    ('right','NEGATIVO'),
    )

from instrucciones import *
from expresiones import *

def p_main(t):
    'main   :  MAIN DOSPUNTOS instrucciones'
    id = inc()
    t[0] = EtiquetaMain('main',t[3],id,t.lexer.lineno)
    t.lexer.lineno = 1
    dot.node(str(id),str(t[1]))
    for item in t[3]:
        dot.edge(str(id),str(item.id_dot))
    addGramatical("S -> MAIN Instrucciones")

def p_instrucciones_listado(t):
    '''instrucciones    :   instruccion instrucciones'''
    t[2].append(t[1])
    t[0] = t[2]
    addGramatical("Instrucciones -> Instruccion Instrucciones")

def p_instrucciones_instruccion(t):
    '''instrucciones      :   instruccion'''
    t[0] = [t[1]]
    addGramatical("Instrucciones -> Instruccion")

def p_instrucciones_empty(t):
    'instrucciones      :   empty'
    addGramatical("Instrucciones ->empty")

def p_instruccion(t):
    '''instruccion  :   print_instruccion
                    |   asignacion_instruccion
                    |   unset_instruccion
                    |   read_instruccion
                    |   exit_instruccion
                    |   etiqueta_instruccion
                    |   goto_instruccion
                    |   if_instruccion
                    '''
    t[0] = t[1]
    if isinstance(t[1],Print):addGramatical("Instruccion -> print_instruccion")
    elif isinstance(t[1],Asignacion):addGramatical("Instruccion -> asignacion_instruccion")
    elif isinstance(t[1],Unset):addGramatical("Instruccion -> unset_instruccion")
    elif isinstance(t[1],Read):addGramatical("Instruccion -> read_instruccion")
    elif isinstance(t[1],Exit):addGramatical("Instruccion -> exit_instruccion")
    elif isinstance(t[1],Etiqueta):addGramatical("Instruccion -> etiqueta_instruccion")
    elif isinstance(t[1],Goto):addGramatical("Instruccion -> goto_instruccion")
    elif isinstance(t[1],Ifgoto):addGramatical("Instruccion -> if_instruccion")

def p_if_instruccion(t):
    'if_instruccion         :   IF ABREPARENTESIS expresion_general CIERRAPARENTESIS GOTO LABEL PUNTOCOMA'
    id = inc()
    t[0] = Ifgoto(t[3],t[6],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[3].id_dot))
    addGramatical("if_instruccion ->IF ABREPARENTESIS expresion_general CIERRAPARENTESIS GOTO LABEL PUNTOCOMA")

def p_goto_instruccion(t):
    '''goto_instruccion     :   GOTO LABEL PUNTOCOMA'''
    id=inc()
    t[0] = Goto(t[2],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[2]))
    addGramatical("goto_instruccion ->GOTO LABEL PUNTOCOMA")

def p_etiqueta_instruccion(t):
    '''etiqueta_instruccion :   LABEL DOSPUNTOS'''
    id = inc()
    t[0] = Etiqueta(t[1],id,t.lexer.lineno)
    dot.node(str(id),"Etiqueta:"+str(t[1]))
    addGramatical("etiqueta_instruccion -> LABEL DOSPUNTOS")

def p_exit_instruccion(t):
    'exit_instruccion   :   EXIT PUNTOCOMA'
    id = inc()
    t[0] = Exit(id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    addGramatical("exit_instruccion -> EXIT PUNTOCOMA")

def p_instruccion_read(t):
    'read_instruccion   :   variable IGUAL READ ABREPARENTESIS CIERRAPARENTESIS PUNTOCOMA'
    id = inc()
    t[0] = Read(t[1],id,t.lexer.lineno)
    dot.node(str(id),str(t[3]))
    dot.edge(str(id),str(t[1].id_dot))
    addGramatical('read_instruccion -> variable IGUAL READ ABREPARENTESIS CIERRAPARENTESIS PUNTOCOMA')

def p_instruccion_print(t):
    'print_instruccion : PRINT ABREPARENTESIS expresion_print CIERRAPARENTESIS PUNTOCOMA'
    id = inc()
    t[0] = Print(t[3],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[3].id_dot))
    addGramatical('print_instruccion -> PRINT ABREPARENTESIS expresion_print CIERRAPARENTESIS PUNTOCOMA')

def p_expresion_print(t):
    '''expresion_print      :   expresion_general'''
    t[0] = t[1]
    addGramatical('''expresion_print -> expresion_general''')

def p_instruccion_asignacion(t):
    '''asignacion_instruccion   :   variable IGUAL expresion_asignacion PUNTOCOMA
                                '''
    id = inc()
    t[0] = Asignacion(t[1],t[3],id,t.lexer.lineno)
    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),str(t[2]))
    dot.edge(str(id),str(t[3].id_dot))
    addGramatical('asignacion_instruccion -> variable IGUAL expresion_asignacion PUNTOCOMA')

def p_asignacion_array(t):
    'asignacion_instruccion     :  variable indices IGUAL expresion_asignacion PUNTOCOMA'
    id = inc()
    t[0] = Array(t[1],t[2],t[4],id,t.lexer.lineno)
    dot.node(str(id),"ARRAY")
    dot.edge(str(id),str(t[1].id_dot))
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))
    dot.edge(str(id),str(t[4].id_dot))
    addGramatical('asignacion_instruccion -> variable indices IGUAL expresion_asignacion PUNTOCOMA')

def p_indices_listado(t):
    'indices                    :   indice  indices'
    t[2].append(t[1])
    t[0] = t[2]
    addGramatical('indices -> indice indices')

def p_indices(t):
    'indices                    :   indice'
    t[0] = [t[1]]
    addGramatical('indices -> indice')

def p_indices_empty(t):
    'indices                    :   empty'
    addGramatical('indices -> empty')

def p_indice(t):
    'indice                     :   ABRECORCHETE expresion_general  CIERRACORCHETE'
    t[0] = t[2]
    addGramatical('indice -> ABRECORCHETE expresion_general CIERRACORCHETE')

def p_expresion_asignacion(t):
    '''expresion_asignacion     :   expresion_puntero
                                |   expresion_general
                                |   expresion_casteo
                                |   expresion_bit
                                |   ARRAY ABREPARENTESIS CIERRAPARENTESIS
                                '''
    if t[1] == "array": 
        id = inc()
        t[0] = ExpresionArrayDeclare(id,t.lexer.lineno)
        dot.node(str(id),str("array()"))
    else: t[0] = t[1]
    
    if isinstance(t[1],ExpresionPuntero):
        addGramatical('expresion_asignacion -> expresion_puntero')
    elif isinstance(t[1],ExpresionNumerica) or isinstance(t[1],ExpresionCadena) or isinstance(t[1],ExpresionArray):
        addGramatical('expresion_asignacion -> expresion_general')
    elif isinstance(t[1],ExpresionLogica) or isinstance(t[1],ExpresionRelacional):
        addGramatical('expresion_asignacion -> expresion_general')
    elif isinstance(t[1],ExpresionCasteo):
        addGramatical('expresion_asignacion -> expresion_casteo')
    elif isinstance(t[1],ExpresionBit):
        addGramatical('expresion_asignacion -> expresion_bit')
    else:
        addGramatical('expresion_asignacion -> ARRAY ABREPARENTESIS CIERRAPARENTESIS')

def p_expresion_array(t):
    'expresion_array            :   variable indices'
    id = inc()
    t[0] = ExpresionArray(t[1],t[2],id,t.lexer.lineno)
    dot.node(str(id),str("ARRAY"))
    dot.edge(str(id),str(t[1].id_dot))
    for item in t[2]:
        dot.edge(str(id),str(item.id_dot))
    addGramatical('expresion_array -> variable indices')

def p_expresion_bit(t):
    '''expresion_bit            :   expresion_numerica  AMPERSAN expresion_numerica
                                |   expresion_numerica  ORBIT    expresion_numerica
                                |   expresion_numerica  XORBIT   expresion_numerica
                                |   expresion_numerica  SHIFTIZQ   expresion_numerica
                                |   expresion_numerica  SHIFTDER   expresion_numerica'''
    id = inc()
    if t[2] == "&"  :   
        t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.AND,id,t.lexer.lineno)
        addGramatical('expresion_bit -> expresion_numerica  AMPERSAN expresion_numerica')
    elif t[2] == "|"  :
        t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.OR,id,t.lexer.lineno)
        addGramatical('expresion_bit -> expresion_numerica  ORBIT expresion_numerica')
    elif t[2] == "^"  :
        t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.XOR,id,t.lexer.lineno)
        addGramatical('expresion_bit -> expresion_numerica  XORBIT expresion_numerica')
    elif t[2] == "<<"  :
        t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.SHIFTIZQ,id,t.lexer.lineno)
        addGramatical('expresion_bit -> expresion_numerica  SHIFTIZQ expresion_numerica')
    elif t[2] == ">>"  :
        t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.SHIFTDER,id,t.lexer.lineno)
        addGramatical('expresion_bit -> expresion_numerica  SHIFTDER expresion_numerica')
    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),str(t[2]))
    dot.edge(str(id),str(t[3].id_dot))

def p_expresion_not_bit(t):
    '''expresion_bit            :   NOTBIT  expresion_numerica'''
    id = inc()
    t[0] = ExpresionNotBit(t[2],id,t.lexer.lineno)
    addGramatical('''expresion_bit -> NOTBIT  expresion_numerica''')

def p_expresion_relacional(t):
    '''expresion_relacional     :   expresion_general COMPARACION expresion_general
                                |   expresion_general DIFERENTE expresion_general
                                |   expresion_general MAYORIGUAL expresion_general
                                |   expresion_general MENORIGUAL expresion_general
                                |   expresion_general MAYOR expresion_general
                                |   expresion_general MENOR expresion_general
                                '''
    id = inc()
    if t[2]   == '==' : 
        t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.IGUAL,id,t.lexer.lineno)
        addGramatical('expresion_relacional -> expresion_general COMPARACION expresion_general')
    elif t[2] == '!=' :
        t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.DIFERENTE,id,t.lexer.lineno)
        addGramatical('expresion_relacional -> expresion_general DIFERENTE expresion_general')
    elif t[2] == '>=':
        t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR_IGUAL,id,t.lexer.lineno)
        addGramatical('expresion_relacional -> expresion_general MAYORIGUAL expresion_general')
    elif t[2] == '<=':
        t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR_IGUAL,id,t.lexer.lineno)
        addGramatical('expresion_relacional -> expresion_general MENORIGUAL expresion_general')
    elif t[2] == '>':
        t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR,id,t.lexer.lineno)
        addGramatical('expresion_relacional -> expresion_general MAYOR expresion_general')
    elif t[2] == '<':
        t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR,id,t.lexer.lineno)
        addGramatical('expresion_relacional -> expresion_general MENOR expresion_general')
    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),str(t[2]))
    dot.edge(str(id),str(t[3].id_dot))

#Se puede agregar expresion_logica para una mayor funcionalidad en casteo,relacionales,etc 
def p_expresion_general(t):
    '''expresion_general        :   expresion_numerica       
                                |   expresion_cadena
                                |   expresion_array
                                |   expresion_logica
                                |   expresion_relacional
                                '''
    t[0] = t[1]
    if isinstance(t[1],ExpresionNumerica):addGramatical("expresion_general -> expresion_numerica")
    elif isinstance(t[1],ExpresionNumerica):addGramatical("expresion_general -> expresion_cadena")
    elif isinstance(t[1],ExpresionNumerica):addGramatical("expresion_general -> expresion_array")
    elif isinstance(t[1],ExpresionNumerica):addGramatical("expresion_general -> expresion_logica")
    elif isinstance(t[1],ExpresionNumerica):addGramatical("expresion_general -> expresion_relacional")

def p_expresion_casteo(t):
    '''expresion_casteo         :   ABREPARENTESIS  tipo_variable CIERRAPARENTESIS expresion_general'''
    id = inc()
    t[0] = ExpresionCasteo(t[2],t[4],id,t.lexer.lineno)
    dot.node(str(id),str("casteo"))
    dot.edge(str(id),str(t[2]))
    dot.edge(str(id),str(t[4].id_dot))
    addGramatical('expresion_casteo -> ABREPARENTESIS tipo_variable CIERRAPARENTESIS expresion_general')

def p_expresion_aritmetica(t):
    '''expresion_numerica   : expresion_numerica MAS expresion_numerica
                            | expresion_numerica MENOS expresion_numerica
                            | expresion_numerica MUL expresion_numerica
                            | expresion_numerica DIV expresion_numerica
                            | expresion_numerica RESIDUO expresion_numerica
                            '''
    id = inc()
    if t[2] == '+'  :
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS,id,t.lexer.lineno)
        addGramatical("expresion_numerica -> expresion_numerica MAS expresion_numerica")
    elif t[2] == '-': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS,id,t.lexer.lineno)
        addGramatical("expresion_numerica -> expresion_numerica MENOS expresion_numerica")
    elif t[2] == '*': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MUL,id,t.lexer.lineno)
        addGramatical("expresion_numerica -> expresion_numerica MUL expresion_numerica")
    elif t[2] == '/': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIV,id,t.lexer.lineno)
        addGramatical("expresion_numerica -> expresion_numerica DIV expresion_numerica")
    elif t[2] == '%': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.RESIDUO,id,t.lexer.lineno)
        addGramatical("expresion_numerica -> expresion_numerica RESIDUO expresion_numerica")
    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),str(t[2]))
    dot.edge(str(id),str(t[3].id_dot))

def p_expresion_negativo(t):
    'expresion_numerica : MENOS expresion_numerica %prec NEGATIVO'
    id = inc()
    t[0] = ExpresionNegativo(t[2],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[2].id_dot))
    addGramatical('expresion_numerica -> MENOS expresion_numerica %prec NEGATIVO')

def p_expresion_absoluto(t):
    'expresion_numerica :   ABS ABREPARENTESIS expresion_numerica CIERRAPARENTESIS %prec ABSOLUTO'
    id = inc()
    t[0] = ExpresionAbsoluto(t[3],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[3].id_dot))
    addGramatical('expresion_numerica -> ABS ABREPARENTESIS expresion_numerica CIERRAPARENTESIS %prec ABSOLUTO')

def p_expresion_numero(t):
    '''expresion_numerica       :   ENTERO
                                |   DECIMAL'''
    id = inc()
    t[0] = ExpresionNumero(id,t[1],t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    addGramatical('expresion_numerica -> ENTERO')

def p_asignacion_variable(t):
    '''expresion_numerica       :   variable'''
    id = inc()
    t[0] = ExpresionIdentificador(id,t[1],t.lexer.lineno)
    dot.node(str(id),"Variable")
    dot.edge(str(id),str(t[1].id_dot))
    addGramatical('expresion_numerica -> variable')

def p_expresion_cadena(t):
    '''expresion_cadena         :   CADENA
                                |   CARACTER'''
    id = inc()
    t[0] = ExpresionComilla(t[1],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    addGramatical('expresion_numerica -> CADENA')

def p_expresion_puntero(t):
    '''expresion_puntero  :   AMPERSAN variable'''
    id = inc()
    t[0] = ExpresionPuntero(t[-2],t[2],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[2].id_dot))
    addGramatical('expresion_puntero -> AMPERSAN variable')

def p_expresion_logica(t):
    '''expresion_logica     :   expresion_numerica AND expresion_numerica
                            |   expresion_numerica OR expresion_numerica
                            |   expresion_numerica XOR expresion_numerica'''
    id = inc()
    t[0] = ExpresionLogica(t[1],t[2],t[3],id,t.lexer.lineno)
    dot.edge(str(id),str(t[1].id_dot))
    dot.node(str(id),str(t[2]))
    dot.edge(str(id),str(t[3].id_dot))
    if t[2] == "&&" :addGramatical("expresion_logica -> expresion_numerica AND expresion_numerica")
    elif t[2] == "||" :addGramatical("expresion_logica -> expresion_numerica OR expresion_numerica")
    elif t[2] == "xor": addGramatical("expresion_logica -> expresion_numerica XOR expresion_numerica")


def p_expresion_not(t):
    '''expresion_logica     :   NOT expresion_numerica'''
    id = inc()
    t[0] = ExpresionNot(t[2],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[2].id_dot))
    addGramatical('expresion_logica -> NOT expresion_numerica')

def p_unset_instruccion(t):
    'unset_instruccion    :   UNSET ABREPARENTESIS variable CIERRAPARENTESIS PUNTOCOMA'
    id = inc()
    t[0] = Unset(t[3],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    dot.edge(str(id),str(t[3].id_dot))
    addGramatical('unset_instruccion -> UNSET ABREPARENTESIS variable CIERRAPARENTESIS PUNTOCOMA')

def p_variable(t):
    '''variable     :   TEMPORAL
                    |   PARAMETRO
                    |   RETURN
                    |   RA
                    |   PILA
                    |   PUNTEROPILA
                    '''
    id = inc()
    t[0] = ExpresionVariable(t[1],id,t.lexer.lineno)
    dot.node(str(id),str(t[1]))
    addGramatical("variable -> VARIABLE")

def p_tipo_variable(t):
    '''tipo_variable        :   INT
                            |   FLOAT
                            |   CHAR'''
    id = inc()
    t[0] = t[1]
    dot.node(str(id),str(t[1]))
    addGramatical("tipo_variable -> TIPOVAR")

def p_error(t):
     if t:
        error = Error("SINTACTICO","Error sintactico en: '%s'" % t.value ,t.lexer.lineno)
        errores.agregar(error)
        parser.errok()
     else:
          error = Error("SINTACTICO","Se esperaba el simbolo ';'",-1)
          errores.agregar(error)
          parser.restart()
 
# def p_error(t):
#     print("Error sintáctico",t)
#     # print("Error sintáctico en '%s'" % t.value)

def p_empty(p):
     'empty :'

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    print((token.lexpos - line_start) + 1)

import ply.yacc as yacc
parser = yacc.yacc()

i= 0
dot = Graph()
dot.attr(splines="false")
dot.node_attr.update(shape='circle')
dot.edge_attr.update(color="blue4")
input = ""

errores = Errores()
repgramatical = {}
indiceGramatical = 1

def parse(i) :
    dot.clear()
    input = i
    errores.errores.clear()
    resultado = parser.parse(i)
    return resultado