from typing import List

from launch import LaunchContext, LaunchDescription, LaunchDescriptionEntity
from launch.actions import DeclareLaunchArgument, OpaqueFunction, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessStart
from launch.substitutions import (
    AndSubstitution,
    LaunchConfiguration,
    NotSubstitution,
    PathJoinSubstitution,
)
from launch_mixins.lbr_bringup import LBRMoveGroupMixin
from launch_mixins.lbr_description import LBRDescriptionMixin, RVizMixin
from launch_mixins.lbr_ros2_control import LBRROS2ControlMixin


def launch_setup(context: LaunchContext) -> List[LaunchDescriptionEntity]:
    ld = LaunchDescription()

    robot_description = LBRDescriptionMixin.param_robot_description(model = "iiwa7_table", sim=False)
    world_robot_tf = [0, 0, 0, 0, 0, 0]  # keep zero
    
    robot_description_left = LBRDescriptionMixin.param_robot_description(model = "iiwa7", robot_name = "lbr_left", port_id = "30201", sim=False)
    world_robot_left_tf = [0, 0, 0, 0, 0, 0]

    # robot state publisher
    robot_state_publisher = LBRROS2ControlMixin.node_robot_state_publisher(
        robot_description=robot_description, use_sim_time=False
    )
    robot_state_publisher_left = LBRROS2ControlMixin.node_robot_state_publisher(
        robot_description=robot_description_left, use_sim_time=False
    )
    
    ld.add_action(robot_state_publisher)
    ld.add_action(robot_state_publisher_left)

    # ros2 control node
    ros2_control_node = LBRROS2ControlMixin.node_ros2_control()
    ros2_control_node_left = LBRROS2ControlMixin.node_ros2_control(
        robot_name="lbr_left"
    )
    
    ld.add_action(ros2_control_node)
    ld.add_action(ros2_control_node_left)

    # joint state broad caster and controller on ros2 control node start
    joint_state_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        controller="joint_state_broadcaster"
    )
    force_torque_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        controller="force_torque_broadcaster"
    )
    lbr_state_broadcaster = LBRROS2ControlMixin.node_controller_spawner(
        controller="lbr_state_broadcaster"
    )
    controller = LBRROS2ControlMixin.node_controller_spawner(
        controller=LaunchConfiguration("ctrl")
    )

    # Same as above, but for the left robot.
    joint_state_broadcaster_left = LBRROS2ControlMixin.node_controller_spawner(
        robot_name ="lbr_left",
        controller="joint_state_broadcaster"
    )
    force_torque_broadcaster_left = LBRROS2ControlMixin.node_controller_spawner(
        robot_name ="lbr_left",
        controller="force_torque_broadcaster"
    )
    lbr_state_broadcaster_left = LBRROS2ControlMixin.node_controller_spawner(
        robot_name ="lbr_left",
        controller="lbr_state_broadcaster"
    )
    controller_left = LBRROS2ControlMixin.node_controller_spawner(
        robot_name ="lbr_left",
        controller=LaunchConfiguration("ctrl")
    )

    controller_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=ros2_control_node,
            on_start=[
                joint_state_broadcaster,
                force_torque_broadcaster,
                lbr_state_broadcaster,
                controller,
            ],
        )
    )

    controller_event_handler_left = RegisterEventHandler(
        OnProcessStart(
            target_action=ros2_control_node_left,
            on_start=[
                joint_state_broadcaster_left,
                force_torque_broadcaster_left,
                lbr_state_broadcaster_left,
                controller_left,
            ],
        )
    )

    ld.add_action(controller_event_handler)
    ld.add_action(controller_event_handler_left)

    # MoveIt 2
    ld.add_action(LBRMoveGroupMixin.arg_allow_trajectory_execution())
    ld.add_action(LBRMoveGroupMixin.arg_capabilities())
    ld.add_action(LBRMoveGroupMixin.arg_disable_capabilities())
    ld.add_action(LBRMoveGroupMixin.arg_monitor_dynamics())
    ld.add_action(LBRMoveGroupMixin.args_publish_monitored_planning_scene())

    # MoveGroup:
    # - requires world frame
    # - urdf only has robot_name/world
    # This transform needs publishing
    robot_name = LaunchConfiguration("robot_name").perform(context)
    ld.add_action(
        LBRDescriptionMixin.node_static_tf(
            tf=world_robot_tf,
            parent="world",
            child=PathJoinSubstitution(
                [
                    robot_name,
                    "world",
                ]  # results in robot_name/world
            ),
        )
    )

    # Just a slight bit of hard-coding - change to kuka_table_left, when implementing
    robot_name_left = "lbr_left"
    ld.add_action(
        LBRDescriptionMixin.node_static_tf(
            tf=world_robot_left_tf,
            parent="world",
            child=PathJoinSubstitution(
                [
                    robot_name_left,
                    "world",
                ]  # results in robot_name_left/world
            ),
        )
    )

    # Build test - Once again, a good bit of hardcoding
    model = "iiwa7_table"
    moveit_configs_builder = LBRMoveGroupMixin.moveit_configs_builder(
        robot_name=model,
        package_name=f"{model}_moveit_config", # Change this to new package name when merging
    )
    move_group_params = LBRMoveGroupMixin.params_move_group()

    model_left = "iiwa7"
    moveit_configs_builder_left = LBRMoveGroupMixin.moveit_configs_builder(
        robot_name=model_left,
        package_name=f"{model_left}_moveit_config",
    )
    move_group_params_left = LBRMoveGroupMixin.params_move_group() # I have a sneeking suspision, that this is not nessecary - test later

    ld.add_action(
        LBRMoveGroupMixin.node_move_group(
            parameters=[
                moveit_configs_builder.to_dict(),
                move_group_params,
                {"use_sim_time": False},
            ],
            condition=IfCondition(LaunchConfiguration("moveit")),
            namespace=robot_name,
        )
    )
    ld.add_action(
        LBRMoveGroupMixin.node_move_group(
            parameters=[
                moveit_configs_builder_left.to_dict(),
                move_group_params_left,
                {"use_sim_time": False},
            ],
            condition=IfCondition(LaunchConfiguration("moveit")),
            namespace=robot_name_left,
        )
    )

    # RViz and MoveIt
    rviz_moveit = RVizMixin.node_rviz(
        rviz_config_pkg=f"{model}_moveit_config",
        rviz_config="config/moveit.rviz",
        parameters=LBRMoveGroupMixin.params_rviz(
            moveit_configs=moveit_configs_builder.to_moveit_configs()
        )
        + [{"use_sim_time": False}],
        condition=IfCondition(
            AndSubstitution(LaunchConfiguration("moveit"), LaunchConfiguration("rviz"))
        ),
        remappings=[
            ("display_planned_path", robot_name + "/display_planned_path"),
            ("joint_states", robot_name + "/joint_states"),
            ("monitored_planning_scene", robot_name + "/monitored_planning_scene"),
            ("planning_scene", robot_name + "/planning_scene"),
            ("planning_scene_world", robot_name + "/planning_scene_world"),
            ("robot_description", robot_name + "/robot_description"),
            ("robot_description_semantic", robot_name + "/robot_description_semantic"),
        ],
    )

    # RViz and MoveIt
    rviz_moveit_left = RVizMixin.node_rviz(
        rviz_config_pkg=f"{model_left}_moveit_config",
        rviz_config="config/moveit.rviz",
        parameters=LBRMoveGroupMixin.params_rviz(
            moveit_configs=moveit_configs_builder_left.to_moveit_configs()
        )
        + [{"use_sim_time": False}],
        condition=IfCondition(
            AndSubstitution(LaunchConfiguration("moveit"), LaunchConfiguration("rviz"))
        ),
        remappings=[
            ("display_planned_path", robot_name_left + "/display_planned_path"),
            ("joint_states", robot_name_left + "/joint_states"),
            ("monitored_planning_scene", robot_name_left + "/monitored_planning_scene"),
            ("planning_scene", robot_name_left + "/planning_scene"),
            ("planning_scene_world", robot_name_left + "/planning_scene_world"),
            ("robot_description", robot_name_left + "/robot_description"),
            ("robot_description_semantic", robot_name_left + "/robot_description_semantic"),
        ],
    )


    # RViz no MoveIt
    rviz = RVizMixin.node_rviz(
        rviz_config_pkg="lbr_bringup",
        rviz_config="config/config.rviz",
        condition=IfCondition(
            AndSubstitution(
                LaunchConfiguration("rviz"),
                NotSubstitution(LaunchConfiguration("moveit")),
            )
        ),
    )

    # RViz event handler
    rviz_event_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=joint_state_broadcaster,
            on_start=[rviz_moveit]
        )
    )

    # Had to move the actual rviz launch to the second event handler to avoid 2 rviz instances. (Or a missed robot arm boot)
    rviz_event_handler_left = RegisterEventHandler(
        OnProcessStart(
            target_action=joint_state_broadcaster_left,
            on_start=[rviz_moveit_left, rviz]
        )
    )
    
    ld.add_action(rviz_event_handler)
    ld.add_action(rviz_event_handler_left)

    return ld.entities


def generate_launch_description() -> LaunchDescription:
    ld = LaunchDescription()
    ld.add_action(LBRDescriptionMixin.arg_model())
    ld.add_action(LBRDescriptionMixin.arg_robot_name())
    ld.add_action(LBRDescriptionMixin.arg_port_id())
    ld.add_action(
        DeclareLaunchArgument(
            name="moveit",
            default_value="false",
            description="Whether to launch MoveIt 2.",
        )
    )
    ld.add_action(
        DeclareLaunchArgument(
            name="rviz", default_value="true", description="Whether to launch RViz."
        )
    )
    ld.add_action(LBRROS2ControlMixin.arg_ctrl_cfg_pkg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl_cfg())
    ld.add_action(LBRROS2ControlMixin.arg_ctrl())
    ld.add_action(OpaqueFunction(function=launch_setup))
    return ld
