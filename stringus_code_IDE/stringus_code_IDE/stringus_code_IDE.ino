
#include <Dynamixel2Arduino.h> //Installer par le gestionnaire de librarie Arduino IDE
#include "src/Scara/Scara.h" //Dans le fichier src, c'est notre propre librarie
#include "Arduino.h"
#include "Wire.h"

#define DXL_SERIAL   Serial1
#define BUFFER_LENGTH 64
#define MAX_SCARA_SPEED 70
#define MAX_TABLE_SPEED 60
#define EEPROM_I2C_ADDRESS 0x50
#define LEFT_APPROACH_ADDRESS 0 // address to store left scara approach position in EEPROM (2x uint16_t = 4 bytes)
#define RIGHT_APPROACH_ADDRESS 4 // address to store right scara approach position in EEPROM (2x uint16_t = 4 bytes)
#define LEFT_SEQ_BASE_ADDRESS 8 // address of first element to store left scara circle sequence in EEPROM (50x2x uint16_t = 200 bytes)
#define RIGHT_SEQ_BASE_ADDRESS 208 // address of first element to store right scara circle sequence in EEPROM (50x2x uint16_t = 200 bytes)

char serialBuffer[BUFFER_LENGTH]; // Buffer pour les messages Serial
int bufferIndex = 0;              // Index pour le char dans serialBuffer

Dynamixel2Arduino _dxl(DXL_SERIAL, -1); 
Scara _scara(_dxl);

void serialControl(); 
void executeCommand(const char* command);
void updateScaraApproach(uint16_t * array, int address, int i2c_address);
void updateScaraSeq(uint16_t array[SCARA_SEQ_RES][2], int address, int num_pos, int i2c_address);
void write_uint16_EEPROM(int address, uint16_t val, int i2c_address);
uint16_t read_uint16_EEPROM(int address, int i2c_address, int numBytes);



