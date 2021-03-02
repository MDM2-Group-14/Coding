from TimeDelayModel import decision, cartesian, runsimulation
import matplotlib.pyplot as plt
import numpy as np
import math

dt = 0.1       # time step used in model
velocitiesData = []
anglesData = []
xValsData = []
yValsData = []
zValsData = []
forwardSpeeds = []
thrusterTimes = []
pitchAngleRates = []
yawAngles = []


for i in range(7, 12):
    displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals = runsimulation(i, i, dt)
    thrusterTimes.append(timeIn)
    for j in range(0, len(time)):
        forwardSpeeds.append(listCurrentVel[j][2])
        pitchAngleRates.append(listCurrentVel[j][0])

print(thrusterTimes)

tlen = len(time)

fig1, ax2d = plt.subplots(1, 2)
for k in range(0, 5):
    forwardSpeedsForEachTime = []
    pitchAngleRatesForEachTime = []
    for l in range(k*tlen, (k+1)*tlen):
        forwardSpeedsForEachTime.append(forwardSpeeds[l])
        pitchAngleRatesForEachTime.append(pitchAngleRates[l])
    ax2d[0].plot(time, forwardSpeedsForEachTime)
    ax2d[1].plot(time, pitchAngleRatesForEachTime)

ax2d[0].legend(("7", "8", "9", "10", "11"), loc="upper left")
ax2d[0].set_title('Forward Speeds')

ax2d[1].legend(("7", "8", "9", "10", "11"), loc="upper right")
ax2d[1].set_title('Pitch Angles')


plt.show()
