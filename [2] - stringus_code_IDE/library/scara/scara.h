#ifndef __SCARA_H__
#define __SCARA_H__
#define moteur_gauche 1
#define moteur_droit 2
#define UP 180
#define DOWN 0
#define DXL_SERIAL Serial1
#define DEBUG_SERIAL Serial
using namespace ControlTableItem;

class Scara
{
public:
    Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);

private:
    const int DXL_DIR_PIN = -1;
    const float DXL_PROTOCOL_VERSION = 2.0;

public:
    Scara(DXL_SERIAL, DXL_DIR_PIN);
    ~Scara();
    void init();
    void update();
    void setPos(float jointPos[2]);
    float *getPos();
    void move(float cmd[2]);
    bool buildInvJacobienne();
    void printPosition();
    void sendDefaultPos();
    void setSpeed(uint8_t speedLimit);
    void setAcceleration(uint8_t AccelLimit);
};

#endif //__SCARA_H__
