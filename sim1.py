import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

time=500

time_steps=np.linspace(1, time, num=time)
starting_position=np.array([-2,5,0])
current_position=starting_position

#boosters
Bzero_one=np.array([3/20,-6/20,10/20])
Bone_one=np.array([-2/10,-3/10,-3/10])
Bzero_zero=np.array([0,4/20,-1/20])
Bone_zero=np.array([-5/10,2/10,-5/10])

target=[0,0]

data=[]

for step in time_steps:
    #pitch man u
    if step%9==0:
        if current_position[0]>target[0]:
            if current_position[1]>target[1]:
                current_position=current_position+Bone_one
                data.append(current_position)
            elif current_position[1]<target[1]:
                current_position=current_position+Bone_zero
                data.append(current_position)
            else:
                print('u on target')

        if current_position[0]<target[0]:
            if current_position[1]>target[1]:
                current_position=current_position+Bzero_one
                data.append(current_position)
            elif current_position[1]<target[1]:
                current_position=current_position+Bzero_zero
                data.append(current_position)
            else:
                print('u on target')


    #yaw man v
    elif step%10==0:
        if current_position[1]>target[1]:
            if current_position[0]>target[0]:
                current_position=current_position+Bone_one
                data.append(current_position)
            elif current_position[0]<target[0]:
                current_position=current_position+Bzero_one
                data.append(current_position)
            else:
                print('u on target')

        if current_position[1]<target[1]:
            if current_position[0]>target[0]:
                current_position=current_position+Bone_zero
                data.append(current_position)
            elif current_position[0]<target[0]:
                current_position=current_position+Bzero_zero
                data.append(current_position)
            else:
                print('u on target')    
    else:
        pass


print(data)
u=[]
v=[]
w=[]
for item in data:
    u.append(item[0])
    v.append(item[1])
    w.append(item[2])


fig = plt.figure()
#ax = fig.add_subplot(111, projection = '3d')

#ax.plot(v,u,w, marker = 'x')

#ax.scatter(*points.T[0], color = 'red')


plt.plot(data)
#plt.plot(v)
plt.grid()
plt.show()