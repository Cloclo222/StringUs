#ifndef __Scara_H__
#define __Scara_H__

#include <Dynamixel2Arduino.h>
#include "Arduino.h"

//Nos variables
#define moteur_gauche 1
#define moteur_droit 2
#define moteur_table 3
#define UP 180
#define DOWN 0

using namespace ControlTableItem;
#define DXL_SERIAL   Serial1

class Scara
{
private:
    Dynamixel2Arduino &_dxl;
    const float DXL_PROTOCOL_VERSION = 2.0;
    int Pos_default[3] = {2560, 2560, 0};
    int Pos_current[3] = {0, 0, 0};
    int SpeedAccel[2] = {0, 0};
    
    

public:
    int range = 512; // 4096 pulses per rotation * 0.125 of full rotation, correct nail will always be offset by 512 pulses
    int seqCalib[100][2];
    uint16_t LeftApproach[2] = {2560, 2560};
    uint16_t RightApproach[2] = {1952, 2800};
    uint16_t seqClou[2][SCARA_SEQ_RES][2] = {{{2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560}},
                                  {{2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560},
                                   {2560, 2560}}};

    Scara(Dynamixel2Arduino &dxl);
    ~Scara();
    void init_com();
    void init_moteur();
    void update();
    void setScaraPos(uint16_t jointPos[2]);
    void doSeq(int side);
    void setTablePos(int TablePos);
    void jointisPos(uint16_t jointPos[2]);
    void tableisPos(int TablePos);
    int* getLastCmd(); 
    float getDxlPos(int moteur);
    void toggleTorque();
    void TorqueOn();
    void TorqueOff();
    void move(float cmd[2]);
    bool buildInvJacobienne();
    void printPosition();
    void sendDefaultPos();
    void setSpeed(uint8_t speedLimitRight, uint8_t speedLimitLeft);
    void setTableSpeed(uint8_t speedLimitTable);
    void setSpeedForLinearMov(uint16_t jointPos[2], uint8_t speedLimit);
    void setAcceleration(uint8_t AccelLimitBras, uint8_t AccelLimitTable);
    int* getSpeedAccel();
    void homing();

};

#endif //__SCARA_H__
