from DiscreteModel import decision, cartesian, runsimulation
import matplotlib.pyplot as plt
import numpy as np
import math

dt = 0.01       # time step used in model
finalSpeeds = []
thrusterTimes = []

timeValues = range(70, 140)

for i in timeValues:
    displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals = runsimulation(i, i, dt)
    finalSpeeds.append(listCurrentVel[-1][2])
    thrusterTimes.append(timeIn)

plt.figure(1)
plt.scatter(timeValues, finalSpeeds)

plt.figure(2)
plt.plot(timeValues, finalSpeeds)

print(thrusterTimes)

plt.show()
