import machine
import time
import math

#VARIABLES PARA LOS SERVOS
#SERVO 1
pin = machine.Pin(12, machine.Pin.OUT)
servo1 = machine.PWM(pin)
servo1.freq(50)

#SERVO 2
pin2 = machine.Pin(25, machine.Pin.OUT)
servo2 = machine.PWM(pin2)
servo2.freq(50)

#VARIABLES DE CONTROL PARA LA CINEMATICA INVERSA
LONGITUD_1 = 12.0
LONGITUD_2 = 12.0

#CONFIGURACION INICIAL DE LOS SERVOS
servo1.duty(20)
servo2.duty(20)
time.sleep_ms(1000)

#LOOP PRINCIPAL
"""while True:
    #VARIABLES DE ENTRADA
    x = float(input("Ingrese la coordenada en x: "))
    y = float(input("Ingrese la coordenada en y: "))
    
    #CALCULAR EL MOVIMIENTO EN RADIANES
    ang_2_rad = math.acos((math.sqrt(x)+ math.sqrt(y) - math.sqrt(LONGITUD_1) - math.sqrt(LONGITUD_2)) / (2*LONGITUD_1*LONGITUD_2))
    ang_1_rad = math.atan(y / x) - math.atan((LONGITUD_2*math.sin(ang_2_rad)) / (LONGITUD_1+ LONGITUD_2*math.cos(ang_2_rad)))
    
    #CALCULAR LOS ANGULOS
    print(ang_1_rad)
    print(ang_2_rad)
    angulo_1 = math.degrees(ang_1_rad)
    angulo_2 = math.degrees(ang_2_rad)
    
    print("Ángulo 1: ", angulo_1)
    print("Ángulo 2: ", angulo_2)
    
    #MAPEAR LOS ANGULOS
    valor_1 = (angulo_1/1.8)+20
    valor_2 = (angulo_2/1.8)+20
    if(angulo_1<0):
        valor_1=20
        
    if(angulo_2<0):
        valor_2=20
        
    print(int(valor_1))
    print(int(valor_2))
    
    #MOVER LOS SERVOS
    servo1.duty(int(valor_1))
    servo2.duty(int(valor_2))
    
    #ESPERAR 10 SEGUNDOS Y REGRESAR A LA POSICION INICIAL
    time.sleep(10)
    servo1.duty(20) 
    servo2.duty(20)"""