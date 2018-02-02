from __future__ import division
from __future__ import unicode_literals
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
        if (objeto.nombre == 'car' or objeto.nombre == 'truck'):
            c=c+1
    return c
def cochesIzquierda(contenedor):
    i=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car' or objeto.nombre == 'truck'):
            if (posicionObjeto(objeto) == 'IZQUIERDA'):
                if (objeto.area > i):
                    i=objeto.area
    return int(i/1000)
def cochesCentro(contenedor):
    c=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car' or objeto.nombre == 'truck'):
            if (posicionObjeto(objeto) == 'CENTRO'): 
                if (objeto.area > c):
                    c=objeto.area
    return int(c/1000)
def cochesDerecha(contenedor):
    d=0
    for e in range(len(contenedor)):
        objeto=contenedor[e]
        if (objeto.nombre == 'car' or objeto.nombre == 'truck'):
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
    PERSON_CERCA=(zonadeteccion.area/1000)*0.10
    PERSON_MEDIO=(zonadeteccion.area/1000)*0.06
    PERSON_LEJOS=(zonadeteccion.area/1000)*0.02

    CAR_CERCA=(zonadeteccion.area/1000)*0.20
    CAR_MEDIO=(zonadeteccion.area/1000)*0.12
    CAR_LEJOS=(zonadeteccion.area/1000)*0.05


    print("Personas")
    print(cuentaPersonas(contenedor))
    print(personasIzquierda(contenedor))
    print(personasCentro(contenedor))
    print(personasDerecha(contenedor))
    print(zonadeteccion.area)
    print(PERSON_CERCA)
    print(PERSON_MEDIO)
    print(PERSON_LEJOS)

    print("Coches")
    print(cuentaCoches(contenedor))
    print(cochesIzquierda(contenedor))
    print(cochesCentro(contenedor))
    print(cochesDerecha(contenedor))
    print(zonadeteccion.area)
    print(CAR_CERCA)
    print(CAR_MEDIO)
    print(CAR_LEJOS)

    ##--------------------------##
    ##          FUZZY           ##
    ##--------------------------##
    in_p_names = ['lejos', 'medio', 'cerca']
    p_izquierda = ctrl.Antecedent(np.arange(0, PERSON_CERCA+1, 1), 'p_izquierda')
    p_centro = ctrl.Antecedent(np.arange(0, PERSON_CERCA+1, 1), 'p_centro')
    p_derecha = ctrl.Antecedent(np.arange(0, PERSON_CERCA+1, 1), 'p_derecha')
    p_izquierda.automf(names=in_p_names)
    p_centro.automf(names=in_p_names)
    p_derecha.automf(names=in_p_names)   
    p_izquierda['lejos'] = p_centro['lejos'] = p_derecha['lejos'] = fuzz.trapmf(p_derecha.universe, [0, 0, (PERSON_LEJOS-2), PERSON_LEJOS])
    p_izquierda['medio'] = p_centro['medio'] = p_derecha['medio'] = fuzz.trapmf(p_derecha.universe, [(PERSON_LEJOS-2), PERSON_LEJOS, (PERSON_MEDIO-2), PERSON_MEDIO])
    p_izquierda['cerca'] = p_centro['cerca'] = p_derecha['cerca'] = fuzz.trapmf(p_derecha.universe, [(PERSON_MEDIO-2), PERSON_MEDIO, PERSON_CERCA, PERSON_CERCA])
    
    in_c_names = ['lejos', 'medio', 'cerca']
    c_izquierda = ctrl.Antecedent(np.arange(0, CAR_CERCA+1, 1), 'c_izquierda')
    c_centro = ctrl.Antecedent(np.arange(0, CAR_CERCA+1, 1), 'c_centro')
    c_derecha = ctrl.Antecedent(np.arange(0, CAR_CERCA+1, 1), 'c_derecha')
    c_izquierda.automf(names=in_c_names)
    c_centro.automf(names=in_c_names)
    c_derecha.automf(names=in_c_names)   
    c_izquierda['lejos'] = c_centro['lejos'] = c_derecha['lejos'] = fuzz.trapmf(c_derecha.universe, [0, 0, (CAR_LEJOS-2), CAR_LEJOS])
    c_izquierda['medio'] = c_centro['medio'] = c_derecha['medio'] = fuzz.trapmf(c_derecha.universe, [(CAR_LEJOS-2), CAR_LEJOS, (CAR_MEDIO-2), CAR_MEDIO])
    c_izquierda['cerca'] = c_centro['cerca'] = c_derecha['cerca'] = fuzz.trapmf(c_derecha.universe, [ (CAR_MEDIO-2), CAR_MEDIO, CAR_CERCA, CAR_CERCA])
 


    out_d_names = ['mucho_izquierda', 'medio_izquierda', 'neutro', 'medio_derecha', 'mucho_derecha']
    direccion = ctrl.Consequent(np.arange(0, 181, 1), 'direccion')
    direccion.automf(names=out_d_names)
    direccion['mucho_izquierda'] = fuzz.trapmf(direccion.universe, [0, 0, 35, 40])
    direccion['medio_izquierda'] = fuzz.trapmf(direccion.universe, [35, 40, 70, 75])
    direccion['neutro'] = fuzz.trapmf(direccion.universe, [70, 75, 105, 110])
    direccion['medio_derecha'] = fuzz.trapmf(direccion.universe, [105, 110, 140, 145])
    direccion['mucho_derecha'] = fuzz.trapmf(direccion.universe, [140, 145, 180, 180])
 
    out_f_names = ['leve', 'medio', 'fuerte']
    frenada = ctrl.Consequent(np.arange(0,101, 1), 'frenada')
    frenada.automf(names=out_f_names)
    frenada['leve'] = fuzz.trapmf(frenada.universe, [0, 0, 16, 20])
    frenada['medio'] = fuzz.trapmf(frenada.universe, [16, 20, 35, 40])
    frenada['fuerte'] = fuzz.trapmf(frenada.universe, [35, 40, 100, 100])



