import numpy as np

# Known positions in the robot cell (P_world) in meters
"""
P_world = np.array([
    [0.15, 0.50, 0.0],
    [0.15, 0.30, 0.0],
    [0.15, 0.10, 0.0],
    [0.25, 0.10, 0.0], 
    [0.25, 0.30, 0.0], 
    [0.25, 0.50, 0.0], 
    [0.50, 0.30, 0.0], 
    [0.50, 0.50, 0.0] 
])

P_robot = np.array([
    [0.116, 0.471, 0.810],
    [0.117, 0.270, 0.811],
    [0.118, 0.068, 0.811],
    [0.218, 0.069, 0.811],
    [0.220, 0.272, 0.810],
    [0.219, 0.474, 0.810],
    [0.469, 0.273, 0.811],
    [0.466, 0.473, 0.811]
])

"""

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

P_robot = np.array([
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
C_robot = np.mean(P_robot, axis=0)
C_world = np.mean(P_world, axis=0)

# Center the points
P_robot_centered = P_robot - C_robot
P_world_centered = P_world - C_world

# Compute covariance matrix
H = np.dot(P_robot_centered.T, P_world_centered)

# Singular Value Decomposition
U, S, Vt = np.linalg.svd(H)

# Compute rotation
R = np.dot(Vt.T, U.T)

# Ensure a proper rotation matrix (det(R) should be +1)
if np.linalg.det(R) < 0:
    Vt[2, :] *= -1
    R = np.dot(Vt.T, U.T)

# Compute translation
t = C_world - np.dot(R, C_robot)

# Construct transformation matrix
T = np.eye(4)
T[:3, :3] = R
T[:3, 3] = t

print("Transformation Matrix:\n", T)

#test 
point = np.array([-0.24237354, 0.23000564, 0.94000006,1])
point_in_global = T @ point

print("test result")
print(point_in_global)


#calculate the error for each value x,y,z compared to the real value in P_robot
Error = np.zeros((len(P_robot),3))
for i in range(len(P_robot)):
    point = np.array([P_robot[i][0],P_robot[i][1],P_robot[i][2],1])
    point_in_global = T @ point
    Error[i] = point_in_global[:3] - P_world[i]

print("Error for each point")
print(Error)

#calculate the mean error for each value x,y,z
mean_error = np.mean(Error,axis=0)
print("Mean error for each value x,y,z")
print(mean_error)


