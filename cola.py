from instrucciones import *

class Cola():
    def __init__(self):
        self.items=[]

    def agregar(self,item):
        self.items.append(item)

    def obtener(self):
        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola esta vacia")

    def getinstruccion(self,indice):
        try:
            return self.items[indice]
        except:
            raise ValueError("El indice ese incorrecto")
    
    def getIndexEtiqueta(self,etiqueta):
        index = 0
        for item in self.items:
            if isinstance(item,Etiqueta) or isinstance(item,EtiquetaMain):
                if item.nombre == etiqueta:
                    return index
            index +=1 
        return None