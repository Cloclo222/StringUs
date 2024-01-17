#ifndef __SCARA_H__
#define __SCARA_H__

#define NB_JOINTS 3
#define SERVO_GUIDE Servo_8
#define GUIDE_POS_CLOSE 160
#define GUIDE_POS_OPEN 20

class BrasShower
{
public:
    //variable public


private:
    //variable public


public:
    BrasShower();
    ~BrasShower();
    void init();
    void update();
    void setPos(float jointPos[2]);
    float *getPos();
    void move(float cmd[2]);
    bool buildInvJacobienne();
    void printPosition();
    void sendDefaultPos();
    void openGuide();
    void closeGuide();
    void setSpeed(uint8_t speedLimit);
};

#endif //__BRAS_H__
