from graphviz import Graph

i=0

def inc():
    global i
    i += 1
    return i
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
    print("Caracter no reconocido '%s'" % t.value[0])
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
    t[0] = EtiquetaMain('main',t[3])
    dot.node(str(t[0]),str(t[1]))
    dot.edge(str(t[0]),str(t[3]))
    # t[0] = t[3]

def p_instrucciones_listado(t):
    '''instrucciones    :   instrucciones   instruccion'''
    t[1].append(t[2])
    t[0] = t[1]
    # dot.edge(str(t[0]),str(t[3]))

def p_instrucciones_instruccion(t):
    '''instrucciones      :   instruccion'''
    t[0] = [t[1]]
    dot.node(str(t[0]),"Instrucciones")
    dot.edge(str(t[0]),str(t[1]))

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
    if isinstance(t[1],Asignacion):
        dot.node(str(t[0]),"Asignacion")
    elif isinstance(t[1],Print):
        dot.node(str(t[0]),"Print")
    elif isinstance(t[1],Unset):
        dot.node(str(t[0]),"Unset")
    elif isinstance(t[1],Read):
        dot.node(str(t[0]),"Read")
    elif isinstance(t[1],Exit):
        dot.node(str(t[0]),"Exit")
    elif isinstance(t[1],Goto):
        dot.node(str(t[0]),"Goto")
    elif isinstance(t[1],Ifgoto):
        dot.node(str(t[0]),"IF")

def p_if_instruccion(t):
    'if_instruccion         :   IF ABREPARENTESIS expresion_general CIERRAPARENTESIS GOTO LABEL PUNTOCOMA'
    t[0] = Ifgoto(t[3],t[6])

def p_goto_instruccion(t):
    '''goto_instruccion     :   GOTO LABEL PUNTOCOMA'''
    t[0] = Goto(t[2])

def p_etiqueta_instruccion(t):
    '''etiqueta_instruccion :   LABEL DOSPUNTOS'''
    t[0] = Etiqueta(t[1])

def p_exit_instruccion(t):
    'exit_instruccion   :   EXIT PUNTOCOMA'
    t[0] = Exit()

def p_instruccion_read(t):
    'read_instruccion   :   variable IGUAL READ ABREPARENTESIS CIERRAPARENTESIS PUNTOCOMA'
    t[0] = Read(t[1])

def p_instruccion_print(t):
    'print_instruccion : PRINT ABREPARENTESIS expresion_print CIERRAPARENTESIS PUNTOCOMA'
    t[0] = Print(t[3])

def p_expresion_print(t):
    '''expresion_print      :   expresion_general'''
    t[0] = t[1]

def p_instruccion_asignacion(t):
    '''asignacion_instruccion   :   variable IGUAL expresion_asignacion PUNTOCOMA
                                '''
    t[0] = Asignacion(t[1],t[3])

def p_asignacion_array(t):
    'asignacion_instruccion     :  variable indices IGUAL expresion_asignacion PUNTOCOMA'
    t[0] = Array(t[1],t[2],t[4])

def p_indices_listado(t):
    'indices                    :   indices indice'
    t[1].append(t[2])
    t[0] = t[1]

def p_indices(t):
    'indices                    :   indice'
    t[0] = [t[1]]

def p_indice(t):
    'indice                     :   ABRECORCHETE expresion_general  CIERRACORCHETE'
    t[0] = t[2]

def p_expresion_asignacion(t):
    '''expresion_asignacion     :   expresion_puntero
                                |   expresion_general
                                |   expresion_casteo
                                |   expresion_bit
                                |   ARRAY ABREPARENTESIS CIERRAPARENTESIS
                                '''
    if t[1] == "array": t[0] = ExpresionArrayDeclare()
    else: t[0] = t[1]

def p_expresion_array(t):
    'expresion_array            :   TEMPORAL indices'
    t[0] = ExpresionArray(t[1],t[2])

def p_expresion_bit(t):
    '''expresion_bit            :   expresion_numerica  AMPERSAN expresion_numerica
                                |   expresion_numerica  ORBIT    expresion_numerica
                                |   expresion_numerica  XORBIT   expresion_numerica
                                |   expresion_numerica  SHIFTIZQ   expresion_numerica
                                |   expresion_numerica  SHIFTDER   expresion_numerica'''
    if t[2] == "&"  :   t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.AND)
    if t[2] == "|"  :   t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.OR)
    if t[2] == "^"  :   t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.XOR)
    if t[2] == "<<"  :   t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.SHIFTIZQ)
    if t[2] == ">>"  :   t[0] = t[0] = ExpresionBit(t[1],t[3],OPERACION_BIT.SHIFTDER)