## ------------------------------------------ //CONTROL VOLANTE\\ ------------------------------------------ ## 
    d_rule1 = ctrl.Rule(antecedent=(
                                    (p_izquierda['cerca'])&(p_centro['medio']|p_centro['lejos']) 
                                 ),
                      consequent=direccion['mucho_derecha'])
                    
    d_rule2 = ctrl.Rule(antecedent=(
                                    (p_izquierda['medio'])&(p_centro['medio']|p_centro['lejos'])
                                 ),
                      consequent=direccion['medio_derecha'])

    d_rule3 = ctrl.Rule(antecedent=(
                                    ((p_izquierda['lejos']&p_derecha['lejos'])|p_centro['cerca'])
                                 ),
                      consequent=direccion['neutro'])

    d_rule4 = ctrl.Rule(antecedent=(
                                    (p_derecha['medio'])&(p_centro['medio']|p_centro['lejos'])
                                 ),
                      consequent=direccion['medio_izquierda'])

    d_rule5 = ctrl.Rule(antecedent=(
                                    (p_derecha['cerca'])&(p_centro['medio']|p_centro['lejos']) 
                                 ),
                      consequent=direccion['mucho_izquierda'])

    
    d_rule6 = ctrl.Rule(antecedent=(
                                    (c_izquierda['cerca'])&(c_centro['medio']|c_centro['lejos']) 
                                 ),
                      consequent=direccion['mucho_derecha'])
                    
    d_rule7 = ctrl.Rule(antecedent=(
                                    (c_izquierda['medio'])&(c_centro['medio']|c_centro['lejos'])
                                 ),
                      consequent=direccion['medio_derecha'])

    d_rule8 = ctrl.Rule(antecedent=(
                                    ((c_izquierda['lejos']&c_derecha['lejos'])|c_centro['cerca'])
                                 ),
                      consequent=direccion['neutro'])

    d_rule9 = ctrl.Rule(antecedent=(
                                    (c_derecha['medio'])&(c_centro['medio']|c_centro['lejos'])
                                 ),
                      consequent=direccion['medio_izquierda'])

    d_rule10 = ctrl.Rule(antecedent=(
                                    (c_derecha['cerca'])&(c_centro['medio']|c_centro['lejos']) 
                                 ),
                      consequent=direccion['mucho_izquierda'])



    ctrl_volante= ctrl.ControlSystem(rules=[d_rule1, d_rule2, d_rule3, d_rule4, d_rule5, 
                                            d_rule6, d_rule7, d_rule8, d_rule9, d_rule10])
    volante = ctrl.ControlSystemSimulation(ctrl_volante)


    volante.input['p_izquierda'] = personasIzquierda(contenedor)
    volante.input['p_centro']    = personasCentro(contenedor)
    volante.input['p_derecha']   = personasDerecha(contenedor)

    volante.input['c_izquierda'] = cochesIzquierda(contenedor)
    volante.input['c_centro']    = cochesCentro(contenedor)
    volante.input['c_derecha']   = cochesDerecha(contenedor)

    volante.compute()

    print("PREDICCION VOLANTE: ")
    print(volante.output['direccion'])
