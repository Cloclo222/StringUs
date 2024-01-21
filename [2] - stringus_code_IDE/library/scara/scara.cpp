#include "scara.h"
#include "src/library/Dynamixel2Arduino"



Scara::Scara()
{
    Dynamixel2Arduino dxl(DXL_SERIAL, DXL_DIR_PIN);

    DEBUG_SERIAL.begin(57600); // Use UART port of DYNAMIXEL Shield to debug.
    dxl.begin(57600); // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
    dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION); // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
    dxl.ping(moteur_gauche); // Get DYNAMIXEL information
    dxl.ping(moteur_droit); 

    //Motor parameter initilization
    dxl.torqueOff(moteur_gauche);
    dxl.torqueOff(moteur_droit);
    dxl.setOperatingMode(moteur_gauche, OP_POSITION);
    dxl.setOperatingMode(moteur_droit, OP_POSITION);
    dxl.torqueOn(moteur_gauche);
    dxl.torqueOn(moteur_droit);

}

Scara::~Scara() {}

void Scara::init()
{
    /*    LOG(INFO, "BrasShower initialisation...");
    _j0.init(&_j0Motor, 0.0f, 120.0f, 0.0f, -18500, 120.0f, 0, 0.0f);;
    LOG(INFO, "Calibrating J0...");

// Blocking call, needs to be skipped when power isn't ON
#ifdef WITH_ROBOT
    _j0.calib(true, 50U);
#endif // WITH_ROBOT
    LOG(INFO, "Done!");

    _j1.init(_j1Params1, _j1Params2, -160.0f, 20.0f, -15.0f, 90.0f, -168.0f, 0.0f, -45.0f);
    _j2.init(_j2Params, -90.0f, 90.0f, -90.0f, 180.0f, 90.0f, 0.0f);
    _j1.setPosOffset(10.0f);

    _guide.init(_guideParams);

    LOG(INFO, "BrasShower initialisation done!");
    
    this->setPos(_defaultPos);
    FOR_ALL(_joints)
    {
        _jointsGoals[i] = _joints[i]->getPos();
    }
    this->update();*/
}

void Scara::update()
{
    /*if (_mode == eJogMode::joint)
    {
        // LOG(INFO, "j0: %f, j1: %f", _jointsGoals[0], _jointsGoals[1]);
        _joints[0]->setPos(_jointsGoals[0]);
        _joints[1]->setPos(_jointsGoals[1]);
    }
    else if (_mode == eJogMode::cartesian)
    {
        LOG(WARN, "Not implemented");
        if (this->buildInvJacobienne())
        {
            Matrix.Multiply((mtx_type *)_invJacobienne, (mtx_type *)_speedCmd, 2, 2, 1, (mtx_type *)_jointsSpeedGoals);
        }
        else
        {
            // Led would be nice
            LOG(WARN, "Singular Matrix --> Jog in joints")
            return;
        }

        // TODO Make speed to pos calcs
        double dt = ((double)(_lastLoopTime - micros()) / (double)1000000.0f);
        float jointsPosAdd[2] = {0.0f, 0.0f};

        FOR_ALL(jointsPosAdd)
        {
            jointsPosAdd[i] = (float)((double)_jointsSpeedGoals[i] * dt);

            LOG(INFO, "J%icmd: %f\t", i, _jointsPos[i] + jointsPosAdd[i]);
            _joints[i]->setPos(_jointsPos[i] + jointsPosAdd[i]);
        }
        Serial.println();
    }

    // Last joint is controlled in absolute from nx
    _joints[2]->setPos(-(_jointsPos[0] + _jointsPos[1]) + _jointsGoals[2]);

    FOR_ALL(_joints)
    {
        _joints[i]->update();
        _jointsPos[i] = _joints[i]->getPos();
    }*/
}

void Scara::setEndEffectorPos(float posAbsDeg)
{
    //_jointsGoals[2] = posAbsDeg;
}

// Switch to joint mode to cartesian and move in m/s {x, y}
void Scara::setPos(float jointPos[3])
{
    
}

// Switch mode to cartesian and move in m/s {x, y}
void Scara::move(float cmd[2])
{

}

// Helper method for cartiesian movement, only done with first 2 joints
// TODO: optimise
// Return bool true if matrix could be inverted or false if singular matrix
bool Scara::buildInvJacobienne()
{

}

void Scara::printPosition()
{

}

void Scara::sendDefaultPos()
{

}

//Return array of three flaot representing the angles
float* Scara::getPos()
{

}

void Scara::openGuide()
{

}

void Scara::closeGuide()
{

}

void Scara::setSpeed(uint8_t speedLimit)
{
    dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_droit, speedLimit);
    dxl.writeControlTableItem(PROFILE_VELOCITY, moteur_gauche, speedLimit);
}

void Scara::setAcceleration(uint8_t AccelLimit);
{
    dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_droit, AccelLimit);
    dxl.writeControlTableItem(PROFILE_ACCELERATION, moteur_gauche, AccelLimit);
}
