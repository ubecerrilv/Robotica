#include <Servo.h>
#include <math.h>

Servo servo1;
Servo servo2;
float nv = 0;
//variables
const int enlace1 = 10;  // Longitud del primer enlace en cm
const int enlace2 = 10;  // Longitud del segundo enlace en cm
 
//configuación del Arduino
void setup() {
  Serial.begin(9600);
  servo1.attach(9);  //Selección del GPIO 10
  servo2.attach(10);  //Selección del GPIO 9
 
 // envia a los servos a su posición inicial
  servo1.write(0);
  servo2.write(0);
  Serial.println("Introduzca datos");
}
//Rutina para evitar el valor cero que envia la función parseFloat
void no_valor()
{
 while (Serial.available() == 0){}          
 nv = Serial.parseFloat();  
}
 
//Programa principal
void loop() {
  int x1, y1, x2, y2;
 //captura de datos
  //Serial.println("Proporciona el valor de X ");
  while(Serial.available()==0){}
  String coords = Serial.readStringUntil('f');
  sscanf(coords.c_str(), "%d,%d,%d,%d", &x1, &y1, &x2, &y2);
  //no_valor();
    //AJUSTE DE COORDENADAS
    x1-=1;
    y1-=2;

    x2-=1;
    y2-=2;
    Serial.print(x1);
    Serial.print(y1);
    Serial.print(x2);
    Serial.println(y2);
  no_valor();
  mueveServos(x1,y1);
  delay(3000);
  mueveServos(x2,y2);
}//FIN LOOP

void mueveServos(int x, int y){    
    //cálculo de los ángulos
   float theta2 = acos((x*x + y*y - enlace1*enlace1 - enlace2*enlace2) / (2 * enlace1 * enlace2));
   float theta1 = atan2(y, x) - atan2((enlace2 * sin(theta2)), (enlace1 + enlace2 * cos(theta2)));

   // Convertir los ángulos de radianes a grados
    int angulo1 = degrees(theta1);
    int angulo2 = degrees(theta2);

    // Asegurarse de que los ángulos estén dentro del rango de 0 a 180 grados
    angulo1 = constrain(angulo1, 0, 180);
    angulo2 = constrain(angulo2, 0, 180);

    // Mover los servos a las posiciones calculadas
    servo1.write(angulo1);
    servo2.write(angulo2);

    // Mostrar los ángulos calculados
    Serial.print("Ángulo 1: ");
    Serial.print(angulo1);
    Serial.print(" grados, Ángulo 2: ");
    Serial.print(angulo2);
    Serial.println(" grados");

    delay(3000);  // Esperar un segundo antes de solicitar nuevas coordenadas
    //REGRESAR SERVOS A LA POSICION ORIGINAL
    servo1.write(0);
    servo2.write(0);
      
}//FIN MUEVE SERVOS