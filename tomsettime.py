import matplotlib.pyplot as plt
import numpy as np
import math
from random import randint


# U = (pitch rate, yaw rate, forward speed)


# individual pilot decision for thrust mode
def decision(direction, freq, decisionCounter, currentVelocity, targetVelocity, B):
    if decisionCounter % freq == 0:
        if currentVelocity[direction] <= targetVelocity[direction]:
            B[direction] = False
        else:
            B[direction] = True
    return B


# pitch, yaw and forward displacement in time step dt is converted to cartesian coordinates
def cartesian(dtDisplacement):
    z = math.sqrt(dtDisplacement[2] ** 2 / (math.tan(dtDisplacement[1]) ** 2 + math.tan(dtDisplacement[0]) ** 2 + 1))
    x = math.tan(dtDisplacement[1]) * z
    y = math.tan(dtDisplacement[0]) * z
    return x, y, z


# program runs for 'hours' number of hours in 'steps' number of steps of size 'dt'
def runsimulation():
    hours = 200  # hours until landing
    dt = 0.1  # time step size (hours)
    yawFreq = 10  # after yawFreq time steps, change yaw rate
    pitchFreq = 9  # after pitchFreq time steps, change pitch rate
    steps = int(hours / dt)  # how many time steps occur
    targetVelocity = np.array([0, 0])  # desired pitch and yaw rates
    currentVelocity = np.array([0, 0, 0.5])  # * math.pi/10      # current pitch and yaw rates
    currentDisplacement = [0, 0, 0]  # initial displacement in cartesian form
    B = [False, False]
    decisionCounter = 0
    time = [0]  # initial time
    timeIn = [0, 0, 0, 0]  # record time in each thruster mode ([(0,0), (0,1), (1,0), (1,1)])
    listCurrentVel = [currentVelocity]  # array of velocities
    displacement = [currentDisplacement]  # array of displacements
    xVals = [currentDisplacement[0]]
    yVals = [currentDisplacement[1]]
    zVals = [currentDisplacement[2]]
    decision(0, pitchFreq, decisionCounter, currentVelocity, targetVelocity, B)  # pilots initial decisions
    decision(1, yawFreq, decisionCounter, currentVelocity, targetVelocity, B)

    thrust1 = np.array([1, 4, -1]) +10 / 20
    thrust2 = np.array([3, -6, 10])+10  / 20
    thrust3 = np.array([-2.5, 1, -2.5])+10 / 20
    thrust4 = np.array([-1, -1.5, -1.5])+10 / 20

    for t in np.linspace(dt, hours, steps):
        time.append(t)
        decisionCounter += 1
        # decision function determines when pilots make decision
        decision(0, pitchFreq, decisionCounter, currentVelocity, targetVelocity, B)
        decision(1, yawFreq, decisionCounter, currentVelocity, targetVelocity, B)

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
        dtDisplacement2 = np.array(cartesian(dtDisplacement))
        dtDisplacement = np.array(cartesian(dtDisplacement))
        print(dtDisplacement, dtDisplacement2)
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
    with open('SetTimeDataFile.txt', 'a') as f:
        f.write("\n" + np.array2string(thrust1, formatter={'float_kind': lambda x: "%.2f" % x}))
        f.write(np.array2string(thrust2, formatter={'float_kind': lambda x: "%.2f" % x}))
        f.write(np.array2string(thrust3, formatter={'float_kind': lambda x: "%.2f" % x}))
        f.write(np.array2string(thrust4, formatter={'float_kind': lambda x: "%.2f" % x}))
        f.write("\nendpoint = " + str(displacement[-1]) + "\nnumber of each choices were:" + str(timeIn))

    plt.show()


runsimulation()