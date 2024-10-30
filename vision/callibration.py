import numpy as np

# Known positions in the robot cell (P_robot) in meters
P_robot = np.array([
    [0.25, 0.10, 0.0],
    [0.50, 0.10, 0.0],
    [0.75, 0.10, 0.0],
    [0.25, 0.30, 0.0],
    [0.50, 0.30, 0.0],
    [0.75, 0.30, 0.0],
    [0.25, 0.50, 0.0],
    [0.50, 0.50, 0.0],
    [0.75, 0.50, 0.0]
])

# Camera-detected positions (P_camera)
P_camera = np.array([
    [-0.24237354, 0.23000564, 0.94000006],
    [0.00251378, 0.23318656, 0.95300007],
    [0.24578281, 0.22845545, 0.94000006],
    [-0.2507086, 0.06273072, 0.87700003],
    [0.00373772, 0.06381112, 0.87200004],
    [0.25700793, 0.06208696, 0.86800003],
    [-0.24321598, -0.10910245, 0.75500005],
    [0.00326621, -0.10634409, 0.762],
    [0.25862357, -0.11151678, 0.763]
])

# Compute centroids
C_camera = np.mean(P_camera, axis=0)
C_robot = np.mean(P_robot, axis=0)

# Center the points
P_camera_centered = P_camera - C_camera
P_robot_centered = P_robot - C_robot

# Compute covariance matrix
H = np.dot(P_camera_centered.T, P_robot_centered)

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

print("Transformation Matrix:\n", T)

#test 
point = np.array([-0.24237354, 0.23000564, 0.94000006,1])
point_in_global = T @ point

print("test result")
print(point_in_global)
