
class elemento:
    def __init__(self,nombre, x1, x2, y1, y2, tamx, tamy, medx, medy, area, centrox=0, centroy=0 ):
        self.nombre = nombre
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.tamx = tamx
        self.tamy = tamy
        self.medx = medx
        self.medy = medy
        self.area = area
        self.centrox = centrox
        self.centroy = centroy


PERSON_MARGEN=0.15
CAR_MARGEN=0.15


##--------------------------------------------------------------------------------------------------------------------##
## FUNCION DEL SABER ##
## ESTA FUNCION ES LA QUE DECIDE QUE HACER ##
##--------------------------------------------------------------------------------------------------------------------##

def oraculo(zonadeteccion, objeto):

#DECISION REFERENTE A PERSONAS
    if ((objeto.nombre == 'person') and 
    ((objeto.area > zonadeteccion.area*PERSON_MARGEN) and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 )) and 
    (objeto.centrox > zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)))
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "STOP"
    if ((objeto.nombre == 'person') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 ) and 
    (objeto.centrox > zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 ) 
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "LEFT"
    if ((objeto.nombre == 'person') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 ) and 
    (objeto.centrox > zonadeteccion.x1 and 
     objeto.centrox < zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3))) 
    ):
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "RIGHT"

#DECISION REFERENTE A COCHES
    if ((objeto.nombre == 'car') and 
    ((objeto.area > zonadeteccion.area*PERSON_MARGEN) and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 )) and 
    (objeto.centrox > zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)))
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "STOP"
    if ((objeto.nombre == 'car') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 ) and 
    (objeto.centrox > zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 ) 
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "RIGHT"
    if ((objeto.nombre == 'car') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 ) and 
    (objeto.centrox > zonadeteccion.x1 and 
     objeto.centrox < zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3))) 
    ):
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "LEFT"   

#DECISION REFERENTE A SI NO ES NADA DE LO ANTERIOR
    if (objeto.nombre != 'person' or objeto.nombre != 'car'):
        #print("oArea: "+str(objeto.area))
        #print("mArea: "+str(zonadeteccion.area*PERSON_MARGEN))
        #print(objeto.nombre) 
        return "GO"




