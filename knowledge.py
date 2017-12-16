
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


zonadeteccion=elemento("zonadeteccion",0, 0, 0, 0, 0, 0, 0, 0, 0)

PERSON_CERCA=zonadeteccion.area*0.05#0.15
PERSON_MEDIO=zonadeteccion.area*0.25
PERSON_LEJOS=zonadeteccion.area*0.50

CAR_MARGEN=zonadeteccion.area*0.05#0.15
CAR_MEDIO=zonadeteccion.area*0.25
CAR_LEJOS=zonadeteccion.area*0.50



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
            if (posicionObjeto(objeto) == 'IZQUIERDA'):
                if (objeto.area > i):
                    i=objeto.area
    return int(i/1000)
def personasCentro(contenedor):
    c=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'person'):
            if (posicionObjeto(objeto) == 'CENTRO'): 
                if (objeto.area > c):
                    c=objeto.area
    return int(c/1000)
def personasDerecha(contenedor):
    d=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'person'):
            if (posicionObjeto(objeto) == 'DERECHA'):
                if (objeto.area > d):
                    d=objeto.area
    return int(d/1000)

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
            if (posicionObjeto(objeto) == 'IZQUIERDA'):
                if (objeto.area > i):
                    i=objeto.area
    return int(i/1000)
def cochesCentro(contenedor):
    c=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car'):
            if (posicionObjeto(objeto) == 'CENTRO'): 
                if (objeto.area > c):
                    c=objeto.area
    return int(c/1000)
def cochesDerecha(contenedor):
    d=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car'):
            if (posicionObjeto(objeto) == 'DERECHA'):
                if (objeto.area > d):
                    d=objeto.area
    return int(d/1000)

def posicionObjeto(objeto):
    if  (
          (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
          (objeto.centrox > zonadeteccion.x1 and 
           objeto.centrox < zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3))) 
        ):
            return "IZQUIERDA"
    elif (
         (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2) and 
         (objeto.centrox > zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3)) and 
          objeto.centrox < zonadeteccion.x2 -((zonadeteccion.x2-zonadeteccion.x1)*(1/3)))
         ): 
            return "CENTRO"
    elif (
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
    izquierda = ctrl.Antecedent(np.arange(0, 101, 1), 'izquierda')
    centro = ctrl.Antecedent(np.arange(0, 101, 1), 'centro')
    derecha = ctrl.Antecedent(np.arange(0, 101, 1), 'derecha')

    direccion = ctrl.Consequent(np.arange(0, 181, 1), 'direccion')
    frenada = ctrl.Consequent(np.arange(0,301, 1), 'frenada')

    innames = ['lejos', 'medio', 'cerca']
    izquierda.automf(names=innames)
    centro.automf(names=innames)
    derecha.automf(names=innames)
 
    out_d_names = ['mucho_izquierda', 'medio_izquierda', 'neutro', 'medio_derecha', 'mucho_derecha']
    direccion.automf(names=out_d_names)
    direccion['mucho_izquierda'] = fuzz.trimf(direccion.universe, [0, 0, 45])
    direccion['medio_izquierda'] = fuzz.trimf(direccion.universe, [0, 45, 90])
    direccion['neutro'] = fuzz.trimf(direccion.universe, [45, 90, 135])
    direccion['medio_derecha'] = fuzz.trimf(direccion.universe, [90, 135, 180])
    direccion['mucho_derecha'] = fuzz.trimf(direccion.universe, [135, 180, 180])
 
    out_f_names = ['leve', 'medio', 'fuerte']
    frenada.automf(names=out_f_names)
    frenada['leve'] = fuzz.trimf(frenada.universe, [0, 8, 16])
    frenada['medio'] = fuzz.trimf(frenada.universe, [16, 26, 35])
    frenada['fuerte'] = fuzz.trimf(frenada.universe, [35, 68, 100])

## ------------------------------------------ //CONTROL VOLANTE\\ ------------------------------------------ ## 
    d_rule1 = ctrl.Rule(antecedent=(
                                    (izquierda['cerca'])&(centro['medio']|centro['lejos']) 
                                 ),
                      consequent=direccion['mucho_derecha'])
                    
    d_rule2 = ctrl.Rule(antecedent=(
                                    (izquierda['medio'])&(centro['medio']|centro['lejos'])
                                 ),
                      consequent=direccion['medio_derecha'])

    d_rule3 = ctrl.Rule(antecedent=(
                                    (izquierda['lejos'])| 
                                    (centro['cerca'])|
                                    (derecha['lejos'])
                                 ),
                      consequent=direccion['neutro'])

    d_rule4 = ctrl.Rule(antecedent=(
                                    (derecha['medio'])&(centro['medio']|centro['lejos'])
                                 ),
                      consequent=direccion['medio_izquierda'])

    d_rule5 = ctrl.Rule(antecedent=(
                                    (derecha['cerca'])&(centro['medio']|centro['lejos']) 
                                 ),
                      consequent=direccion['mucho_izquierda'])


    ctrl_volante= ctrl.ControlSystem(rules=[d_rule1, d_rule2, d_rule3, d_rule4, d_rule5])
    volante = ctrl.ControlSystemSimulation(ctrl_volante)

    volante.input['izquierda'] = (personasIzquierda(contenedor)|cochesIzquierda(contenedor))
    volante.input['centro']    = (personasCentro(contenedor)|cochesCentro(contenedor))
    volante.input['derecha']   = (personasDerecha(contenedor)|cochesDerecha(contenedor))

    volante.compute()

    print("PREDICCION VOLANTE: ")
    print(volante.output['direccion'])
## ------------------------------------------ \\CONTROL VOLANTE// ------------------------------------------ ##
## --------------------------------------------------------------------------------------------------------- ##
## ------------------------------------------ //CONTROL FRENADA\\ ------------------------------------------ ##
    f_rule1 = ctrl.Rule(antecedent=(
                                    (centro['cerca'])
                                 ),
                      consequent=frenada['fuerte'])
                    
    f_rule2 = ctrl.Rule(antecedent=(
                                    (izquierda['medio'])|(centro['medio'])|(derecha['medio'])
                                 ),
                      consequent=frenada['medio'])

    f_rule3 = ctrl.Rule(antecedent=(
                                    (izquierda['lejos'])|(centro['lejos'])|(derecha['lejos'])
                                 ),
                      consequent=frenada['leve'])


    ctrl_freno= ctrl.ControlSystem(rules=[f_rule1, f_rule2, f_rule3])
    freno = ctrl.ControlSystemSimulation(ctrl_freno)

    freno.input['izquierda'] = 0#(personasIzquierda(contenedor)|cochesIzquierda(contenedor))
    freno.input['centro']    = 100#(personasCentro(contenedor)|cochesCentro(contenedor))
    freno.input['derecha']   = 0#(personasDerecha(contenedor)|cochesDerecha(contenedor))

    freno.compute()

    print("PREDICCION FRENADA: ")
    print(freno.output['frenada'])

## ------------------------------------------ \\CONTROL FRENADA// ------------------------------------------ ##

    return "GO"    




## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
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




