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
    int range = 491;
    int seq0[100][2];
    int seq1[100][2];
    int seqOfficial[100][2] = {{2553, 2559},
{2551, 2559},
{2543, 2551},
{2532, 2538},
{2518, 2522},
{2504, 2504},
{2490, 2485},
{2477, 2466},
{2468, 2447},
{2462, 2425},
{2460, 2404},
{2462, 2379},
{2465, 2353},
{2471, 2332},
{2481, 2312},
{2493, 2296},
{2505, 2281},
{2515, 2269},
{2530, 2257},
{2545, 2246},
{2562, 2238},
{2580, 2232},
{2599, 2231},
{2619, 2230},
{2641, 2231},
{2661, 2234},
{2684, 2238},
{2704, 2247},
{2724, 2257},
{2742, 2267},
{2760, 2279},
{2778, 2293},
{2796, 2310},
{2808, 2328},
{2818, 2348},
{2824, 2372},
{2828, 2397},
{2831, 2421},
{2832, 2447},
{2833, 2474},
{2832, 2502},
{2831, 2526},
{2828, 2546},
{2824, 2563},
{2817, 2580},
{2806, 2595},
{2794, 2608},
{2779, 2617},
{2765, 2626},
{2751, 2633},
{2736, 2639},
{2719, 2642},
{2702, 2643},
{2684, 2643},
{2665, 2643},
{2645, 2642},
{2624, 2640},
{2604, 2637},
{2586, 2633},
{2570, 2626},
{2555, 2617},
{2542, 2606},
{2532, 2596},
{2523, 2584},
{2517, 2569},
{2514, 2556},
{2513, 2541},
{2513, 2522},
{2514, 2502},
{2516, 2484},
{2518, 2464},
{2522, 2445},
{2529, 2428},
{2538, 2413},
{2551, 2400},
{2564, 2391},
{2576, 2383},
{2587, 2378},
{2599, 2378},
{2609, 2383},
{2622, 2390},
{2635, 2400},
{2647, 2412},
{2655, 2425},
{2661, 2439},
{2667, 2455},
{2670, 2475},
{2670, 2495},
{2669, 2517},
{2661, 2533},
{2649, 2547},
{2633, 2559},
{2618, 2569},
{2602, 2577},
{2586, 2583},
{2572, 2585},
{2559, 2586},
{2546, 2584},
{2535, 2581},
{2523, 2574}
};
    Scara(Dynamixel2Arduino &dxl);
    ~Scara();
    void init_com();
    void init_moteur();
    void update();
    void setScaraPos(int jointPos[2]);
    void doSeq(int side);
    void setTablePos(int TablePos);
    void jointisPos(int jointPos[2]);
    void tableisPos(int TablePos);
    int* getLastCmd(); 
    float getDxlPos(int moteur);
    void toggleTorque(int i);
    void move(float cmd[2]);
    bool buildInvJacobienne();
    void printPosition();
    void sendDefaultPos();
    void setSpeed(uint8_t speedLimitRight, uint8_t speedLimitLeft);
    void setSpeedForLinearMov(int jointPos[2], uint8_t speedLimit);
    void setAcceleration(uint8_t AccelLimitBras, uint8_t AccelLimitTable);
    int* getSpeedAccel();
    void homing();

};

#endif //__SCARA_H__
