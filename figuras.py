import cv2
import numpy as np

# Define los rangos de colores para el azul y el rojo
azul_bajo = np.array([100, 100, 20], np.uint8)
azul_alto = np.array([130, 255, 255], np.uint8)
rojo_bajo = np.array([0, 100, 20], np.uint8)
rojo_alto = np.array([25, 255, 255], np.uint8)

# Abre la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Obtiene un nuevo frame de la cámara web
    ret, frame = cap.read()

    # Convierte el frame al espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crea máscaras para el azul y el rojo
    mask_azul = cv2.inRange(hsv, azul_bajo, azul_alto)
    mask_rojo = cv2.inRange(hsv, rojo_bajo, rojo_alto)

    # Encuentra los contornos en las máscaras
    contornos_azul = cv2.findContours(mask_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_rojo = cv2.findContours(mask_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibuja los contornos encontrados
    if contornos_azul is not None:
        for contorno in contornos_azul[0]:
            cv2.drawContours(frame, contorno, -1, (0, 0, 255), 2)
    if contornos_rojo is not None:
        for contorno in contornos_rojo[0]:
            cv2.drawContours(frame, contorno, -1, (0, 255, 0), 2)

    # Muestra el frame
    cv2.imshow("Frame", frame)

    # Espera a que se presione una tecla
    k = cv2.waitKey(1)

    # Si se presiona la tecla q, se sale del bucle
    if k == ord("q"):
        break

# Cierra la cámara web
cap.release()

# Destruye todas las ventanas abiertas
cv2.destroyAllWindows()

