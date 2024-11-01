import numpy as np


pose = [0.00505068, 0.06414559, 0.851, 0.0, 0.0, 0.0]

angle_around_x = 180-33
T_world_cam = np.array([
                [1, 0, 0, 0.487],  # Example values, replace with actual transformation values
                [0, np.cos(np.pi/180*angle_around_x), -np.sin(np.pi/180*angle_around_x), 0.77],
                [0, np.sin(np.pi/180*angle_around_x), np.cos(np.pi/180*angle_around_x), 0.62],
                [0, 0, 0, 1]
            ])

# Found in CAD model
T_world_moveit = np.array([
                [1, 0, 0, 0.035],  # Example values, replace with actual transformation values
                [0, 1, 0, 0.034],
                [0, 0, 1, 0.809],
                [0, 0, 0, 1]
            ])

# Extract the position from the pose and append 1 to make it a 4D vector
pos_cam = pose[:3]
pos_cam.append(1)

# Transform the position from camera to world coordinates
pos_world = np.dot(T_world_cam, pos_cam)
pos_moveit = np.dot(T_world_moveit, pos_world)

print(pos_moveit)
