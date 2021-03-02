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
def runsimulation():
    hours = 200  # hours until landing
    dt = 0.1  # time step size (hours)
    steps = int(hours / dt)  # how many time steps occur
    targetVelocity = np.array([0, 0])  # desired pitch and yaw rates
    currentVelocity = np.array([0, 0, 0.5])  # * math.pi/10      # current pitch and yaw rates
    currentDisplacement = [0, 0, 0]  # initial displacement in cartesian form
    B = [False, False]
    time = [0]  # initial time
    timeIn = [0, 0, 0, 0]  # record time in each thruster mode ([(0,0), (0,1), (1,0), (1,1)])
    listCurrentVel = [currentVelocity]  # array of velocities
    displacement = [currentDisplacement]  # array of displacements
    xVals = [currentDisplacement[0]]
    yVals = [currentDisplacement[1]]
    zVals = [currentDisplacement[2]]
    decision(0, currentVelocity, targetVelocity, B)  # pilots initial decisions
    decision(1, currentVelocity, targetVelocity, B)

    # in order to allow pilots to make a decision a certain time after the pitch or yaw rates go above/below the target
    # values, need to have their individual time delays, keep track of when the target value is crossed (change of sign
    # in the subtraction) as well as establish a counter to keep track of delay
    timeDelay = [10, 10]
    pitchRateSign = np.sign(targetVelocity[0] - currentVelocity[0])
    yawRateSign = np.sign(targetVelocity[1] - currentVelocity[1])
    overshoot = [0, 0]
    pitchRateSignChange = False
    yawRateSignChange = False

    thrust1 = np.array([1, 4, -1]) / 20
    thrust2 = np.array([3, -6, 10]) / 20
    thrust3 = np.array([-2.5, 1, -2.5]) / 20
    thrust4 = np.array([-1, -1.5, -1.5]) / 20

    for t in np.linspace(dt, hours, steps):
        time.append(t)

        # update info on whether the threshold has been crossed by comparing old iterations data to new
        oldPitchRateSign = pitchRateSign
        oldYawRateSign = yawRateSign
        pitchRateSign = np.sign(targetVelocity[0] - currentVelocity[0])
        yawRateSign = np.sign(targetVelocity[1] - currentVelocity[1])

        # once a threshold is crossed, allow the overshoot counter to begin
        if pitchRateSign != oldPitchRateSign:
            pitchRateSignChange = True
        if yawRateSign != oldYawRateSign:
            yawRateSignChange = True

        if yawRateSignChange:
            overshoot[1] += 1
        if pitchRateSignChange:
            overshoot[0] += 1

        # once the overshoot counter reaches the assigned time delays for each pilot, allow them to make their decisions
        if overshoot[0] == timeDelay[0]:
            B = decision(0, currentVelocity, targetVelocity, B)
            pitchRateSignChange = False
            overshoot[0] = 0
        if overshoot[1] == timeDelay[1]:
            B = decision(1, currentVelocity, targetVelocity, B)
            yawRateSignChange = False
            overshoot[1] = 0

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
        dtDisplacement = currentVelocity * dt
        dtDisplacement = np.array(cartesian(dtDisplacement))
        currentDisplacement = currentDisplacement + dtDisplacement

        xVals.append(currentDisplacement[0])
        yVals.append(currentDisplacement[1])
        zVals.append(currentDisplacement[2])

        displacement.append(currentDisplacement)
        listCurrentVel.append(currentVelocity)

    print(timeIn)
    fig1, ax2d = plt.subplots(1, 2)
    ax2d[0].plot(time, listCurrentVel)
    ax2d[0].legend(("Pitch rate", "Yaw rate", "Forward speed"), loc="upper right")
    ax2d[0].set_title('Velocity')
    ax2d[1].plot(time, displacement)
    ax2d[1].legend(("x", "y", "z"), loc="upper right")
    ax2d[1].set_title('Displacement')

    fig2 = plt.figure()
    ax3d = plt.axes(projection="3d")
    ax3d.plot3D(xVals, zVals, yVals)
    ax3d.set_xlabel('X axis')
    ax3d.set_ylabel('Z axis')
    ax3d.set_zlabel('Y axis')
    with open('TimeDelayData.txt', 'a') as f:
        f.write("\n" + np.array2string(thrust1, formatter={'float_kind': lambda x: "%.3f" % x}))
        f.write(np.array2string(thrust2, formatter={'float_kind': lambda x: "%.3f" % x}))
        f.write(np.array2string(thrust3, formatter={'float_kind': lambda x: "%.3f" % x}))
        f.write(np.array2string(thrust4, formatter={'float_kind': lambda x: "%.3f" % x}))
        f.write("\nendpoint = " + str(displacement[-1]) + "\nnumber of each choices were:" + str(timeIn))
    plt.show()

runsimulation()
