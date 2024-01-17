#include "system/bras_shower.h"

BrasShower::BrasShower()
{
}

BrasShower::~BrasShower() {}

void BrasShower::init()
{
    LOG(INFO, "BrasShower initialisation...");
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
    this->update();
}

void BrasShower::update()
{
    if (_mode == eJogMode::joint)
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
    }
}

void BrasShower::setEndEffectorPos(float posAbsDeg)
{
    _jointsGoals[2] = posAbsDeg;
}

// Switch to joint mode to cartesian and move in m/s {x, y}
void BrasShower::setPos(float jointPos[3])
{
    _mode = eJogMode::joint;
    _jointsGoals[0] = jointPos[0];
    _jointsGoals[1] = jointPos[1];

    this->setEndEffectorPos(jointPos[2]);
}

// Switch mode to cartesian and move in m/s {x, y}
void BrasShower::move(float cmd[2])
{
    _mode = eJogMode::cartesian;
    _speedCmd[0] = cmd[0];
    _speedCmd[1] = cmd[1];
}

// Helper method for cartiesian movement, only done with first 2 joints
// TODO: optimise
// Return bool true if matrix could be inverted or false if singular matrix
bool BrasShower::buildInvJacobienne()
{
    const float j0x = 0.0f;
    const float j0y = 0.0f;
    const float j1x = 0.0f;
    const float j1y = 0.0f;
    const float j2x = 0.0f;
    const float j2y = 0.0f;

    float theta_0 = radians(_jointsPos[0]);
    float theta_1 = radians(_jointsPos[1]);
    // Might want to evalute new pos
    float theta_2 = radians(_jointsPos[2]);

    // nx = j0x*cos(theta_0) + j1x*cos(theta_0+theta_1) + 0.5*j2x*cos(theta_0+theta_1+theta_2) - j0y*sin(theta_0) - j1y*sin(theta_0+theta_1) - 0.5*j2y*sin(theta_0+theta_1+theta_2)
    _invJacobienne[0][0] = (double)(j0x * -sin(theta_0) + j1x * -sin(theta_0 + theta_1) + 0.5 * j2x * -sin(theta_0 + theta_1 + theta_2) - j0y * cos(theta_0) - j1y * cos(theta_0 + theta_1) - 0.5 * j2y * cos(theta_0 + theta_1 + theta_2));
    _invJacobienne[0][1] = (double)(j1x * -sin(theta_0 + theta_1) + 0.5 * j2x * -sin(theta_0 + theta_1 + theta_2) - j1y * cos(theta_0 + theta_1) - 0.5 * j2y * cos(theta_0 + theta_1 + theta_2));

    // ny = j0x*sin(theta_0) + j0y*cos(theta_0) + j1x*sin(theta_0+theta_1) + j1y*cos(theta_0+theta_1) + 0.5*j2x*sin(theta_0+theta_1+theta_2) + 0.5*j2y*cos(theta_0+theta_1+theta_2)
    _invJacobienne[1][0] = (double)(j0x * cos(theta_0) + j0y * -sin(theta_0) + j1x * cos(theta_0 + theta_1) + j1y * -sin(theta_0 + theta_1) + 0.5 * j2x * cos(theta_0 + theta_1 + theta_2) + 0.5 * j2y * -sin(theta_1 + theta_2));
    _invJacobienne[1][1] = (double)(j1x * cos(theta_0 + theta_1) + j1y * -sin(theta_0 + theta_1) + 0.5 * j2x * cos(theta_0 + theta_1 + theta_2) + 0.5 * j2y * -sin(theta_0 + theta_1 + theta_2));

    LOG(INFO, "%d", (Matrix.Invert((mtx_type *)_invJacobienne, 2)));
    return 0; //(bool);
}

void BrasShower::printPosition()
{
    LOG(INFO, "J0: %f \tJ1: %f \tJ2: %f\n", _jointsPos[0], _jointsPos[1], _jointsPos[2]);
    LOG(INFO, "J0count: %f \tJ1abs: %f \tJ2abs: %f\n", _joints[0]->getPosAbs(), _joints[1]->getPosAbs(), _joints[2]->getPosAbs());
}

void BrasShower::sendDefaultPos()
{
    this->setPos(_defaultPos);
}

//Return array of three flaot representing the angles
float* BrasShower::getPos()
{
//    LOG(INFO, "%f", _jointsPos[0]);
   return _jointsPos;
}

void BrasShower::openGuide()
{
    // LOG(INFO,"open guide");
    _guide.setPos(GUIDE_POS_OPEN);
}

void BrasShower::closeGuide()
{
    // LOG(INFO,"close guide");
    _guide.setPos(GUIDE_POS_CLOSE);
}

void BrasShower::setSpeed(uint8_t speedLimit)
{
    _j0.setSpeed(speedLimit);
}
