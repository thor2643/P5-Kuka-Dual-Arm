import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
 
# Known positions in the robot cell (P_world) in meters 
P_world = np.array([
    [0.25, 0.10, 0.0], 
    [0.25, 0.30, 0.0], 
    [0.25, 0.50, 0.0], 
    [0.50, 0.10, 0.0], 
    [0.50, 0.30, 0.0],
    [0.50, 0.50, 0.0],
    [0.75, 0.10, 0.0],
    [0.75, 0.30, 0.0],
    [0.75, 0.50, 0.0]
])

P_camera = np.array([
    [-0.249, 0.213, 0.95],
    [-0.247, 0.047, 0.853],
    [-0.248, -0.123, 0.751],
    [-0.003, 0.217, 0.965],
    [-0.002, 0.046, 0.854],
    [-0.003, -0.123, 0.757],
    [0.247, 0.215, 0.967],
    [0.249, 0.043, 0.859],
    [0.250, -0.125, 0.754]
])
 
# Compute centroids 
C_camera = np.mean(P_camera, axis=0) 
C_robot = np.mean(P_world, axis=0) 
 
# Center the points 
P_camera_centered = P_camera - C_camera 
P_world_centered = P_world - C_robot 
  
# Compute covariance matrix 
H = np.dot(P_camera_centered.T, P_world_centered) 
 
# Singular Value Decomposition 
U, S, Vt = np.linalg.svd(H) 
 
# Compute rotation 
R = np.dot(Vt.T, U.T) 
 
# Ensure a proper rotation matrix (det(R) should be +1) 
if np.linalg.det(R) < 0: 
    Vt[2, :] *= -1 
    R = np.dot(Vt.T, U.T) 
 
# Compute translation 
t = C_robot - np.dot(R, C_camera) 
 
 
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

 

print("test result") 
print(point_in_global) 
print() 
 

# Calculate the transformed camera points 
P_camera_transformed = np.zeros(P_camera.shape) 
for i in range(P_camera.shape[0]): 
    point = np.append(P_camera[i], 1)  # Add the homogeneous coordinate 
    transformed_point = T @ point     # Apply the transformation 
    P_camera_transformed[i] = transformed_point[:3]  # Extract x, y, z coordinates 


print("Transformed camera points:") 
print(P_camera_transformed) 

# Compute the squared differences 
squared_differences = np.sum(np.square(P_camera_transformed - P_world), axis=1) 


# RMSD 
rmsd = np.sqrt(np.mean(squared_differences)) 
print()
print("RMSD:", rmsd) 
  

#plot the transformed camera points 
fig = plt.figure() 
ax = fig.add_subplot(111, projection='3d') 
ax.scatter(P_world[:,0],P_world[:,1],P_world[:,2],c='r',label='Robot points') 
ax.scatter(P_camera[:,0],P_camera[:,1],P_camera[:,2],c='b',label='Camera points') 
ax.scatter(P_camera_transformed[:,0],P_camera_transformed[:,1],P_camera_transformed[:,2],c='g',label='Camera points transformed') 
ax.set_xlabel('X') 
ax.set_ylabel('Y') 
ax.set_zlabel('Z ') 
plt.legend() 
plt.show() 