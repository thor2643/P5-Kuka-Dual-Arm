import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
 
# Known positions in the robot frame  (Left)
P_robot = np.array([
    [0.567509, 0.0706314, 0.822243],
    [0.71981, 0.071357, 0.82235],
    [0.86943, 0.072108, 0.82269],
    [0.56797, 0.27397, 0.82143],
    [0.71783, 0.27654, 0.821],
    [0.86865, 0.27794, 0.82178],
    [0.56499, 0.46881, 0.8207],
    [0.7152, 0.47224, 0.81968],
    [0.86677,0.47542, 0.81946]
])



P_world = np.array([
    [0.6, 0.1, 0.01], 
    [0.75, 0.1, 0.01],
    [0.9, 0.1, 0.01],
    [0.6, 0.3, 0.01],
    [0.75, 0.3, 0.01],
    [0.9, 0.3, 0.01],
    [0.6, 0.5, 0.01],
    [0.75, 0.5, 0.01],
    [0.9, 0.5, 0.01]
    
])
 
# Compute centroids 
C_world = np.mean(P_world, axis=0) 
C_robot = np.mean(P_robot, axis=0) 
 
# Center the points 
P_world_centered = P_world - C_world 
P_robot_centered = P_robot - C_robot 
  
# Compute covariance matrix 
H = np.dot(P_world_centered.T, P_robot_centered) 
 
# Singular Value Decomposition 
U, S, Vt = np.linalg.svd(H) 
 
# Compute rotation 
R = np.dot(Vt.T, U.T) 
 
# Ensure a proper rotation matrix (det(R) should be +1) 
if np.linalg.det(R) < 0: 
    Vt[2, :] *= -1 
    R = np.dot(Vt.T, U.T) 
 
# Compute translation 
t = C_robot - np.dot(R, C_world) 
 
 
# Construct transformation matrix 
T = np.eye(4) 
T[:3, :3] = R 
T[:3, 3] = t 
 
print("Transformation matrix:") 
print(T) 
print() 
 

#test  
point = np.array([-0.24237354, 0.23000564, 0.94000006,1]) 
point_in_global = T @ point 

 

#print("test result") 
#print(point_in_global) 
#print() 
 

# Calculate the transformed world points 
P_world_transformed = np.zeros(P_world.shape) 
for i in range(P_world.shape[0]): 
    point = np.append(P_world[i], 1)  # Add the homogeneous coordinate 
    transformed_point = T @ point     # Apply the transformation 
    P_world_transformed[i] = transformed_point[:3]  # Extract x, y, z coordinates 


print("Transformed world points:") 
print(P_world_transformed) 

# Compute the squared differences 
squared_differences = np.sum(np.square(P_world_transformed - P_robot), axis=1) 


# RMSD 
rmsd = np.sqrt(np.mean(squared_differences)) 
print()
print("RMSD:", rmsd) 
  

#plot the transformed world points 
fig = plt.figure() 
ax = fig.add_subplot(111, projection='3d') 
ax.scatter(P_robot[:,0],P_robot[:,1],P_robot[:,2],c='r',label='Robot points') 
ax.scatter(P_world[:,0],P_world[:,1],P_world[:,2],c='b',label='World points') 
ax.scatter(P_world_transformed[:,0],P_world_transformed[:,1],P_world_transformed[:,2],c='g',label='Points transformed') 
ax.set_xlabel('X') 
ax.set_ylabel('Y') 
ax.set_zlabel('Z ') 
plt.legend() 
plt.show() 