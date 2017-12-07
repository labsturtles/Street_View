import knowledge as kw
import cv2

width=0        
height=0

zonadeteccion=kw.elemento("zonadeteccion",0, 0, 0, 0, 0, 0, 0, 0, 0)
objeto=kw.elemento("none",0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
contenedor=[]

#Guardamos el tamaño de la imagen: ancho, alto
def resolucionImagen(ancho, alto):
    global width 
    global height
    width = ancho
    height = alto

#Creamos el area de deteccion, donde se interactuara con los resultados
#Se le pasa como parametros el tamaño del cuadro deteccion: esquina superior izquieda, esquina inferior derecha
def creaAreaDetect(x1, x2, y1, y2):
    
    tam_x=(x2-x1)
    tam_y=(y2-y1)
    med_x=(tam_x/2)
    med_y=(tam_y/2)
    area=(tam_x * tam_y)

    global zonadeteccion
    zonadeteccion=kw.elemento("zonadeteccion",x1, x2, y1, y2, tam_x, tam_y, med_x, med_y, area)


def possElemento(nombre, x1, x2, y1, y2):
    
    tam_x=(x2-x1)
    tam_y=(y2-y1)
    med_x=(tam_x/2)
    med_y=(tam_y/2)
    area=(tam_x * tam_y)
    
    global zonadeteccion
    zonadeteccion=kw.elemento(nombre,x1, x2, y1, y2, tam_x, tam_y, med_x, med_y, area)


def procesaElemento(boxes, classes, scores, category_index, image_np):
    
    global objeto
    objeto=kw.elemento("none",0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    contenedor.clear()

    min_score_thresh=.5
    max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
              box = tuple(boxes[i].tolist())
              #print(box)

              #Se extrae la posicion del objeto y tamaño
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
              #print("Area: "+str(area))                    
              centrox=x1+med_x
              centroy=y1+med_y

              #print("centro_X: "+str(centrox))
              #print("centro_Y: "+str(centroy))
    

              #Se identifica el objeto
              if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]['name']
                    #print(class_name)

                   
                    objeto=kw.elemento(class_name,x1, x2, y1, y2, tam_x, tam_y, med_x, med_y, area, centrox, centroy)
                    #Guarda los objetos en un array
                    contenedor.append(objeto)

                    #Pinta en la imagen el Area definida
                    cv2.rectangle(image_np,(int(zonadeteccion.x1),int(zonadeteccion.y1)),(int(zonadeteccion.x2),int(zonadeteccion.y2)),(0,255,0),3)
                    cv2.rectangle(image_np,(int(zonadeteccion.x1+((zonadeteccion.x2-zonadeteccion.x1)*(1/3))),int(zonadeteccion.y1)),(int(zonadeteccion.x2-((zonadeteccion.x2-zonadeteccion.x1)*(1/3))),int(zonadeteccion.y2)),(0,255,0),3)


                    #Pinta en la imagen el centro
                    #cv2.circle(image_np,(int(objeto.centrox),int(objeto.centroy)), 5, (0,0,255), -1)


    
    ## pregunto al oraculo que decision tomar
    
#    for e in range(len(contenedor)):
#         #print(len(contenedor))
#        objeto=contenedor[e]
#        print(objeto.nombre)

    return kw.oraculo(zonadeteccion, contenedor)		


