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
#include <C:\Users\loicu\OneDrive\Documents\[5] - Repo Git\StringUs\StringUs\stringus_code_IDE\library\scara\scara.h>

void setup() {
  Scara bras();
}

void loop() {
 
  dxl.setGoalPosition(moteur_gauche, 0);
  dxl.setGoalPosition(moteur_droit, 0);
  delay(3000);
  dxl.setGoalPosition(moteur_gauche, 1000);
  dxl.setGoalPosition(moteur_droit, 1000);
  delay(3000);


}
