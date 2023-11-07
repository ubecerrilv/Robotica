import machine
import time

#VARIABLES PARA LOS SERVOS
pin = machine.Pin(12, machine.Pin.OUT)
servo = machine.PWM(pin)

servo.freq(50)

servo.duty(20)
time.sleep_ms(1000)

while True:
    servo.duty(20)
    time.sleep_ms(1000)  
    
    servo.duty(125)
    time.sleep_ms(1000)