def p_expresion_not_bit(t):
    '''expresion_bit            :   NOTBIT  expresion_numerica'''
    t[0] = ExpresionNotBit(t[2])

def p_expresion_relacional(t):
    '''expresion_relacional     :   expresion_general COMPARACION expresion_general
                                |   expresion_general DIFERENTE expresion_general
                                |   expresion_general MAYORIGUAL expresion_general
                                |   expresion_general MENORIGUAL expresion_general
                                |   expresion_general MAYOR expresion_general
                                |   expresion_general MENOR expresion_general
                                '''
    if t[2]   == '==' : t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.IGUAL)
    elif t[2] == '!=' : t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.DIFERENTE)
    elif t[2] == '>=' : t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR_IGUAL)
    elif t[2] == '<=' : t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR_IGUAL)
    elif t[2] == '>'  : t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MAYOR)
    elif t[2] == '<'  : t[0] = ExpresionRelacional(t[1],t[3],OPERACION_RELACIONAL.MENOR)

#Se puede agregar expresion_logica para una mayor funcionalidad en casteo,relacionales,etc 
def p_expresion_general(t):
    '''expresion_general        :   expresion_numerica       
                                |   expresion_cadena
                                |   expresion_array
                                |   expresion_logica
                                |   expresion_relacional
                                '''
    t[0] = t[1]

def p_expresion_casteo(t):
    '''expresion_casteo         :   ABREPARENTESIS  tipo_variable CIERRAPARENTESIS expresion_general'''
    t[0] = ExpresionCasteo(t[2],t[4])

def p_expresion_aritmetica(t):
    '''expresion_numerica   : expresion_numerica MAS expresion_numerica
                            | expresion_numerica MENOS expresion_numerica
                            | expresion_numerica MUL expresion_numerica
                            | expresion_numerica DIV expresion_numerica
                            | expresion_numerica RESIDUO expresion_numerica
                            '''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MUL)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIV)
    elif t[2] == '%': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.RESIDUO)

def p_expresion_negativo(t):
    'expresion_numerica : MENOS expresion_numerica %prec NEGATIVO'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_absoluto(t):
    'expresion_numerica :   ABS ABREPARENTESIS expresion_numerica CIERRAPARENTESIS %prec ABSOLUTO'
    t[0] = ExpresionAbsoluto(t[3])

def p_expresion_numero(t):
    '''expresion_numerica       :   ENTERO
                                |   DECIMAL'''
    t[0] = ExpresionNumero(t[1])

def p_asignacion_variable(t):
    '''expresion_numerica       :   variable'''
    t[0] = ExpresionIdentificador(t[1])

def p_expresion_cadena(t):
    '''expresion_cadena         :   CADENA
                                |   CARACTER'''
    t[0] = ExpresionComilla(t[1])

def p_expresion_puntero(t):
    '''expresion_puntero  :   AMPERSAN variable'''
    t[0] = ExpresionPuntero(t.stack[2].value,t[2])

def p_expresion_logica(t):
    '''expresion_logica     :   expresion_numerica AND expresion_numerica
                            |   expresion_numerica OR expresion_numerica
                            |   expresion_numerica XOR expresion_numerica'''
    t[0] = ExpresionLogica(t[1],t[2],t[3])

def p_expresion_not(t):
    '''expresion_logica     :   NOT expresion_numerica'''
    t[0] = ExpresionNot(t[2])

def p_unset_instruccion(t):
    'unset_instruccion    :   UNSET ABREPARENTESIS variable CIERRAPARENTESIS PUNTOCOMA'
    t[0] = Unset(t[3])

def p_variable(t):
    '''variable     :   TEMPORAL
                    |   PARAMETRO
                    |   RETURN
                    |   RA'''
    t[0] = ExpresionVariable(t[1])

def p_tipo_variable(t):
    '''tipo_variable        :   INT
                            |   FLOAT
                            |   CHAR'''
    t[0] = t[1]

def p_error(t):
    print("Error sintáctocp",t)
    print("Error sintáctico en '%s'" % t.value)

def p_empty(p):
     'empty :'

import ply.yacc as yacc
parser = yacc.yacc()

i= 0
dot = Graph()
dot.attr(splines="false")
dot.node_attr.update(shape='circle')
dot.edge_attr.update(color="blue4")

def parse(input) :
    dot.clear()
    resultado = parser.parse(input)
    dot.view()
    return resultado