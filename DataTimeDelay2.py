from TimeDelayModel import decision, cartesian, runsimulation
import matplotlib.pyplot as plt
import numpy as np
import math

dt = 0.01       # time step used in model
finalSpeeds = []
thrusterTimes = []

timeValues = range(100, 150)

for i in timeValues:
    displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals = runsimulation(i, i, dt)
    finalSpeeds.append(listCurrentVel[-1][2])
    thrusterTimes.append(timeIn)


plt.scatter(timeValues, finalSpeeds)
print(thrusterTimes)
plt.show()
