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
            prefix=['gnome-terminal --']
        ),

        # Janise
        Node(
            package='janise',
            executable='client_omni',
            prefix=['gnome-terminal --']
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

        # LBR - Real.launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('lbr_bringup'),
                    'launch',
                    'real.launch.py'
                )
            )
        ),

        # Uncomment the following block if you want to open set_moveit_coords.launch.py in a new terminal
        # ExecuteProcess(
        #     cmd=[
        #         'gnome-terminal', '--', 'bash', '-c', 
        #         'ros2 launch set_moveit_coords set_moveit_coords.launch.py; exec bash'
        #     ],
        #     output='screen'
        # ),
    ])