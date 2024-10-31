import numpy as np

T_cam_world_1 = np.array([
                [-1, 0, 0, -0.487],  # Example values, replace with actual transformation values
                [0, 1, 0, 0.336],
                [0, 0, -1, 1.011],
                [0, 0, 0, 1]
            ])

angle_around_x = 34
T_cam_world_2 = np.array([
                [1, 0, 0, 0],  # Example values, replace with actual transformation values
                [0, np.cos(angle_around_x), -np.sin(angle_around_x), 0],
                [0, np.sin(angle_around_x), np.cos(angle_around_x), 0],
                [0, 0, 0, 1]
            ])

T_total = np.dot(T_cam_world_1, T_cam_world_2)
print(T_total)

test_vector = np.array([0.008, 0.214, 0.893, 1])
world_vector = np.dot(T_total, test_vector)

print(f"\nWorld_vector: {world_vector}")