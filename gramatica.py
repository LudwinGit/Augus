#
# Ludwin Romario Burrión Imuchac
# 01-06-2020
#

tokens = [
    #RESERVADAS
    'MAIN','LABEL','GOTO','UNSET','PRINT','READ','EXIT','INT','FLOAT','CHAR',
    #REGISTROS
    'TEMPORAL','PARAMETRO','RETURN','RA','PILA','PUNTEROPILA',

    #TIPOS
    'ENTERO','DECIMAL','CADENA','CARACTER',

    #SIMBOLOS
    'DOSPUNTOS','PUNTOCOMA','IGUAL','ABREPARENTESIS','CIERRAPARENTESIS'
]

# Tokens
t_MAIN= r'main'
t_LABEL=r'label'
t_GOTO=r'goto'
t_UNSET=r'unset'
t_PRINT=r'print'
t_READ=r'read'
t_EXIT=r'exit'
t_INT=r'int'
t_FLOAT=r'float'
t_CHAR=r'char'
t_TEMPORAL= r'\$t[0-9]+'
t_PARAMETRO= r'\$a[0-9]+'
t_RETURN= r'\$v[0-9]+'
t_RA= r'\$ra'
t_PILA= r'\$s[0-9]'
t_PUNTEROPILA= r'\$sp'
t_DOSPUNTOS= r'\:'
t_PUNTOCOMA= r'\;'
t_IGUAL= r'\='
t_ABREPARENTESIS = r'\('
t_CIERRAPARENTESIS = r'\)'

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
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO(t):
    r'//.*\n'
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
                                        '''
    t[0] = t[1]

def p_instruccion_print(t):
    'print_instruccion : PRINT ABREPARENTESIS expresion_cadena CIERRAPARENTESIS PUNTOCOMA'
    t[0] = Print(t[3])

def p_instruccion_asignacion(t):
    'asignacion_instruccion    :   TEMPORAL IGUAL expresion_asignacion PUNTOCOMA'
    t[0] = Asignacion(t[1],t[3])

def p_asignacion_numero(t):
    '''expresion_asignacion     :   ENTERO
                                |   DECIMAL'''
    t[0] = ExpresionNumero(t[1])

def p_asignacion_cadena(t):
    '''expresion_asignacion     :   CADENA
                                |   CARACTER'''
    t[0] = ExpresionComilla(t[1])

def p_asignacion_copia(t):
    '''expresion_asignacion     :   TEMPORAL'''
    t[0] = ExpresionIdentificador(t[1])

def p_expresion_cadena(t):
    'expresion_cadena : CADENA'
    t[0] = ExpresionComilla(t[1])

# def p_expresion_numerica:

# def p_expresion_array:

# def p_instruccion
# # def p_main(t):
# #     'expresion : MAIN'


import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)