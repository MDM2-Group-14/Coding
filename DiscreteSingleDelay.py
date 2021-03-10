import matplotlib.pyplot as plt
import numpy as np
import math
from random import randint

# U = (pitch rate, yaw rate, forward speed)


# individual pilot decision for thrust mode
def decision(direction, freq, decisionCounter, currentVelocity, targetVelocity, B):
    decisionMade = False
    if decisionCounter % freq == 0:
        if currentVelocity[direction] <= targetVelocity[direction]:
            B[direction] = False
        else:
            B[direction] = True
        decisionMade = True
    return B, decisionMade


# pitch, yaw and forward displacement in time step dt is converted to cartesian coordinates
def cartesian(dtDisplacement):
    z = math.sqrt(dtDisplacement[2]**2 / (math.tan(dtDisplacement[1])**2 + math.tan(dtDisplacement[0])**2 +1))
    x = math.tan(dtDisplacement[1])*z
    y = math.tan(dtDisplacement[0])*z
    return x, y, z


# program runs for 'hours' number of hours in 'steps' number of steps of size 'dt'
def runsimulation(yawFreq, pitchFreq, dt):
    hours = 200  # hours until landing
    dt = dt  # time step size (hours)
    steps = int(hours / dt)  # how many time steps occur

    targetVelocity = np.array([0, 0])  # desired pitch and yaw rates
    currentVelocity = np.array([0, 0, 0.5])  # * math.pi/10      # current pitch and yaw rates
    currentDisplacement = [0, 0, 0]  # initial displacement in cartesian form
    currentAngle = [0, 0, 0]

    B = [False, False]
    decisionCounter = -1
    time = [0]  # initial time
    timeIn = np.array([0, 0, 0, 0])  # record time in each thruster mode ([(0,0), (0,1), (1,0), (1,1)])

    listCurrentVel = [currentVelocity]  # array of velocities
    displacement = [currentDisplacement]  # array of displacements
    angles = [currentAngle] # array of angles
    xVals = [currentDisplacement[0]]
    yVals = [currentDisplacement[1]]
    zVals = [currentDisplacement[2]]

    thrust1 = np.array([0.003, 0.003, 0.06])        # B(0,0)
    thrust2 = np.array([0.004, -0.006, 0.02])       # B(0,1)
    thrust3 = np.array([-0.003, 0.004, -0.03])      # B(1,0)
    thrust4 = np.array([-0.005, -0.003, -0.02])     # B(1,1)

    thrust = [0, 0, 0]

    for t in np.linspace(dt, hours, steps):
        time.append(t)
        decisionCounter += 1

        # decision function determines when pilots make decision
        B, decisionMade = decision(0, pitchFreq, decisionCounter, currentVelocity, targetVelocity, B)
        B, decisionMade = decision(1, yawFreq, decisionCounter, currentVelocity, targetVelocity, B)

        if decisionMade == True:
            thrustDelayCounter = 1
            lastThrust = thrust

        if B == [False, False]:
            thrust = thrust1
            timeIn[0] += 1
        elif B == [False, True]:
            thrust = thrust2
            timeIn[1] += 1
        elif B == [True, False]:
            thrust = thrust3
            timeIn[2] += 1
        else:
            thrust = thrust4
            timeIn[3] += 1

        if thrustDelayCounter < 60:
            thrust = ((math.exp(0.05*thrustDelayCounter - 3))*(thrust-lastThrust)) + lastThrust
            thrustDelayCounter += 1
            currentVelocity = currentVelocity + (dt * thrust)  # update rocket's velocity
        if thrustDelayCounter >= 60:
            thrust = 0

        dtAngle = currentVelocity * dt
        currentAngle = currentAngle + dtAngle
        dtDisplacement = np.array(cartesian(dtAngle))
        currentDisplacement = currentDisplacement + dtDisplacement

        xVals.append(currentDisplacement[0])
        yVals.append(currentDisplacement[1])
        zVals.append(currentDisplacement[2])

        displacement.append(currentDisplacement)
        angles.append(currentAngle)
        listCurrentVel.append(currentVelocity)
    return displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals

