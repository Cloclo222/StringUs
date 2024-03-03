#include "scara.h"
#include <cmath>


Scara::Scara(Dynamixel2Arduino &dxl) : _dxl(dxl) {}

Scara::~Scara() {}

void Scara::init_com()
{
        
        //Serial.begin(115200);  // initialise Serial DEBUG_SERIAL port
        //while (!Serial);
        _dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION); // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
        _dxl.ping(moteur_gauche); // Get DYNAMIXEL information
        _dxl.ping(moteur_droit); // Get DYNAMIXEL information
}

void Scara::init_moteur()
{
    _dxl.torqueOff(moteur_gauche);
    _dxl.setOperatingMode(moteur_gauche, OP_POSITION);
   // _dxl.writeControlTableItem(MIN_POSITION_LIMIT, moteur_gauche, 0);
    //_dxl.writeControlTableItem(MAX_POSITION_LIMIT, moteur_gauche, 4095);
    _dxl.writeControlTableItem(DRIVE_MODE, moteur_gauche, 0);
    _dxl.writeControlTableItem(HOMING_OFFSET, moteur_gauche, 0);
    _dxl.ledOn(moteur_gauche);
    _dxl.torqueOn(moteur_gauche); 

    _dxl.torqueOff(moteur_droit);
    _dxl.setOperatingMode(moteur_droit, OP_POSITION);
    //_dxl.writeControlTableItem(MIN_POSITION_LIMIT, moteur_droit, 0);
    //_dxl.writeControlTableItem(MAX_POSITION_LIMIT, moteur_droit, 4095);
    _dxl.writeControlTableItem(DRIVE_MODE, moteur_droit, 1);
    _dxl.writeControlTableItem(HOMING_OFFSET, moteur_droit, 0);
    _dxl.ledOn(moteur_droit);
    _dxl.torqueOn(moteur_droit);  
}

void Scara::update()
{

}

// Switch to joint mode to cartesian and move in m/s {x, y}
void Scara::setPos(int jointPos[2])
{
    _dxl.setGoalPosition(moteur_gauche, jointPos[0], UNIT_DEGREE);
    _dxl.setGoalPosition(moteur_droit, jointPos[1], UNIT_DEGREE);
    Pos_current[0] = jointPos[0];
    Pos_current[1] = jointPos[1];

}

void Scara::isPos(int jointPos[2]) {
    bool isMoteurGaucheInPosition = false;
    bool isMoteurDroitInPosition = false;
    float marge_erreur = 1.0;
    
    while (!isMoteurGaucheInPosition || !isMoteurDroitInPosition) {
        float currentPosGauche = _dxl.getPresentPosition(moteur_gauche, UNIT_DEGREE);
        float currentPosDroit = _dxl.getPresentPosition(moteur_droit, UNIT_DEGREE);
        
        isMoteurGaucheInPosition = abs(currentPosGauche - jointPos[0]) <= marge_erreur;
        isMoteurDroitInPosition = abs(currentPosDroit - jointPos[1]) <= marge_erreur;
        
        delay(200); // Delay to prevent overwhelming the controller with requests.
    }
}

bool Scara::buildInvJacobienne()
{
return false;
}

void Scara::sendDefaultPos()
{
    int jointPos[2] = {Pos_default[0], Pos_default[1]}; // or replace with your default positions
    this->setPos(jointPos);
}

int* Scara::getPos()
{
    return Pos_current;
}

void Scara::setSpeed(uint8_t speedLimitLeft, uint8_t speedLimitRight)
{
    using namespace ControlTableItem;
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_droit, speedLimitRight);
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_gauche, speedLimitLeft);
    this->SpeedAccel[0] = speedLimitRight;
}

void Scara::setSpeedForLinearMov(int jointPos[2], uint8_t speedLimit)
{
    
    float leftDelta = abs(jointPos[0] - this->getPos()[0]);
    float rightDelta = abs(jointPos[1] - this->getPos()[1]);
    

    if (leftDelta > rightDelta)
    {
        float ratio = rightDelta/leftDelta;
        float speedLimitMod = speedLimit * ratio;
        uint8_t result = round(speedLimitMod);
        setSpeed(speedLimit,result);
        //setSpeed(5,20);
    }
    else if (rightDelta > leftDelta)
    {
        float ratio = leftDelta/rightDelta;
        float speedLimitMod = speedLimit * ratio;
        uint8_t result = round(speedLimitMod);
        setSpeed(result,speedLimit);
        //setSpeed(5,20);
    }
    else if(rightDelta == leftDelta)
    {
        setSpeed(speedLimit, speedLimit);
    }

}

void Scara::setAcceleration(uint8_t AccelLimit)
{
    using namespace ControlTableItem;
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_droit, AccelLimit);
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_gauche, AccelLimit);
    this->SpeedAccel[1] = AccelLimit;
}

int* Scara::getSpeedAccel()
{
    return SpeedAccel;
}

void Scara::homing(){

    this->setSpeed(20,20);
    this->setAcceleration(0);


    _dxl.setGoalPosition(moteur_gauche, Pos_default[0], UNIT_DEGREE);
    _dxl.setGoalPosition(moteur_droit, Pos_default[1], UNIT_DEGREE);

    delay(3000);
    
    return;
}