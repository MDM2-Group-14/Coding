from Model2 import decision, cartesian, runsimulation
import matplotlib.pyplot as plt
import numpy as np
import math

velocitiesData = []
anglesData = []
xValsData = []
yValsData = []
zValsData = []
forwardSpeeds = []
thrusterTimes = []
pitchAngles = []
yawAngles = []


for i in range(7, 12):
    displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals = runsimulation(i, 10)
    thrusterTimes.append(timeIn)
    for j in range(0, len(time)):
        forwardSpeeds.append(listCurrentVel[j][2])
        pitchAngles.append(angles[j][0])

print(thrusterTimes)

tlen = len(time)

fig1, ax2d = plt.subplots(1, 2)
for k in range(0, 5):
    forwardSpeedsForEachTime = []
    pitchAnglesForEachTime = []
    for l in range(k*tlen, (k+1)*tlen):
        forwardSpeedsForEachTime.append(forwardSpeeds[l])
        pitchAnglesForEachTime.append(pitchAngles[l])
    ax2d[0].plot(time, forwardSpeedsForEachTime)
    ax2d[1].plot(time, pitchAnglesForEachTime)

ax2d[0].legend(("7", "8", "9", "10", "11"), loc="upper left")
ax2d[0].set_title('Forward Speeds')

ax2d[1].legend(("7", "8", "9", "10", "11"), loc="upper right")
ax2d[1].set_title('Pitch Angles')


plt.show()
