import matplotlib.pyplot as plt
import numpy as np
import math

# U = (pitch rate, yaw rate, forward speed)


def decision(direction, freq):
    if decisionCounter % freq == 0:
        if CO[direction] <= FO[direction]:
            B[direction] = False
        else:
            B[direction] = True
    return B


hours = 200     # hours until landing
dt = 0.1        # time step size (hours)
yawFreq = 10       # after yawFreq time steps, change yaw rate
pitchFreq = 10       # after pitchFreq time steps, change pitch rate
steps = int(hours / dt)
FO = np.array([0, 0])
CO = np.array([0, 0, 1]) * math.pi/10

# thrust1 - B(0,0)
# thrust2 - B(0,1)
# thrust3 - B(1,0)
# thrust4 - B(1,1)
thrust1 = np.array([0.1, 0.2, 0.05])
thrust2 = np.array([0.15, -0.6, 0.3])
thrust3 = np.array([-0.2, 0.1, -0.2])
thrust4 = np.array([-0.2, -0.3, -0.2])

timeIn = [0, 0, 0, 0]

listCO = [CO]
disp = [0.1, 0.07, 0]
displacement = [disp]
decisionCounter = 0
B = [False, False]
time = [0]

decision(0, pitchFreq)
decision(1, yawFreq)

for t in np.linspace(dt, hours, steps):
    time.append(t)
    decisionCounter += 1

    decision(0, pitchFreq)

    decision(1, yawFreq)

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

    CO = CO + (dt * thrust)
    disp = disp + (CO * dt)
    displacement.append(disp)
    listCO.append(CO)

print(timeIn)

fig, axs = plt.subplots(1, 2)
axs[0].plot(time, listCO)
axs[0].legend(("Pitch rate", "Yaw rate", "Forward speed"), loc="upper right")
axs[0].set_title('Velocity')
axs[1].plot(time, displacement)
axs[1].legend(("Pitch", "Yaw", "Forward displacement"), loc="upper right")
axs[1].set_title('Displacement')


plt.show()
