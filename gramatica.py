#
# Ludwin Romario Burrión Imuchac
# 01-06-2020
#

tokens = [
    #RESERVADAS
    'MAIN','LABEL','GOTO','UNSET','PRINT','READ','EXIT','INT','FLOAT','CHAR','ABS',
    #VARIABLES
    'TEMPORAL','PARAMETRO','RETURN','RA','PILA','PUNTEROPILA',

    #TIPOS
    'ENTERO','DECIMAL','CADENA','CARACTER',

    #SIMBOLOS
    'DOSPUNTOS','PUNTOCOMA','IGUAL','ABREPARENTESIS','CIERRAPARENTESIS','MENOS',
    'MAS','MUL','DIV','AMPERSAN','RESIDUO','NOT','AND','OR','XOR','COMPARACION',
    'DIFERENTE','MAYORIGUAL','MENORIGUAL','MAYOR','MENOR','NOTBIT'
]

# Tokens
t_MAIN=                 r'main'
t_LABEL=                r'label'
t_GOTO=                 r'goto'
t_UNSET=                r'unset'
t_PRINT=                r'print'
t_READ=                 r'read'
t_EXIT=                 r'exit'
t_INT=                  r'int'
t_FLOAT=                r'float'
t_CHAR=                 r'char'
t_ABS=                  r'abs'
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
# Caracteres ignorados
t_ignore = " \t"

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

def p_init(t):
    'init   :   instrucciones'
    t[0] = t[1]

def p_instrucciones_listado(t):
    '''instrucciones    :   instrucciones instruccion'''
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t):
    '''instrucciones      :   instruccion'''
    t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion  :   print_instruccion
                    |   asignacion_instruccion
                    |   unset_instruccion
                    |   read_instruccion
                    |   exit_instruccion
                                        '''
    t[0] = t[1]

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
    '''expresion_print      :   expresion_cadena
                            |   expresion_numerica'''
    t[0] = t[1]

def p_instruccion_asignacion(t):
    'asignacion_instruccion    :   variable IGUAL expresion_asignacion PUNTOCOMA'
    t[0] = Asignacion(t[1],t[3])

def p_expresion_asignacion(t):
    '''expresion_asignacion     :   expresion_puntero
                                |   expresion_logica
                                |   expresion_general
                                |   expresion_casteo
                                |   expresion_relacional
                                |   expresion_bit
                                '''
    t[0] = t[1]

def p_expresion_bit(t):
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
                                |   expresion_cadena'''
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
                    |   PARAMETRO'''
    t[0] = ExpresionVariable(t[1])

def p_tipo_variable(t):
    '''tipo_variable        :   INT
                            |   FLOAT
                            |   CHAR'''
    t[0] = t[1]

def p_error(t):
    print("Error sintáctocp",t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)