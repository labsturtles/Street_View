
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


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


PERSON_MARGEN=0.05#0.15
CAR_MARGEN=0.05#0.15

zonadeteccion=elemento("zonadeteccion",0, 0, 0, 0, 0, 0, 0, 0, 0)

def cuentaPersonas(contenedor):
    p=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'person'):
            p=p+1
    return p
def personasIzquierda(contenedor):
    i=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'person'):
            if (posicionObjeto(objeto, PERSON_MARGEN) == 'IZQUIERDA'):
                 i=i+1
    return i
def personasCentro(contenedor):
    c=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'person'):
            if (posicionObjeto(objeto, PERSON_MARGEN) == 'CENTRO'): 
                 c=c+1
    return c
def personasDerecha(contenedor):
    d=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'person'):
            if (posicionObjeto(objeto, PERSON_MARGEN) == 'DERECHA'):
                 d=d+1
    return d



def cuentaCoches(contenedor):
    c=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car'):
            c=c+1
    return c
def cochesIzquierda(contenedor):
    i=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car'):
            if (posicionObjeto(objeto, CAR_MARGEN) == 'IZQUIERDA'):
                 i=i+1
    return i
def cochesCentro(contenedor):
    c=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car'):
            if (posicionObjeto(objeto, CAR_MARGEN) == 'CENTRO'): 
                 c=c+1
    return c
def cochesDerecha(contenedor):
    d=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car'):
            if (posicionObjeto(objeto, CAR_MARGEN) == 'DERECHA'):
                 d=d+1
    return d


def posicionObjeto(objeto, MARGEN):
    if  ((objeto.area > zonadeteccion.area*PERSON_MARGEN)and
          (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
          (objeto.centrox > zonadeteccion.x1 and 
           objeto.centrox < zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3))) 
         ):
            return "IZQUIERDA"
    elif ((objeto.area > zonadeteccion.area*PERSON_MARGEN) and
         (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
         (objeto.centrox > zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
          objeto.centrox < zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)))
         ): 
            return "CENTRO"
    elif ((objeto.area > zonadeteccion.area*PERSON_MARGEN)and
          (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
          (objeto.centrox > zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
           objeto.centrox < zonadeteccion.x2 ) 
         ):
            return "DERECHA"
    else:
            return "FUERA"


##--------------------------------------------------------------------------------------------------------------------##
## FUNCION DEL SABER ##
## ESTA FUNCION ES LA QUE DECIDE QUE HACER ##
##--------------------------------------------------------------------------------------------------------------------##

def oraculo(detectionzone, contenedor):
    global zonadeteccion

    zonadeteccion=detectionzone
    print("Personas")
    print(cuentaPersonas(contenedor))
    print(personasIzquierda(contenedor))
    print(personasCentro(contenedor))
    print(personasDerecha(contenedor))
    print("Coches")
    print(cuentaCoches(contenedor))
    print(cochesIzquierda(contenedor))
    print(cochesCentro(contenedor))
    print(cochesDerecha(contenedor))


    ##--------------------------##
    ##          FUZZY           ##
    ##--------------------------##
    personas = ctrl.Antecedent(np.arange(0, 1001, 1), 'personas')
    coches = ctrl.Antecedent(np.arange(0, 1001, 1), 'coches')
    direccion = ctrl.Consequent(np.arange(0, 2501, 1), 'direccion')
    

    names = ['left', 'center', 'right']
    dnames = ['izquierda', 'stop', 'derecha']
    personas.automf(names=names)
    coches.automf(names=names)
    direccion.automf(names=dnames)

    direccion['izquierda'] = fuzz.trimf(direccion.universe, [0, 0, 1250])
    direccion['stop'] = fuzz.trimf(direccion.universe, [0, 1250, 2500])
    direccion['derecha'] = fuzz.trimf(direccion.universe, [1250, 2500, 2500])

 
    rule1 = ctrl.Rule(antecedent=(
                                    (personas['left'])| 
                                    (coches['center'] | personas['center'])| 
                                    (personas['right']) 
                                 ),
                      consequent=direccion['stop'], label='stop')
                    
    rule2 = ctrl.Rule(antecedent=(
                                    (coches['left'])| 
                                    (personas['center'])| 
                                    (personas['right'])
                                 ),
                      consequent=direccion['izquierda'], label='izquierda')

    rule3 = ctrl.Rule(antecedent=(
                                    (personas['left'])| 
                                    (personas['center'])| 
                                    (coches['right'])
                                 ),
                      consequent=direccion['derecha'], label='derecha')


    ctrl_direction= ctrl.ControlSystem(rules=[rule1, rule2, rule3])
    direction = ctrl.ControlSystemSimulation(ctrl_direction)

    direction.input['personas'] = (personasIzquierda(contenedor)+
                                personasCentro(contenedor)*10+
                                personasDerecha(contenedor)*100)
    direction.input['coches'] =   (cochesIzquierda(contenedor)+
                                cochesCentro(contenedor)*10+
                                cochesDerecha(contenedor)*100)
    direction.compute()

    print("PREDICCION: ")
    print(direction.output['direccion'])

    print((cochesIzquierda(contenedor)+cochesCentro(contenedor)*10+
                                cochesDerecha(contenedor)*100))
    print((personasIzquierda(contenedor)+
                                personasCentro(contenedor)*10+
                                personasDerecha(contenedor)*100))

    return "GO"    





##-------------------------##
## NO SE USA ESTA FUNCION# ##
##-------------------------##
def P_oraculo(zonadeteccion, contenedor):

#DECISION REFERENTE A PERSONAS
    if ((objeto.nombre == 'person') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN) and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
    (objeto.centrox > zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)))
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "STOP"
    if ((objeto.nombre == 'person') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
    (objeto.centrox > zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 ) 
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "LEFT"
    if ((objeto.nombre == 'person') and 
    (objeto.area > zonadeteccion.area*PERSON_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
    (objeto.centrox > zonadeteccion.x1 and 
     objeto.centrox < zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3))) 
    ):
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "RIGHT"

#DECISION REFERENTE A COCHES
    if ((objeto.nombre == 'car') and 
    (objeto.area > zonadeteccion.area*CAR_MARGEN) and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
    (objeto.centrox > zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)))
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "STOP"
    if ((objeto.nombre == 'car') and 
    (objeto.area > zonadeteccion.area*CAR_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
    (objeto.centrox > zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
     objeto.centrox < zonadeteccion.x2 ) 
    ): 
        print("Area: "+str(objeto.area))
        print(objeto.nombre)     
        return "RIGHT"
    if ((objeto.nombre == 'car') and 
    (objeto.area > zonadeteccion.area*CAR_MARGEN)and
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
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




