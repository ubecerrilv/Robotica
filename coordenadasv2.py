import cv2
import numpy as np
import keyboard

# Función para detectar y obtener coordenadas de un objeto de un color específico
def detect_object(frame, lower_color, upper_color, shape_name):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    
    # Encuentra contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Aproxima la forma del contorno
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Filtra contornos con un número específico de vértices (4 para cuadrado/rectángulo, 3 para triángulo)
        if len(approx) == 4 and shape_name in ['square', 'rectangle']:
            x, y, w, h = cv2.boundingRect(contour)
            x_center = x + w // 2
            y_center = y + h // 2
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f'{shape_name.upper()} ({x_center}, {y_center})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        elif len(approx) == 3 and shape_name == 'triangle':
            M = cv2.moments(contour)
            x_center = int(M["m10"] / M["m00"])
            y_center = int(M["m01"] / M["m00"])
            cv2.drawContours(frame, [contour], 0, (255, 0, 0), -1)
            cv2.putText(frame, f'{shape_name.upper()} ({x_center}, {y_center})', (x_center, y_center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    return frame

# Inicialización de la cámara USB
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Definir los rangos de color para los objetos
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # Espera a que se presione la tecla "Enter" para realizar la detección
    if keyboard.is_pressed("Enter"):
        # Detección de objetos
        frame = detect_object(frame, lower_red, upper_red, 'circle')
        frame = detect_object(frame, lower_red, upper_red, 'triangle')
        frame = detect_object(frame, lower_blue, upper_blue, 'square')
        frame = detect_object(frame, lower_blue, upper_blue, 'rectangle')

    cv2.imshow('Object Detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