void setup() {
    delay(5000);
    Serial.begin(115200);
    _dxl.begin(57600);
    Serial.println("Baudrate init.");

    _scara.init_com();
    Serial.println("Comunication init.");
    _scara.init_moteur();
    Serial.println("Moteur init.");
    
    Wire.begin();
    write_uint16_EEPROM(LEFT_APPROACH_ADDRESS, 2825, EEPROM_I2C_ADDRESS);
    write_uint16_EEPROM(LEFT_APPROACH_ADDRESS + 2, 1925, EEPROM_I2C_ADDRESS);
    updateScaraApproach(_scara.LeftApproach, LEFT_APPROACH_ADDRESS, EEPROM_I2C_ADDRESS);
    updateScaraApproach(_scara.RightApproach, RIGHT_APPROACH_ADDRESS, EEPROM_I2C_ADDRESS);
    updateScaraSeq(_scara.seqClou[0], LEFT_SEQ_BASE_ADDRESS, SCARA_SEQ_RES, EEPROM_I2C_ADDRESS);
    updateScaraSeq(_scara.seqClou[1], RIGHT_SEQ_BASE_ADDRESS, SCARA_SEQ_RES, EEPROM_I2C_ADDRESS);
    Wire.end();

    
    
    delay(100);
    _scara.setAcceleration(15,5);
    _scara.homing();
    _scara.setSpeed(MAX_SCARA_SPEED, MAX_SCARA_SPEED);
    _scara.setTableSpeed(MAX_TABLE_SPEED);
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
          uint16_t position[2] = {angle1, angle2};
          _scara.setSpeedForLinearMov(position,MAX_SCARA_SPEED);
          _scara.setScaraPos(position);
          int current_table_pos = _scara.getLastCmd()[2];
          // Serial.println("im in isPos");
          _scara.jointisPos(position);
          // Serial.println("im out isPos");
          
        }

        else{
        // Serial.print("C1_error : La commande n'a pas reçu deux angles."); 
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
        // Serial.print("C2_error : La commande n'a pas reçu 1 angle."); 
        }

        break;
      }

      //==============================================================================================================//
      // 3 : ...
      case 3: {
        int angleGauche, angleDroite, angleTable;
        if (sscanf(command + 2, "%d %d %d", &angleGauche,  &angleDroite,  &angleTable) == 3) { //Regarde s'il y a 1 angle
          
          uint16_t position[2] = {angleGauche, angleDroite};

          _scara.setTablePos(angleTable);

          _scara.setSpeedForLinearMov(position,MAX_SCARA_SPEED);
          _scara.setScaraPos(position);

          uint16_t current_pos[2] = {_scara.getLastCmd()[0],_scara.getLastCmd()[1]};
          _scara.tableisPos(angleTable);
          _scara.jointisPos(current_pos);

          delay(200);
          
        }

        else{
        // Serial.print("C3_error : La commande n'a pas reçu 3 angle."); 
        }
        break;
      }

      case 4: {
       _scara.doSeq(0);
     
      
        
        break;
      }
      
      case 5: {
        int angle1;
        if (sscanf(command + 2, "%d", &angle1) == 1) { //Regarde s'il y a 1 angle
          int CE = _scara.getLastCmd()[2]; // Current Encoder position
          int CRT = floor(CE/4096)*4096 + angle1; // Current Revolution Target
          int current_pos[2] = {_scara.getLastCmd()[0],_scara.getLastCmd()[1]};

          if(abs(CRT-CE)<2048){
            if(CRT>CE){
              _scara.setTablePos(CRT - _scara.range);
              _scara.setScaraPos(_scara.LeftApproach);
              _scara.jointisPos(_scara.LeftApproach);
              _scara.tableisPos(CRT - _scara.range);
              _scara.doSeq(0);
              _scara.setScaraPos(_scara.LeftApproach);
              _scara.jointisPos(_scara.LeftApproach);
            }else{
               _scara.setTablePos(CRT + _scara.range);
               _scara.setScaraPos(_scara.RightApproach);
               _scara.jointisPos(_scara.RightApproach);
               _scara.tableisPos(CRT + _scara.range);
               _scara.doSeq(1);
               _scara.setScaraPos(_scara.RightApproach);
               _scara.jointisPos(_scara.RightApproach);
            } 
          }else{
            if(CRT>CE){
              _scara.setTablePos(CRT - 4096 + _scara.range);
              _scara.setScaraPos(_scara.RightApproach);
              _scara.jointisPos(_scara.RightApproach);
              _scara.tableisPos(CRT - 4096 + _scara.range);
              _scara.doSeq(1);
              _scara.setScaraPos(_scara.RightApproach);
              _scara.jointisPos(_scara.RightApproach);
            }else{
               _scara.setTablePos(CRT + 4096 - _scara.range);
               _scara.setScaraPos(_scara.LeftApproach);
               _scara.jointisPos(_scara.LeftApproach);
               _scara.tableisPos(CRT + 4096 - _scara.range);
               _scara.doSeq(0);
               _scara.setScaraPos(_scara.LeftApproach);
               _scara.jointisPos(_scara.LeftApproach);
            } 
          }
        }
        // Serial.println('erreur C5');
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
        _scara.toggleTorque(1);
        Serial.println('1');
        break;
      }
      case 2: {
        printPos();
        break;
      }
      case 3: {
        int i = 0;
        while(i<SCARA_SEQ_RES){
          if(_dxl.readControlTableItem(MOVING, moteur_gauche) || _dxl.readControlTableItem(MOVING, moteur_droit))
          {
            _scara.seqCalib[i][0] = _scara.getDxlPos(moteur_gauche);
            Serial.println(_scara.seqCalib[i][0]);
            _scara.seqCalib[i][1] = _scara.getDxlPos(moteur_droit);
            Serial.println(_scara.seqCalib[i][1]);
            i++;
          }
          delay(30);
        }
        _scara.toggleTorque(1);
        break;
      }
    }
  }
  else if (command[0] == 'W') {          
    char command_char = command[1];
    int command_int = command_char - '0';
    switch (command_int) { // Regarde le chiffre de commande
      case 0: {   // calibrer approche gauche
        Wire.begin();
        write_uint16_EEPROM(LEFT_APPROACH_ADDRESS, (uint16_t) _scara.getDxlPos(moteur_gauche), EEPROM_I2C_ADDRESS);
        write_uint16_EEPROM(LEFT_APPROACH_ADDRESS + 2, (uint16_t) _scara.getDxlPos(moteur_droit), EEPROM_I2C_ADDRESS);
        updateScaraApproach(_scara.LeftApproach, LEFT_APPROACH_ADDRESS, EEPROM_I2C_ADDRESS);
        Wire.end();
        Serial.println('1');                                                      
        break;
      }
      case 1: { // calibrer approche droite
        Wire.begin();
        write_uint16_EEPROM(RIGHT_APPROACH_ADDRESS, (uint16_t) _scara.getDxlPos(moteur_gauche), EEPROM_I2C_ADDRESS);
        write_uint16_EEPROM(RIGHT_APPROACH_ADDRESS + 2, (uint16_t) _scara.getDxlPos(moteur_droit), EEPROM_I2C_ADDRESS);      
        updateScaraApproach(_scara.RightApproach, RIGHT_APPROACH_ADDRESS, EEPROM_I2C_ADDRESS); 
        Wire.end();
        Serial.println('1');    
        break;
      }
      case 2: { // calibrer sequence gauche
        Wire.begin();
        int i = 0;
        while(i< 4 * SCARA_SEQ_RES){
          while(!_dxl.readControlTableItem(MOVING, moteur_gauche) && !_dxl.readControlTableItem(MOVING, moteur_droit))
          {
          }
          write_uint16_EEPROM(LEFT_SEQ_BASE_ADDRESS+i, (uint16_t) _scara.getDxlPos(moteur_gauche), EEPROM_I2C_ADDRESS);
          write_uint16_EEPROM(LEFT_SEQ_BASE_ADDRESS+i+2, (uint16_t) _scara.getDxlPos(moteur_droit), EEPROM_I2C_ADDRESS);
          delay(60);
          i += 4;
        }
        _scara.toggleTorque(1);
        updateScaraSeq(_scara.seqClou[0], LEFT_SEQ_BASE_ADDRESS, SCARA_SEQ_RES, EEPROM_I2C_ADDRESS);
        Wire.end();
        Serial.println('1');
        break;
      }
      case 3: { // calibrer sequence droite
        Wire.begin();
        int i = 0;
        while(i< 4 * SCARA_SEQ_RES){
          while(!_dxl.readControlTableItem(MOVING, moteur_gauche) && !_dxl.readControlTableItem(MOVING, moteur_droit))
          {
          }
          write_uint16_EEPROM(RIGHT_SEQ_BASE_ADDRESS+i, (uint16_t) _scara.getDxlPos(moteur_gauche), EEPROM_I2C_ADDRESS);
          write_uint16_EEPROM(RIGHT_SEQ_BASE_ADDRESS+i+2, (uint16_t) _scara.getDxlPos(moteur_droit), EEPROM_I2C_ADDRESS);
          delay(60);
          i += 4;
        }
        _scara.toggleTorque(1);
        updateScaraSeq(_scara.seqClou[1], RIGHT_SEQ_BASE_ADDRESS, SCARA_SEQ_RES, EEPROM_I2C_ADDRESS);
        Wire.end();
        Serial.println('1');
        break;
      }
      case 4: { // playback approche gauche
        Serial.println("Play back left approach");
        _scara.toggleTorque(1);
        _scara.setScaraPos(_scara.LeftApproach);
        _scara.jointisPos(_scara.LeftApproach);
        Serial.println('1');
        break;
      }
      case 5: { // playback approche droite
        Serial.println("Play back right approach");
        _scara.toggleTorque(1);
        _scara.setScaraPos(_scara.RightApproach);
        _scara.jointisPos(_scara.RightApproach);
        Serial.println('1');
        break;
      }
      case 6: { // playback approche + sequence gauche
        Serial.println("Play back left sequence");
        _scara.toggleTorque(1);
        _scara.setScaraPos(_scara.LeftApproach);
        _scara.jointisPos(_scara.LeftApproach);
        _scara.doSeq(0);
        _scara.setScaraPos(_scara.LeftApproach);
        _scara.jointisPos(_scara.LeftApproach);
        Serial.println('1');
        break;
      }
      case 7: { // playback approche + sequence droite
        Serial.println("Play back right sequence");
        _scara.toggleTorque(1);
        _scara.setScaraPos(_scara.RightApproach);
        _scara.jointisPos(_scara.RightApproach);
        _scara.doSeq(1);
        _scara.setScaraPos(_scara.RightApproach);
        _scara.jointisPos(_scara.RightApproach);
        Serial.println('1');
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

void updateScaraApproach(uint16_t * array, int address, int i2c_address){
  array[0] = read_uint16_EEPROM(address, i2c_address, 2);
  array[1] = read_uint16_EEPROM(address+2, i2c_address, 2);
}

void updateScaraSeq(uint16_t array[SCARA_SEQ_RES][2], int address, int num_pos, int i2c_address){
  for(int i = 0; i<num_pos; i++){
    array[i][0] = read_uint16_EEPROM(address+(4*i), i2c_address, 2);
    array[i][1] = read_uint16_EEPROM(address+(4*i)+2, i2c_address, 2);
  }
}

// Function to write to EEPROOM
void write_uint16_EEPROM(int address, uint16_t val, int i2c_address = EEPROM_I2C_ADDRESS)
{
  // Begin transmission to I2C EEPROM
  Wire.beginTransmission(i2c_address);

  // Send memory address as two 8-bit bytes
  Wire.write((int)(address >> 8));   // MSB
  Wire.write((int)(address & 0xFF)); // LSB

  // Send data to be stored
  char buff[64];
  sprintf(buff, "value to be written at address %d : %d", address, val);
  byte data[2] = {(val >> 8), (val & 0xff)};

  Serial.println(buff);
  Wire.write(data, 2);

  // End the transmission
  Wire.endTransmission();

  // Add 5ms delay for EEPROM
  delay(5);
}

// Function to read from EEPROM
uint16_t read_uint16_EEPROM(int address, int i2c_address = EEPROM_I2C_ADDRESS, int numBytes = 2)
{
  // Define byte for received data
  uint16_t rcvData = 0;

  // Begin transmission to I2C EEPROM
  Wire.beginTransmission(i2c_address);

  // Send memory address as two 8-bit bytes
  Wire.write((int)(address >> 8));   // MSB
  Wire.write((int)(address & 0xFF)); // LSB

  int ret;
  // End the transmission
  ret = Wire.endTransmission();
  //Serial.println(ret);
  
  Wire.requestFrom(i2c_address, 2);

  // Read the data and assign to variable
  byte MSB =  Wire.read();
  byte LSB = Wire.read();
  rcvData = ((uint16_t) MSB << 8) | LSB;
  char buff[64];
  sprintf(buff, "value read at address %d : %d", address, rcvData);
  Serial.println(buff);
  // Return the data as function output
  return rcvData;
}
