#include <Dynamixel2Arduino.h> //Installer par le gestionnaire de librarie Arduino IDE
#include "src/Scara/Scara.h" //Dans le fichier src, c'est notre propre librarie
#include "Arduino.h"

#define DXL_SERIAL   Serial1

void printData(); 

Dynamixel2Arduino _dxl(DXL_SERIAL, -1); //Si variable définit avec un "_" à l'avant, c'est un objet!

Scara _scara(_dxl);

void setup() {
    Serial.begin(115200);

    _dxl.begin(57600);

   _scara.init_com();
   _scara.init_moteur();
}

void loop() {

  int pos[2] = {1000,0};
  _scara.setPos(pos);
  delay(3000);
  printData();
  pos[0] = 0;
  pos[1] = 1000;
  _scara.setPos(pos);
  delay(3000);
  printData();
}

void printData() {
    //Serial.print("X: "); Serial.print(_scara.printData.x);
    //Serial.print(", Y: "); Serial.print(_scara.printData.y);
    Serial.print(", Angle gauche: "); Serial.print(_scara.getPos()[0]);
    Serial.print(", Angle droite: "); Serial.print(_scara.getPos()[1]);
    Serial.print(", Vitesse Max: "); Serial.print(_scara.getSpeedAccel()[0]);
    Serial.print(", Acceleration Max: "); Serial.println(_scara.getSpeedAccel()[1]);
}