import numpy as np


def transformation_matrix(rpy, xyz):
    roll, pitch, yaw = rpy
    x, y, z = xyz

    # Rotation matrices around x, y, and z axes
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    
    # Combined rotation matrix
    R = Rz @ Ry @ Rx
    
    # Transformation matrix
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [x, y, z]
    
    return T

def forward_kinematics_left(joint_angles):
    # Define the fixed transformation from world to left_link_0
    T_mount_left = transformation_matrix([-0.785398163, 0, -1.57079633], [0.711114, 0.756691, 1.037203])
    
    # Define the transformation matrices for each joint
    T_left_A1 = transformation_matrix([0, 0, 0], [0.0, 0.0, 0.1475])
    T_left_A2 = transformation_matrix([0, 0, 0], [0.0, -0.0105, 0.1925])
    T_left_A3 = transformation_matrix([0, 0, 0], [0.0, 0.0105, 0.2075])
    T_left_A4 = transformation_matrix([0, 0, 0], [0.0, 0.0105, 0.1925])
    T_left_A5 = transformation_matrix([0, 0, 0], [0.0, -0.0105, 0.2075])
    T_left_A6 = transformation_matrix([0, 0, 0], [0.0, -0.0707, 0.1925])
    T_left_A7 = transformation_matrix([0, 0, 0], [0.0, 0.0707, 0.091])
    T_left_joint_ee = transformation_matrix([0, 0, 0], [0, 0, 0.035])
    
    # Define the rotation matrices for each joint angle
    R_left_A1 = transformation_matrix([0, 0, joint_angles[0]], [0, 0, 0])
    R_left_A2 = transformation_matrix([0, joint_angles[1], 0], [0, 0, 0])
    R_left_A3 = transformation_matrix([0, 0, joint_angles[2]], [0, 0, 0])
    R_left_A4 = transformation_matrix([0, -joint_angles[3], 0], [0, 0, 0])
    R_left_A5 = transformation_matrix([0, 0, joint_angles[4]], [0, 0, 0])
    R_left_A6 = transformation_matrix([0, joint_angles[5], 0], [0, 0, 0])
    R_left_A7 = transformation_matrix([0, 0, joint_angles[6]], [0, 0, 0])
    
    # Compute the final transformation matrix
    T = T_mount_left @ T_left_A1 @ R_left_A1 @ T_left_A2 @ R_left_A2 @ T_left_A3 @ R_left_A3 @ T_left_A4 @ R_left_A4 @ T_left_A5 @ R_left_A5 @ T_left_A6 @ R_left_A6 @ T_left_A7 @ R_left_A7 @ T_left_joint_ee
    
    return T

def forward_kinematics_right(joint_angles):
    # Define the fixed transformation from world to right_link_0
    T_mount_right = transformation_matrix([0.785398163, 0, -1.57079633], [0.268524, 0.756691, 1.037203])
    
    # Define the transformation matrices for each joint
    T_right_A1 = transformation_matrix([0, 0, 0], [0.0, 0.0, 0.1475])
    T_right_A2 = transformation_matrix([0, 0, 0], [0.0, -0.0105, 0.1925])
    T_right_A3 = transformation_matrix([0, 0, 0], [0.0, 0.0105, 0.2075])
    T_right_A4 = transformation_matrix([0, 0, 0], [0.0, 0.0105, 0.1925])
    T_right_A5 = transformation_matrix([0, 0, 0], [0.0, -0.0105, 0.2075])
    T_right_A6 = transformation_matrix([0, 0, 0], [0.0, -0.0707, 0.1925])
    T_right_A7 = transformation_matrix([0, 0, 0], [0.0, 0.0707, 0.091])
    T_right_joint_ee = transformation_matrix([0, 0, 0], [0, 0, 0.035])
    
    # Define the rotation matrices for each joint angle
    R_right_A1 = transformation_matrix([0, 0, joint_angles[0]], [0, 0, 0])
    R_right_A2 = transformation_matrix([0, joint_angles[1], 0], [0, 0, 0])
    R_right_A3 = transformation_matrix([0, 0, joint_angles[2]], [0, 0, 0])
    R_right_A4 = transformation_matrix([0, -joint_angles[3], 0], [0, 0, 0])
    R_right_A5 = transformation_matrix([0, 0, joint_angles[4]], [0, 0, 0])
    R_right_A6 = transformation_matrix([0, joint_angles[5], 0], [0, 0, 0])
    R_right_A7 = transformation_matrix([0, 0, joint_angles[6]], [0, 0, 0])
    
    # Compute the final transformation matrix
    T = T_mount_right @ T_right_A1 @ R_right_A1 @ T_right_A2 @ R_right_A2 @ T_right_A3 @ R_right_A3 @ T_right_A4 @ R_right_A4 @ T_right_A5 @ R_right_A5 @ T_right_A6 @ R_right_A6 @ T_right_A7 @ R_right_A7 @ T_right_joint_ee
    
    return T

# Example usage with some joint angles
joint_angles_degrees = [-22, 8, -153, 62, -165, 95, 10]
joint_angles_rads = [angle * np.pi/180 for angle in joint_angles_degrees]
pose = forward_kinematics_left(joint_angles_rads)
print(pose)

joint_angles_degrees = [61, 70, -58, -55, 11, 93, -71]
joint_angles_rads = [angle * np.pi/180 for angle in joint_angles_degrees]
pose = forward_kinematics_right(joint_angles_rads)
print(pose)