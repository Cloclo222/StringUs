#include <Dynamixel2Arduino.h> //Installer par le gestionnaire de librarie Arduino IDE
#include "src/Scara/Scara.h" //Dans le fichier src, c'est notre propre librarie
#include "Arduino.h"
using namespace ControlTableItem;

Scara _scara; //Si variable définit avec un "_" à l'avant, c'est un objet!

void setup() {
  _scara.init();
}

void loop() {
 
  /*_scara.setGoalPosition(moteur_gauche, 0);
  dxl.setGoalPosition(moteur_droit, 0);
  delay(3000);
  dxl.setGoalPosition(moteur_gauche, 1000);
  dxl.setGoalPosition(moteur_droit, 1000);*/
  int pos[2] = {1000,1000};
  _scara.setPos(pos);
  Serial1.println("test");
  delay(3000);
}
