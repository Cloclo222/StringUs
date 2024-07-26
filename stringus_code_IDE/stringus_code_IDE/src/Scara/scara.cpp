#include "scara.h"
//#include <cmath>

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
    _dxl.writeControlTableItem(MOVING_THRESHOLD, moteur_gauche, 1);
    _dxl.ledOn(moteur_gauche);
    _dxl.torqueOn(moteur_gauche); 

    _dxl.torqueOff(moteur_droit);
    _dxl.setOperatingMode(moteur_droit, OP_POSITION);
    //_dxl.writeControlTableItem(MIN_POSITION_LIMIT, moteur_droit, 0);
    //_dxl.writeControlTableItem(MAX_POSITION_LIMIT, moteur_droit, 4095);
    _dxl.writeControlTableItem(DRIVE_MODE, moteur_droit, 1);
    _dxl.writeControlTableItem(HOMING_OFFSET, moteur_droit, 0);
    _dxl.writeControlTableItem(MOVING_THRESHOLD, moteur_droit, 1);
    _dxl.ledOn(moteur_droit);
    _dxl.torqueOn(moteur_droit);  

    _dxl.torqueOff(moteur_table);
    _dxl.setOperatingMode(moteur_table, OP_EXTENDED_POSITION);
    //_dxl.writeControlTableItem(MIN_POSITION_LIMIT, moteur_droit, 0);
    //_dxl.writeControlTableItem(MAX_POSITION_LIMIT, moteur_droit, 4095);
    _dxl.writeControlTableItem(DRIVE_MODE, moteur_table, 0);
    _dxl.writeControlTableItem(HOMING_OFFSET, moteur_table,10);
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

void Scara::doSeq(int side){
// Serial.println("Je suis entre dans doSeq");
  for(int i = 0; i < 100; i++)
    {
        this->setScaraPos(this->seqClou[side][i]);
        delay(5);
    }
// Serial.println("Je suis sorti de doSeq");
}

void Scara::setTablePos(int TablePos)
{
    // Serial.println("Je suis entre dans setTablepos");
    _dxl.setGoalPosition(moteur_table, TablePos);
    Pos_current[2] = TablePos;
    // Serial.println("Je suis sorti de setTablepos");

}

void Scara::jointisPos(int jointPos[2]) {
    bool isMoteurGaucheInPosition = false;
    bool isMoteurDroitInPosition = false;
    int marge_erreur = 10;
    
    // Serial.println("Je suis entre dans jointispos");
    while (!isMoteurGaucheInPosition || !isMoteurDroitInPosition) {
        int currentPosGauche = _dxl.getPresentPosition(moteur_gauche);
        int currentPosDroit = _dxl.getPresentPosition(moteur_droit);
        // Serial.println(abs(jointPos[0]- currentPosGauche));
        // Serial.println(abs(jointPos[1]- currentPosDroit));
        isMoteurGaucheInPosition = abs(jointPos[0]- currentPosGauche) <= marge_erreur;
        isMoteurDroitInPosition = abs(jointPos[1]- currentPosDroit) <= marge_erreur;
        delay(50);
    }
    // Serial.println("Je suis sorti de jointispos");
}

void Scara::tableisPos(int TablePos) {
    bool isMoteurTableInPosition = false;
    int marge_erreur = 2;
    
    // Serial.println("Je suis entre dans tableispos");
    while (!isMoteurTableInPosition) {
        int currentPosTable = _dxl.getPresentPosition(moteur_table);
        isMoteurTableInPosition = abs(currentPosTable - TablePos) <= marge_erreur;
        delay(50); // Delay to prevent overwhelming the controller with requests.
    }
    // Serial.println("Je suis sorti de tableispos");
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
    int currentPosGauche = _dxl.getPresentPosition(moteur);
    return currentPosGauche;
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

void Scara::setTableSpeed(uint8_t speedLimitTable)
{
    using namespace ControlTableItem;
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_table, speedLimitTable);
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

void Scara::setAcceleration(uint8_t AccelLimitBras, uint8_t AccelLimitTable)
{
    using namespace ControlTableItem;
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_droit, AccelLimitBras);
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_gauche, AccelLimitBras);
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_table, AccelLimitTable);
    this->SpeedAccel[1] = AccelLimitTable;
}

int* Scara::getSpeedAccel()
{
    return SpeedAccel;
}

void Scara::homing(){

    this->setSpeed(20,20);
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_table, 40);

    _dxl.setGoalPosition(moteur_gauche, Pos_default[0]);
    _dxl.setGoalPosition(moteur_droit, Pos_default[1]);
    _dxl.setGoalPosition(moteur_table, Pos_default[2] );

    delay(3000);

    Pos_current[0] = _dxl.getPresentPosition(moteur_gauche);
    Pos_current[1] = _dxl.getPresentPosition(moteur_droit);
    Pos_current[2] = _dxl.getPresentPosition(moteur_table);
    
    return;
}