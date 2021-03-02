from HysteresisModel import decision, cartesian, runsimulation
import matplotlib.pyplot as plt
import numpy as np
import math

dt = 0.01       # time step used in model
finalSpeeds = []

timeValues = range(1, 50)

for i in timeValues:
    displacement, angles, listCurrentVel, time, timeIn, xVals, yVals, zVals = runsimulation(i/1000, i/1000, dt)
    finalSpeeds.append(listCurrentVel[-1][2])

plt.scatter(timeValues, finalSpeeds)

plt.show()
