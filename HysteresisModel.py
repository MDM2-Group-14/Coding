import matplotlib.pyplot as plt
import numpy as np
import math
from random import randint

# U = (pitch rate, yaw rate, forward speed)


# individual pilot decision for thrust mode
def decision(direction, currentVelocity, targetVelocity, B):
    if currentVelocity[direction] <= targetVelocity[direction]:
        B[direction] = False
    else:
        B[direction] = True
    return B


# pitch, yaw and forward displacement in time step dt is converted to cartesian coordinates
def cartesian(dtDisplacement):
    z = math.sqrt(dtDisplacement[2]**2 / (math.tan(dtDisplacement[1])**2 + math.tan(dtDisplacement[0])**2 +1))
    x = math.tan(dtDisplacement[1])*z
    y = math.tan(dtDisplacement[0])*z
    return x, y, z


# program runs for 'hours' number of hours in 'steps' number of steps of size 'dt'
def runsimulation(pitchOvershoot, yawOvershoot, dt):
    hours = 200  # hours until landing
    dt = dt  # time step size (hours)
    steps = int(hours / dt)  # how many time steps occur
    targetVelocity = np.array([0, 0])  # desired pitch and yaw rates
    currentVelocity = np.array([0, 0, 0.5])      # current pitch and yaw rates
    currentDisplacement = [0, 0, 0]  # initial displacement in cartesian form
    currentAngle = [0, 0, 0]

    B = [False, False]
    time = [0]  # initial time
    timeIn = [0, 0, 0, 0]  # record time in each thruster mode ([(0,0), (0,1), (1,0), (1,1)])

    listCurrentVel = [currentVelocity]  # array of velocities
    displacement = [currentDisplacement]  # array of displacements
    angles = [currentAngle]  # array of angles
    xVals = [currentDisplacement[0]]
    yVals = [currentDisplacement[1]]
    zVals = [currentDisplacement[2]]

    decision(0, currentVelocity, targetVelocity, B)  # pilots initial decisions
    decision(1, currentVelocity, targetVelocity, B)

    # angular overshoot around target pitch and yaw rates at which pilots make decisions
    overshoot = [pitchOvershoot, yawOvershoot]

    thrust1 = np.array([0.001, 0.002, 0.006])
    thrust2 = np.array([0.0015, -0.006, 0.002])
    thrust3 = np.array([-0.002, 0.001, -0.003])
    thrust4 = np.array([-0.002, -0.003, -0.002])

    for t in np.linspace(dt, hours, steps):
        time.append(t)

        if abs(currentVelocity[0] - targetVelocity[0]) >= overshoot[0]:
            B = decision(0, currentVelocity, targetVelocity, B)

        if abs(currentVelocity[1] - targetVelocity[1]) >= overshoot[1]:
            B = decision(1, currentVelocity, targetVelocity, B)

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

        currentVelocity = currentVelocity + (dt * thrust)  # update rocket's velocity
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

    return (displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals)