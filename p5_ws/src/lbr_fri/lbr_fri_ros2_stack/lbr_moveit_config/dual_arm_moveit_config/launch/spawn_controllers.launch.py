from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription

"""
def generate_launch_description():
    config_file_path = os.path.join(
        get_package_share_directory('dual_arm_config'),
        'config',
        'ros2_controllers.yaml'
    )

    urdf_file_path = os.path.join(
        get_package_share_directory('lbr_description'),
        'urdf',
        'dual_arm',    
        'dual_setup.urdf'
    )

    return LaunchDescription([
        # Start robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[urdf_file_path],
            output='screen',
        ),
    ])
"""

"""
# Start controller_manager
Node(
    package='controller_manager',
    executable='ros2_control_node',
    parameters=[config_file_path],
    output='screen',
),
# Spawning controllers in sequence
TimerAction(
    period=5.0,
    actions=[
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
            output='screen',
        )
    ],
),
RegisterEventHandler(
    OnProcessExit(
        target_action=Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
            output='screen',
        ),
        on_exit=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['right_arm_controller'],
                output='screen',
            )
        ],
    )
),
RegisterEventHandler(
    OnProcessExit(
        target_action=Node(
            package='controller_manager',
            executable='spawner',
            arguments=['right_arm_controller'],
            output='screen',
        ),
        on_exit=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['left_arm_controller'],
                output='screen',
            )
        ],
    )
),
RegisterEventHandler(
    OnProcessExit(
        target_action=Node(
            package='controller_manager',
            executable='spawner',
            arguments=['left_arm_controller'],
            output='screen',
        ),
        on_exit=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['right_gripper_controller'],
                output='screen',
            )
        ],
    )
),
RegisterEventHandler(
    OnProcessExit(
        target_action=Node(
            package='controller_manager',
            executable='spawner',
            arguments=['right_gripper_controller'],
            output='screen',
        ),
        on_exit=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['left_gripper_controller'],
                output='screen',
            )
        ],
    )
),"""
    

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_spawn_controllers_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("dual_arm", package_name="dual_arm_moveit_config").to_moveit_configs()
    return generate_spawn_controllers_launch(moveit_config)
