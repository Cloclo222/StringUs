
#include <Dynamixel2Arduino.h> //Installer par le gestionnaire de librarie Arduino IDE
#include "src/Scara/Scara.h" //Dans le fichier src, c'est notre propre librarie
#include "Arduino.h"

#define DXL_SERIAL   Serial1
#define BUFFER_LENGTH 64

char serialBuffer[BUFFER_LENGTH]; // Buffer pour les messages Serial
int bufferIndex = 0;              // Index pour le char dans serialBuffer

void serialControl(); 
void executeCommand(const char* command);

Dynamixel2Arduino _dxl(DXL_SERIAL, -1); //Si variable définit avec un "_" à l'avant, c'est un objet!

Scara _scara(_dxl);

void setup() {
    Serial.begin(115200);
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

  delay(100);
  serialControl();

}

void serialControl() {

  while (Serial.available() > 0) {            //Si message dans Serial
    char incomingChar = Serial.read();

      if (incomingChar == '}')                // "}" veut dire que c'est la fin du message
      {
        serialBuffer[bufferIndex] = '\0';     // Mets une fin au string
        //Serial.print(serialBuffer);
        executeCommand(serialBuffer);     // executeCommand, en skippant le '{'
        bufferIndex = 0;                    
      } 
      
      else if (incomingChar != '{' && bufferIndex < BUFFER_LENGTH - 1)  //Condition pour enregistrer les char jusqu'à }
      { 
        serialBuffer[bufferIndex++] = incomingChar;                     
      }
  }
}

void executeCommand(const char* command) {
  
  if (command[0] == 'C') {            // Regarde si le string commence par C
    char command_char = command[1];
    int command_int = command_char - '0';
    switch (command_int) { // Regarde le chiffre de commande
                 
      //==============================================================================================================//
      // 1 : Mouvement simple jusqu'à l'angle demandé
      case 1: {                                                      
        int angle1, angle2;
        sscanf(command + 2, "%d %d", &angle1, &angle2);
        if (sscanf(command + 2, "%d %d", &angle1, &angle2) == 2) { //Regarde s'il y a deux angle
          int position[2] = {angle1, angle2};
          _scara.setPos(position);
          _scara.isPos(position);
          
        }

        else{
        Serial.print("C1_error : La commande n'a pas reçu deux angles."); 
        }

        break;
      }

      //==============================================================================================================//
      // 2 : ...
      case 2: {
        break;
      }

      //==============================================================================================================//
      // 3 : ...
      case 3: {
        break;
      }
    }
  }
  
  Serial.println('1'); // Retourne 1 au programme Python pour demander une prochaine commande
}