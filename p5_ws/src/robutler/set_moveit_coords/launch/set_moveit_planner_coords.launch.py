from typing import List

from launch import LaunchContext, LaunchDescription, LaunchDescriptionEntity
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_mixins.lbr_bringup import LBRMoveGroupMixin
from launch_mixins.lbr_description import LBRDescriptionMixin
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def launch_setup(context: LaunchContext) -> List[LaunchDescriptionEntity]:

    arg1 = DeclareLaunchArgument('x', default_value='0', description='First integer parameter')
    arg2 = DeclareLaunchArgument('y', default_value='0.5', description='Second integer parameter')
    arg3 = DeclareLaunchArgument('z', default_value='1', description='Third integer parameter')

    model = "iiwa7_table"

    # generate moveit configs
    moveit_configs = LBRMoveGroupMixin.moveit_configs_builder(
        robot_name=model,
        package_name=f"{model}_moveit_config",
    )

    # launch demo node
    node_action = Node(
        package="set_moveit_coords",
        executable="set_moveit_coords",
        parameters=[
            moveit_configs.to_dict(),
            {"use_sim_time": LaunchConfiguration("sim")},
            LBRDescriptionMixin.param_robot_name(),
            {"x": LaunchConfiguration('x')},
            {"y": LaunchConfiguration('y')},
            {"z": LaunchConfiguration('z')},
        ],
        arguments=[
            LaunchConfiguration('x'),
            LaunchConfiguration('y'),
            LaunchConfiguration('z'),
        ]
    )
    
    return [arg1, arg2, arg3, node_action]


def generate_launch_description() -> LaunchDescription:
    ld = LaunchDescription()
    

    ld.add_action(LBRDescriptionMixin.arg_model())
    ld.add_action(LBRDescriptionMixin.arg_robot_name())
    ld.add_action(LBRDescriptionMixin.arg_sim())

    ld.add_action(OpaqueFunction(function=launch_setup))
    return ld
