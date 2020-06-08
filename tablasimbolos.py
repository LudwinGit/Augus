from enum import Enum

class TIPO_DATO(Enum) :
    NUMERO = 1
    FLOAT = 2
    CHAR = 3
    STRING = 4
    ARRAY = 5
    ETIQUETA = 6

class Simbolo() :
    def __init__(self, id, tipo, valor,puntero,etiqueta) :
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.puntero = puntero
        self.declarada_en = etiqueta
        self.dimension = 0

class TablaDeSimbolos() :
    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    
    def obtener(self, id) :
        if not id in self.simbolos :
            return None
        return self.simbolos[id]

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo

    def eliminar(self, simbolo):
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            del self.simbolos[simbolo.id]