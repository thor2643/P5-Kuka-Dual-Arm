import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        # Camera Package - Service (We need to make it spin by default, if not done already)
        Node(
            package='object_detector',
            executable='detector_service',
            prefix=['gnome-terminal -- bash -c "ros2 run object_detector detector_service; exec bash"']
        ),
        
        # 3F Gripper - Service
        Node(
            package='robotiq_3f_gripper_ros2_control',
            executable='gripper_control_service_server'
        ),
        
        # 2F Gripper - Service
        Node(
            package='robotiq_2f_85_control',
            executable='gripper_control_service_node'
        ),

        # Janise
        Node(
            package='janise',
            executable='omni_client',
            prefix=['gnome-terminal -- bash -c "ros2 run janise omni_client; exec bash"']
        ),

        # Moveit Coords - Set_moveit_coords.launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('set_moveit_coords'),
                    'launch',
                    'set_moveit_coords.launch.py'
                )
            )
        ),
        
        # Realsense
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('realsense2_camera'),
                    'launch',
                    'rs_launch.py'
                )
            )
        ),

        # Dual Arm - Demo Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('dual_arm_moveit_config'),
                    'launch',
                    'demo.launch.py'
                )
            )
        ),
    ])
