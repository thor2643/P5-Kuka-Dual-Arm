from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

from typing import List
from launch import LaunchContext, LaunchDescription, LaunchDescriptionEntity
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration

#from lbr_bringup.description import LBRDescriptionMixin


def generate_launch_description():
    # Set MoveIt configuration
    moveit_config = MoveItConfigsBuilder("iiwa7", package_name="moveit2_launch").to_moveit_configs()

    # Define hello_moveit node
    send_cudes_node = Node(
        package="send_cudes",
        executable="send_cudes",
        output="screen",
        parameters=[
            moveit_config.robot_description,  # Load URDF
            moveit_config.robot_description_semantic,  # Load SRDF
            moveit_config.robot_description_kinematics,  # Load kinematics.yaml
        ],
    )

    return LaunchDescription([send_cudes_node]) 
