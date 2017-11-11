width=0        
height=0

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
objeto=elemento("none",0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
decision="GO"
MARGEN=0.15

#Guardamos el tamaño de la imagen: ancho, alto
def resolucionImagen(ancho, alto):
    global width 
    global height
    width = ancho
    height = alto

#Creamos el area de deteccion, donde se interactuara con los resultados
#Se le pasa como parametros el tamaño del cuadro deteccion: esquina superior izquieda, esquina inferior derecha
def creaAreaDetect(x1, x2, y1, y2):
    
    #Pinta en la imagen el cuadro
    #cv2.rectangle(image_np,(int(refx1),int(refy1)),(int(refx2),int(refy2)),(0,255,0),3)
    tam_x=(x2-x1)
    tam_y=(y2-y1)
    med_x=(tam_x/2)
    med_y=(tam_y/2)
    area=(tam_x * tam_y)
    
    global zonadeteccion
    zonadeteccion=elemento("zonadeteccion",x1, x2, y1, y2, tam_x, tam_y, med_x, med_y, area)


def possElemento(nombre, x1, x2, y1, y2):
    
    tam_x=(x2-x1)
    tam_y=(y2-y1)
    med_x=(tam_x/2)
    med_y=(tam_y/2)
    area=(tam_x * tam_y)
    
    global zonadeteccion
    zonadeteccion=elemento(nombre,x1, x2, y1, y2, tam_x, tam_y, med_x, med_y, area)


def decisionElemento(boxes, classes, scores, category_index, mg=0.15):
    
    global decision
    decision="GO"

    global MARGEN
    MARGEN=mg

    min_score_thresh=.5
    max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
              box = tuple(boxes[i].tolist())
              print("...")
              print(box)

              #Se extra la posicion del objeto y tamaño
              x1=box[1]*width
              x2=box[3]*width
              y1=box[0]*height
              y2=box[2]*height
              tam_x=(x2-x1)
              tam_y=(y2-y1) 
              med_x=(tam_x/2)
              med_y=(tam_y/2)
              area=(tam_x*tam_y)
              #print("tam_X: "+str(tam_x))
              #print("tam_Y: "+str(tam_y)) 
              print("Area: "+str(area))                    
              centrox=x1+med_x
              centroy=y1+med_y

              #Pinta en la imagen el centro
              #cv2.circle(image_np,(int(xc),int(yc)), 5, (0,0,255), -1)
              print("centro_X: "+str(centrox))
              print("centro_Y: "+str(centroy))
    

              #Se identifica el objeto
              if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]['name']
                    print(class_name)

                    global objeto
                    objeto=elemento(class_name,x1, x2, y1, y2, tam_x, tam_y, med_x, med_y, area, centrox, centroy)

                    oraculo(zonadeteccion, objeto)
			

    return decision



##--------------------------------------------------------------------------------------------------------------------##
## FUNCION DEL SABER ##
## ESTA FUNCION ES LA QUE DECIDE QUE HACER ##
##--------------------------------------------------------------------------------------------------------------------##

def oraculo(zonadeteccion, objeto):

    if ((objeto.nombre == 'person') and 
    ((objeto.centrox > zonadeteccion.x1 and objeto.centrox < zonadeteccion.x2 ) and 
    (objeto.centroy > zonadeteccion.y1 and objeto.centroy < zonadeteccion.y2 ) and objeto.area > objeto.area*MARGEN)):

        decision="STOP"
        print("STOP")