## ------------------------------------------ \\CONTROL VOLANTE// ------------------------------------------ ##
## --------------------------------------------------------------------------------------------------------- ##
## ------------------------------------------ //CONTROL FRENADA\\ ------------------------------------------ ##
    f_rule1 = ctrl.Rule(antecedent=(
                                    (p_izquierda['cerca'])|(p_centro['cerca'])|(p_derecha['cerca'])
                                 ),
                      consequent=frenada['fuerte'])
                    
    f_rule2 = ctrl.Rule(antecedent=(
                                    (p_izquierda['medio'])|(p_centro['medio'])|(p_derecha['medio'])
                                 ),
                      consequent=frenada['medio'])

    f_rule3 = ctrl.Rule(antecedent=(
                                    (p_izquierda['lejos'])|(p_centro['lejos'])|(p_derecha['lejos'])
                                 ),
                      consequent=frenada['leve'])
    
    
    f_rule4 = ctrl.Rule(antecedent=(
                                    (c_izquierda['cerca'])|(c_centro['cerca'])|(c_derecha['cerca'])
                                 ),
                      consequent=frenada['fuerte'])
    f_rule5 = ctrl.Rule(antecedent=(
                                    (c_izquierda['medio'])|(c_centro['medio'])|(c_derecha['medio'])
                                 ),
                      consequent=frenada['medio'])

    f_rule6 = ctrl.Rule(antecedent=(
                                    (c_izquierda['lejos'])|(c_centro['lejos'])|(c_derecha['lejos'])
                                 ),
                      consequent=frenada['leve'])



    ctrl_freno= ctrl.ControlSystem(rules=[f_rule1, f_rule2, f_rule3, 
                                          f_rule4, f_rule5, f_rule6])
    freno = ctrl.ControlSystemSimulation(ctrl_freno)


    freno.input['p_izquierda'] = personasIzquierda(contenedor)
    freno.input['p_centro']    = personasCentro(contenedor)
    freno.input['p_derecha']   = personasDerecha(contenedor)

    freno.input['c_izquierda'] = cochesIzquierda(contenedor)
    freno.input['c_centro']    = cochesCentro(contenedor)
    freno.input['c_derecha']   = cochesDerecha(contenedor)


    freno.compute()

    print("PREDICCION FRENADA: ")
    print(freno.output['frenada'])

## ------------------------------------------ \\CONTROL FRENADA// ------------------------------------------ ##

    return volante.output['direccion'], freno.output['frenada']




## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
##-------------------------##
## NO SE USA ESTA FUNCION# ##
##-------------------------##
def P_oraculo(zonadeteccion, contenedor):

    CAR_MARGEN=0
    PERSON_MARGEN=0

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




