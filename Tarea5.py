# LIBRERIAS A UTILIZAR
from inspect import getcallargs
from uu import encode
import cv2
import numpy as np
import serial
import time


# INICIALIZACION DE COMUNICACION SERIAL CON EL ESP32
ser = serial.Serial('/dev/ttyACM0', 9600)


# DEFINICION DE RANGO DE COLORES DE LAS FIGURAS GEOMETRICAS
red_lower = np.array([0,100,20],np.uint8)
red_upper = np.array([5,255,255],np.uint8)

green_lower = np.array([40,50,40],np.uint8)
green_upper = np.array([70,255,70],np.uint8)

blue_lower = np.array([100,100,20],np.uint8)
blue_upper = np.array([125,255,255],np.uint8)

# FUNCION PARA OBTENER LAS COORDENADAS DE LA FIGURA EN LA IMAGEN
def get_coordinates(contour):
   M = cv2.moments(contour)
   cX = int(M["m10"] / M["m00"])
   cY = int(M["m01"] / M["m00"])
   return cX, cY


# INICIALIZACION DE LA CAMARA
cap = cv2.VideoCapture(1)  # CAMARA 1: EXTERNA, CAMARA 0: LAPTOP

def ejecuta(cap, envia):
   # CAPTURA DE UN FOTOGRAMA EN LA IMAGEN
   ret, frame = cap.read()

   if not ret:
       return None

   # APLICA UN SUAVIZADO PARA REDUCIR EL RUIDO
   blurred = cv2.GaussianBlur(frame, (11, 11), 0)


   # CONVIERTE EL FOTOGRAMA A UN ESPACIO DE COLOR HSV
   hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


   # DETECCION DE FIGURAS ROJAS
   red_mask = cv2.inRange(hsv, red_lower, red_upper)
   red_mask = cv2.erode(red_mask, None, iterations=2)
   red_mask = cv2.dilate(red_mask, None, iterations=2)


   # DETECCION DE FIGURAS AZULES
   blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
   blue_mask = cv2.erode(blue_mask, None, iterations=2)
   blue_mask = cv2.dilate(blue_mask, None, iterations=2)

   #DETECCION DE FIGURAS VERDES
   green_mask = cv2.inRange(hsv, green_lower, green_upper)
   green_mask = cv2.erode(green_mask, None, iterations=2)
   green_mask = cv2.dilate(green_mask, None, iterations=2)


   # Encontrar los contornos de las figuras detectadas
   red_contours, _ = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   blue_contours, _ = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   green_contours, _ = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


   # VARIABLES PARA MANDARLAS A ARDUINO
   x1=0
   y1=0
   x2=0
   y2=0

   # PROCESAR LOS CONTORNO DE LAS FIGURAS ROJAS
   for contour in red_contours:
       area = cv2.contourArea(contour)
       if area > 500:  #PRUEBA Y ERROR
           x1, y1 = get_coordinates(contour)
           x1=int((17*(x1-315))/(315))
           y1=int((26*(480-y1))/(480)-1)

           x, y = get_coordinates(contour)
           cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
           cv2.putText(frame, 'Triangulo rojo '+str(x1)+', '+str(y1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

           if envia:
              print("Triangulo rojo: ",x1,y1)
            


   # PROCESAR LOS CONTORNOS DE LAS FIGURAS AZULES
   for contour in blue_contours:
       area = cv2.contourArea(contour)
       if area > 500:  # PRUEBA Y ERROR
           x2, y2 = get_coordinates(contour)
           x2=int((17*(x2-315))/(315))
           y2=int((26*(480-y2))/(480)-1)

           x,y = get_coordinates(contour)
           cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)
           cv2.putText(frame, 'Circulo azul '+str(x2)+', '+str(y2), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

           if envia:
              print("Circulo azul:",x2,y2)
    
    #ENVIAR DATOS A ARDUINO
   if envia:
       ser.write(f"{x1},{y1},{x2},{y2}f".encode())

   return frame


while True:
    # MUESTRA IMAGEN PROCESADA
   frame = ejecuta(cap, False)
   cv2.imshow('Camera', frame)

   #EJECUTA LA ACCION DE LOS SERVOS CON E
   if cv2.waitKey(1) & 0xFF == ord('e'):
       ejecuta(cap, True)

   # SALE DEL BUCLE CON "q"
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break
   

# TERMINA EL PROGRAMA
cap.release()
cv2.destroyAllWindows()