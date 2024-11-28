from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch_mixins.lbr_description import LBRDescriptionMixin
from launch_mixins.lbr_ros2_control import LBRROS2ControlMixin
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import (
    AndSubstitution,
    LaunchConfiguration,
    NotSubstitution,
    PathJoinSubstitution,
)


class LBRSystemInterface(LBRDescriptionMixin, LBRROS2ControlMixin):
    pass


def generate_launch_description() -> LaunchDescription:
    ld = LaunchDescription()
    ld.add_action(LBRSystemInterface.arg_model())
    ld.add_action(LBRSystemInterface.arg_robot_name())
    ld.add_action(LBRSystemInterface.arg_port_id())
    robot_description = LBRSystemInterface.param_robot_description(sim=False)
    ld.add_action(LBRSystemInterface.arg_ctrl_cfg_pkg())
    ld.add_action(LBRSystemInterface.arg_ctrl_cfg())
    ld.add_action(LBRSystemInterface.arg_ctrl())

    robot_state_publisher = LBRSystemInterface.node_robot_state_publisher(
        robot_description=robot_description,
        use_sim_time=False,
    )
    ld.add_action(robot_state_publisher)

    #ros2_control_node = LBRSystemInterface.node_ros2_control()
    #ld.add_action(ros2_control_node)

    # ros2 control node
    ros2_control_node_right = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"use_sim_time": False},
            PathJoinSubstitution(
                [
                    FindPackageShare(
                        LaunchConfiguration(
                            "ctrl_cfg_pkg", default="lbr_ros2_control"
                        )
                    ),
                    LaunchConfiguration(
                        "ctrl_cfg", default="config/lbr_controllers.yaml"
                    ),
                ]
            ),
        ],
        namespace="lbr",
        remappings=[
            ("~/robot_description", "robot_description"),
        ],
    )

    ros2_control_node_left = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"use_sim_time": False},
            PathJoinSubstitution(
                [
                    FindPackageShare(
                        LaunchConfiguration(
                            "ctrl_cfg_pkg", default="lbr_ros2_control_left"
                        )
                    ),
                    LaunchConfiguration(
                        "ctrl_cfg", default="config/lbr_controllers_left.yaml"
                    ),
                ]
            ),
        ],
        namespace="lbr",
        remappings=[
            ("~/robot_description", "robot_description"),
        ],
    )

    ld.add_action(ros2_control_node_right)
    ld.add_action(ros2_control_node_left)


    joint_state_broadcaster = LBRSystemInterface.node_controller_spawner(
        controller="joint_state_broadcaster"
    )
    force_torque_broadcaster = LBRSystemInterface.node_controller_spawner(
        controller="force_torque_broadcaster"
    )
    lbr_state_broadcaster = LBRSystemInterface.node_controller_spawner(
        controller="lbr_state_broadcaster"
    )
    controller = LBRSystemInterface.node_controller_spawner(
        controller=LaunchConfiguration("ctrl")
    )
    controller_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=ros2_control_node_right,
            on_start=[
                joint_state_broadcaster,
                force_torque_broadcaster,
                lbr_state_broadcaster,
                controller,
            ],
        )
    )
    ld.add_action(controller_event_handler)
    return ld
