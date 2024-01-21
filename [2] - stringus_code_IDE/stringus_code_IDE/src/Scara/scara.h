#ifndef __Scara_H__
#define __Scara_H__

#include <Dynamixel2Arduino.h>
#include "Arduino.h"


//Nos variables
#define moteur_gauche 1
#define moteur_droit 2
#define UP 180
#define DOWN 0

using namespace ControlTableItem;
#define DXL_SERIAL   Serial1

class Scara
{
private:
    Dynamixel2Arduino _dxl; //Si variable définit avec un "_" à l'avant, c'est un objet!
    const float DXL_PROTOCOL_VERSION = 2.0;

    const int Pos_default[2] = {0, 0};
    int Pos_current[2] = {0, 0};

public:
    Scara();
    ~Scara();
    void init_com();
    void init_moteur();
    void update();
    void setPos(int jointPos[2]);
    int* getPos(); 
    void move(float cmd[2]);
    bool buildInvJacobienne();
    void printPosition();
    void sendDefaultPos();
    void setSpeed(uint8_t speedLimit);
    void setAcceleration(uint8_t AccelLimit);
};

#endif //__SCARA_H__
