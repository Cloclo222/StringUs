
#include <Dynamixel2Arduino.h> //Installer par le gestionnaire de librarie Arduino IDE
#include "src/Scara/Scara.h" //Dans le fichier src, c'est notre propre librarie
#include "Arduino.h"

#define DXL_SERIAL   Serial1

void printData(); 

Dynamixel2Arduino _dxl(DXL_SERIAL, -1); //Si variable définit avec un "_" à l'avant, c'est un objet!

Scara _scara(_dxl);

int x;

void setup() {
    Serial.begin(115200);
    Serial.setTimeout(1);
    _dxl.begin(57600);
    Serial.println("Baudrate init.");

    _scara.init_com();
    Serial.println("Comunication init.");
    _scara.init_moteur();
    Serial.println("Moteur init.");

    delay(2000);
    _scara.homing();
    Serial.println("Homing complete.");
    

    _scara.setSpeed(50); //Limite à 100
    _scara.setAcceleration(0); //No-limit
    Serial.println("AccelSpeed complete.");
}

void loop() {

  if (Serial.available() > 0) {
    int x = Serial.readString().toInt();
    Serial.print(x);
    int pos[x] = {x, x};
   _scara.setPos(pos);
  }
    
  

   /*delay(1000);
   int pos[2] = {104, 81};
   _scara.setPos(pos);

   delay(1000);
   int pos1[2] = {81, 104};
   _scara.setPos(pos1);

   delay(1000);
   int pos2[2] = {95, 118};
   _scara.setPos(pos2);

   delay(1000);
   int pos3[2] = {118, 95};
   _scara.setPos(pos3);*/
}

void printData() {
    //Serial.print("X: "); Serial.print(_scara.printData.x);
    //Serial.print(", Y: "); Serial.print(_scara.printData.y);
    Serial.print(", Angle gauche: "); Serial.print(_scara.getPos()[0]);
    Serial.print(", Angle droite: "); Serial.print(_scara.getPos()[1]);
    Serial.print(", Vitesse Max: "); Serial.print(_scara.getSpeedAccel()[0]);
    Serial.print(", Acceleration Max: "); Serial.println(_scara.getSpeedAccel()[1]);
}