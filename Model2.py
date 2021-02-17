import matplotlib.pyplot as plt
import numpy as np
import math

# U = (pitch rate, yaw rate, forward speed)


# individual pilot decision for thrust mode
def decision(direction):
    if currentVelocity[direction] <= targetVelocity[direction]:
        B[direction] = False
    else:
        B[direction] = True
    return B


# pitch, yaw and forward displacement in time step dt is converted to cartesian coordinates
def cartesian(dtDisplacement):
    x = math.sin(dtDisplacement[0]) * dtDisplacement[2]
    y = math.sin(dtDisplacement[0]) * math.sin(dtDisplacement[1]) * dtDisplacement[2]
    z = math.cos(dtDisplacement[0]) * dtDisplacement[2]
    return x, y, z


hours = 200     # hours until landing
dt = 0.1        # time step size (hours)
steps = int(hours / dt)     # how many time steps occur
targetVelocity = np.array([0, 0])       # desired pitch and yaw rates
currentVelocity = np.array([-1, -1, 1]) * math.pi/10      # current pitch and yaw rates
dtDisplacement = [0.01, 0.07, 0]        # initial displacement
B = [False, False]      # initial Boolean values
time = [0]      # initial time
timeIn = [0, 0, 0, 0]       # record time in each thruster mode ([(0,0), (0,1), (1,0), (1,1)])
listCurrentVel = [currentVelocity]      # array of velocities
displacement = [dtDisplacement]     # array of displacements
x, y, z = cartesian(dtDisplacement)     # initial cartesian coordinates
xVals = [x]
yVals = [y]
zVals = [z]
decision(0)      # pilots' initial decisions
decision(1)


# thrust1 - B(0,0)
# thrust2 - B(0,1)
# thrust3 - B(1,0)
# thrust4 - B(1,1)
thrust1 = np.array([0.01, 0.02, 0.3])
thrust2 = np.array([0.015, -0.06, 0.2])
thrust3 = np.array([-0.02, 0.01, -0.3])
thrust4 = np.array([-0.02, -0.03, -0.2])

# in order to allow pilots to make a decision a certain time after the pitch or yaw rates go above/below the target
# values, need to have their individual time delays, keep track of when the target value is crossed (change of sign
# in the subtraction) as well as establish a counter to keep track of delay
timeDelay = [12, 9]
pitchRateSign = np.sign(targetVelocity[0] - currentVelocity[0])
yawRateSign = np.sign(targetVelocity[1] - currentVelocity[1])
overshoot = [0, 0]
pitchRateSignChange = False
yawRateSignChange = False

# program runs for 'hours' number of hours in 'steps' number of steps of size 'dt'
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
        B = decision(0)
        pitchRateSignChange = False
        overshoot[0] = 0
    if overshoot[1] == timeDelay[1]:
        B = decision(1)
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

    currentVelocity = currentVelocity + (dt * thrust)
    dtDisplacement = dtDisplacement + (currentVelocity * dt)

    x, y, z = cartesian(dtDisplacement)
    xVals.append(x)
    yVals.append(y)
    zVals.append(z)

    displacement.append(dtDisplacement)
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

plt.show()