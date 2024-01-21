#include "Scara.h"

Scara::Scara() : _dxl(Serial1, -1)
{}

Scara::~Scara() {}

void Scara::init()
{
    Serial1.println("Initialisation des moteurs du Scara");
        //Serial.begin(57600); // Use UART port of DYNAMIXEL Shield to debug.
        _dxl.begin(57600); // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
        _dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION); // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
        _dxl.ping(moteur_gauche); // Get DYNAMIXEL information
        _dxl.ping(moteur_droit); 
        this->setSpeed(30);
        this->setAcceleration(30);

    Serial1.println("Init: moteur 1 (gauche)");
        _dxl.setID(moteur_gauche, 1);
        _dxl.ledOn(moteur_gauche);
        _dxl.torqueOff(moteur_gauche);
        _dxl.setOperatingMode(moteur_gauche, OP_POSITION);
        _dxl.torqueOn(moteur_gauche);  
        
        //if(this->getPos() != 0)
            //this->
    
    Serial1.println("Init: moteur 2 (droit)");
        _dxl.setID(moteur_droit, 1);
        _dxl.ledOn(moteur_droit);
        _dxl.torqueOff(moteur_droit);
        _dxl.setOperatingMode(moteur_droit, OP_POSITION);
        _dxl.torqueOn(moteur_droit);  

    Serial1.println("Initialisation completee");

}

void Scara::update()
{
    
}

// Switch to joint mode to cartesian and move in m/s {x, y}
void Scara::setPos(int jointPos[2])
{
    _dxl.setGoalPosition(moteur_gauche, jointPos[0]);
    _dxl.setGoalPosition(moteur_droit, jointPos[1]);
}

// Helper method for cartiesian movement, only done with first 2 joints
// TODO: optimise
// Return bool true if matrix could be inverted or false if singular matrix
bool Scara::buildInvJacobienne()
{
return false;
}

void Scara::printPosition()
{
    Serial1.print("Moteur_gauche: ");
    Serial1.print(Pos_current[0]);
    Serial1.print("\tMoteur_droit: ");
    Serial1.println(Pos_current[1]);
}

void Scara::sendDefaultPos()
{
    int jointPos[2] = {Pos_default[0], Pos_default[1]}; // or replace with your default positions
    this->setPos(jointPos);
}

int* Scara::getPos()
{
    Pos_current[0] = _dxl.getPresentPosition(moteur_gauche);
    Pos_current[1] = _dxl.getPresentPosition(moteur_droit);
    return Pos_current;
}

void Scara::setSpeed(uint8_t speedLimit)
{
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_droit, speedLimit);
    _dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_gauche, speedLimit);
}

void Scara::setAcceleration(uint8_t AccelLimit)
{
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_droit, AccelLimit);
    _dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_gauche, AccelLimit);
}
