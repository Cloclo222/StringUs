
#include <Dynamixel2Arduino.h> //Installer par le gestionnaire de librarie Arduino IDE
#include "src/Scara/Scara.h" //Dans le fichier src, c'est notre propre librarie
#include "Arduino.h"
#include <string>

#define DXL_SERIAL   Serial1
#define BUFFER_LENGTH 64
#define MAX_SCARA_SPEED 50
#define MAX_TABLE_SPEED 40

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
    _scara.setAcceleration(15,3);
    _scara.homing();
    Serial.println("Homing complete.");
    
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
          _scara.setSpeedForLinearMov(position,MAX_SCARA_SPEED);
          _scara.setScaraPos(position);
          int current_table_pos = _scara.getLastCmd()[2];
          // Serial.println("im in isPos");
          _scara.jointisPos(position);
          // Serial.println("im out isPos");
          
        }

        else{
        Serial.print("C1_error : La commande n'a pas reçu deux angles."); 
        }

        break;
      }

      //==============================================================================================================//
      // 2 : ...
      case 2: {                                                    
        int angle1;
        if (sscanf(command + 2, "%d", &angle1) == 1) { //Regarde s'il y a 1 angle
          _scara.setTablePos(angle1);
          _scara.tableisPos(angle1);
        }

        else{
        Serial.print("C2_error : La commande n'a pas reçu 1 angle."); 
        }

        break;
      }

      //==============================================================================================================//
      // 3 : ...
      case 3: {
        int angleGauche, angleDroite, angleTable;
        if (sscanf(command + 2, "%d %d %d", &angleGauche,  &angleDroite,  &angleTable) == 3) { //Regarde s'il y a 1 angle
          
          int position[2] = {angleGauche, angleDroite};

          _scara.setTablePos(angleTable);

          _scara.setSpeedForLinearMov(position,MAX_SCARA_SPEED);
          _scara.setScaraPos(position);

          int current_pos[2] = {_scara.getLastCmd()[0],_scara.getLastCmd()[1]};
          _scara.tableisPos(angleTable);
          _scara.jointisPos(current_pos);

          delay(200);
          
        }

        else{
        Serial.print("C3_error : La commande n'a pas reçu 3 angle."); 
        }
        break;
      }

      case 4: {
        while(true){
          _scara.doSeq(0);
          _scara.setTablePos(0);
          _scara.tableisPos(0);
          Serial.print('1');
          _scara.setTablePos(100);
          _scara.doSeq(0);
          _scara.tableisPos(100);
          Serial.print('1');
        }
        
        break;
      }
      
      case 5: {
        int angle1;
        if (sscanf(command + 2, "%d", &angle1) == 1) { //Regarde s'il y a 1 angle
          int CE = _scara.getLastCmd()[2];
          int CRT = floor(CE/4096)*4096 + angle1;
          int current_pos[2] = {_scara.getLastCmd()[0],_scara.getLastCmd()[1]};

          if(abs(CRT-CE)<2048){
            if(CRT>CE){
              _scara.setTablePos(CRT - _scara.range);
              _scara.tableisPos(CRT - _scara.range);
              //_scara.doSeq(0);
            }else{
               _scara.setTablePos(CRT + _scara.range);
               _scara.tableisPos(CRT + _scara.range);
               //_scara.doSeq(1);
            } 
          }else{
            if(CRT>CE){
              _scara.setTablePos(CRT - 4096 + _scara.range);
              _scara.tableisPos(CRT - 4096 + _scara.range);
              //_scara.doSeq(1);
            }else{
               _scara.setTablePos(CRT + 4096 - _scara.range);
               _scara.tableisPos(CRT + 4096 - _scara.range);
               //_scara.doSeq(1);
            } 
          }
        }
        Serial.println('erreur C5');
        break;
      }
    }
     Serial.println('1'); // Retourne 1 au programme Python pour demander une prochaine commande
  }
  else if (command[0] == 'T') {            // Regarde si le string commence par C
    char command_char = command[1];
    int command_int = command_char - '0';
    switch (command_int) { // Regarde le chiffre de commande
      case 0: {                                                      
        _scara.toggleTorque(0);
        Serial.println('1');    
        break;
      }
      case 1: {
        printPos();
        break;
      }
      case 2: {
        int i = 0;
        while(i<100){
          if(_dxl.readControlTableItem(MOVING, moteur_gauche) || _dxl.readControlTableItem(MOVING, moteur_droit))
          {
            _scara.seq0[i][0] = _scara.getDxlPos(moteur_gauche);
            Serial.println(_scara.seq0[i][0]);
            _scara.seq0[i][1] = _scara.getDxlPos(moteur_droit);
            Serial.println(_scara.seq0[i][1]);
            i++;
          }
          delay(30);
        }
        _scara.toggleTorque(1);
        break;
      }
    }
  }
}

void printPos(){
  int left_pos = _scara.getDxlPos(moteur_gauche);
  int right_pos = _scara.getDxlPos(moteur_droit);
  int table_pos = _scara.getDxlPos(moteur_table);
  Serial.println(left_pos);
  Serial.println(right_pos);
  Serial.println(table_pos);
}

