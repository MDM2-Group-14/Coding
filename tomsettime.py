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
    x = math.sin(dtDisplacement[0]) * math.cos(dtDisplacement[1]) * dtDisplacement[2]
    y = math.sin(dtDisplacement[0]) * math.sin(dtDisplacement[1]) * dtDisplacement[2]
    z = math.cos(dtDisplacement[0]) * dtDisplacement[2]
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
    currentDisplacement = [0.00, 0.00, 0]  # initial displacement in cartesian form
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

    thrust1 = np.array([randint(1, 10), randint(1, 10), randint(-1, 4)]) / 20  # thrust1 - B(0,0)
    thrust2 = np.array([randint(1, 10), -randint(1, 10), randint(-1, 4)]) / 20  # thrust2 - B(0,1)
    thrust3 = np.array([-randint(1, 10), randint(1, 10), randint(-1, 4)]) / 20  # thrust3 - B(1,0)
    thrust4 = np.array([-randint(1, 10), -randint(1, 10), randint(-1, 4)]) / 20  # thrust4 - B(1,1)

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
    ax2d[1].legend(("Pitch", "Yaw", "Forward displacement"), loc="upper right")
    ax2d[1].set_title('Displacement')

    fig2 = plt.figure()
    ax3d = plt.axes(projection="3d")
    ax3d.plot3D(xVals, zVals, yVals)
    ax3d.set_xlabel('X axis')
    ax3d.set_ylabel('Z axis')
    ax3d.set_zlabel('Y axis')

    with open('SetTimeDataFile.txt', 'a') as f:
        f.write("\n" + np.array2string(thrust1, formatter={'float_kind':lambda x: "%.2f" % x}))
        f.write(np.array2string(thrust2, formatter={'float_kind':lambda x: "%.2f" % x}))
        f.write(np.array2string(thrust3, formatter={'float_kind':lambda x: "%.2f" % x}))
        f.write(np.array2string(thrust4, formatter={'float_kind':lambda x: "%.2f" % x}))
        f.write("\nendpoint = " + str(displacement[-1]) + "\nnumber of each choices were:" + str(timeIn))
    plt.show()


