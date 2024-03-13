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
        _dxl.ping(moteur_table); // Get DYNAMIXEL information
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

    _dxl.torqueOff(moteur_table);
    _dxl.setOperatingMode(moteur_table, OP_POSITION);
    //_dxl.writeControlTableItem(MIN_POSITION_LIMIT, moteur_droit, 0);
    //_dxl.writeControlTableItem(MAX_POSITION_LIMIT, moteur_droit, 4095);
    _dxl.writeControlTableItem(DRIVE_MODE, moteur_table, 0);
    _dxl.writeControlTableItem(HOMING_OFFSET, moteur_table, 0);
    _dxl.ledOn(moteur_table);
    _dxl.torqueOn(moteur_table); 
}

void Scara::update()
{

}

void Scara::setScaraPos(int jointPos[2])
{
    _dxl.setGoalPosition(moteur_gauche, jointPos[0]);
    _dxl.setGoalPosition(moteur_droit, jointPos[1]);
    Pos_current[0] = jointPos[0];
    Pos_current[1] = jointPos[1];

}

void Scara::setTablePos(int TablePos)
{
    _dxl.setGoalPosition(moteur_table, TablePos);
    Pos_current[2] = TablePos;

}

void Scara::isPos(int jointPos[2], int TablePos) {
    bool isMoteurGaucheInPosition = false;
    bool isMoteurDroitInPosition = false;
    bool isMoteurTableInPosition = false;
    int marge_erreur = 10;
    
    while (!isMoteurGaucheInPosition || !isMoteurDroitInPosition || !isMoteurTableInPosition) {
        float currentPosGauche = _dxl.getPresentPosition(moteur_gauche);
        float currentPosDroit = _dxl.getPresentPosition(moteur_droit);
        float currentPosTable = _dxl.getPresentPosition(moteur_table);
        
        isMoteurGaucheInPosition = abs(currentPosGauche - jointPos[0]) <= marge_erreur;
        isMoteurDroitInPosition = abs(currentPosDroit - jointPos[1]) <= marge_erreur;
        isMoteurTableInPosition = abs(currentPosTable - TablePos) <= marge_erreur;
        
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
    int TablePos = Pos_default[2];
    this->setScaraPos(jointPos);
    this->setTablePos(TablePos);
}

int* Scara::getLastCmd()
{
    return Pos_current;
}

float Scara::getDxlPos(int moteur)
{
    float currentPosGauche = _dxl.getPresentPosition(moteur);
}

void Scara::toggleTorque(int i)
{
    if (i == 0){
        _dxl.torqueOff(moteur_gauche);
        _dxl.torqueOff(moteur_droit);
    }
    else if (i == 1){
        _dxl.torqueOn(moteur_gauche);
        _dxl.torqueOn(moteur_droit);
    }
    
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
    
    float leftDelta = abs(jointPos[0] - this->getLastCmd()[0]);
    float rightDelta = abs(jointPos[1] - this->getLastCmd()[1]);
    

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
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_table, 40);
    this->setAcceleration(0);


    _dxl.setGoalPosition(moteur_gauche, Pos_default[0]);
    _dxl.setGoalPosition(moteur_droit, Pos_default[1]);
    _dxl.setGoalPosition(moteur_table, Pos_default[2] );

    delay(3000);

    Pos_current[0] = _dxl.getPresentPosition(moteur_gauche);
    Pos_current[1] = _dxl.getPresentPosition(moteur_droit);
    Pos_current[2] = _dxl.getPresentPosition(moteur_table);
    
    return;
}