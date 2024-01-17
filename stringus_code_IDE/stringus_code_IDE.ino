#include <Arduino.h>
/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#include <Dynamixel2Arduino.h>


//OpenRB does not require the DIR control pin.
#define DXL_SERIAL Serial1
#define DEBUG_SERIAL Serial
const int DXL_DIR_PIN = -1;
const float DXL_PROTOCOL_VERSION = 2.0;
Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);
using namespace ControlTableItem;


#define moteur_gauche 1
#define moteur_droit 2
#define UP 180
#define DOWN 0


void setup() {
  
  
  DEBUG_SERIAL.begin(57600); // Use UART port of DYNAMIXEL Shield to debug.
  dxl.begin(57600); // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION); // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.ping(moteur_gauche); // Get DYNAMIXEL information
  dxl.ping(moteur_droit); 

  //Motor parameter initilization
  dxl.torqueOff(moteur_gauche);
  dxl.torqueOff(moteur_droit);
  dxl.setOperatingMode(moteur_gauche, OP_POSITION);
  dxl.setOperatingMode(moteur_droit, OP_POSITION);
  dxl.torqueOn(moteur_gauche);
  dxl.torqueOn(moteur_droit);
}

void loop() {
 
  dxl.setGoalPosition(moteur_gauche, 0);
  dxl.setGoalPosition(moteur_droit, 0);
  delay(3000);
  dxl.setGoalPosition(moteur_gauche, 1000);
  dxl.setGoalPosition(moteur_droit, 1000);
  delay(3000);

  /*switch(key_input) { //Contrôle de vitesse et acceleration
    case '1':
      // Low Profile Acceleration, High Profile Velocity
      // Refer to API documentation for available parameters
      // http://emanual.robotis.com/docs/en/parts/interface/dynamixel_shield/#dynamixelshieldv010-or-above
      dxl.writeControlTableItem(PROFILE_ACCELERATION, DXL_ID, 50);
      dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID, 300);
      break;
    case '2':
      // Max Profile Acceleration, Low Profile Velocity
      dxl.writeControlTableItem(PROFILE_ACCELERATION, DXL_ID, 0);
      dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID, 100);
      break;
    case '3':
      // Max Profile Acceleration, Max Profile Velocity
      // WARNING : Please BE AWARE that this option will make a vibrant motion for PRO(A) or PRO+ series that requires high current supply.
      dxl.writeControlTableItem(PROFILE_ACCELERATION, DXL_ID, 0);
      dxl.writeControlTableItem(PROFILE_VELOCITY, DXL_ID, 0);
      break;
    default:
      break;
  }*/
}
