from typing import Dict, List, Optional, Union

from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


class LBRDescriptionMixin:
    @staticmethod
    def param_robot_description(
        model: Optional[Union[LaunchConfiguration, str]] = LaunchConfiguration(
            "model", default="iiwa7"
        ),
        robot_name: Optional[Union[LaunchConfiguration, str]] = LaunchConfiguration(
            "robot_name", default="lbr"
        ),
        port_id: Optional[Union[LaunchConfiguration, str]] = LaunchConfiguration(
            "port_id", default="30200"
        ),
        mode: Optional[Union[LaunchConfiguration, bool]] = LaunchConfiguration(
            "mode", default="mock"
        ),
    ) -> Dict[str, str]:
        robot_description = {
            "robot_description": Command(
                [
                    FindExecutable(name="xacro"),
                    " ",
                    PathJoinSubstitution(
                        [
                            FindPackageShare("lbr_description"),
                            "urdf",
                            model,
                            model,
                        ]
                    ),
                    ".xacro",
                    " robot_name:=",
                    robot_name,
                    " port_id:=",
                    port_id,
                    " mode:=",
                    mode,
                ]
            )
        }
        return robot_description

    @staticmethod
    def arg_model(default_value: str = "iiwa7") -> DeclareLaunchArgument:
        return DeclareLaunchArgument(
            name="model",
            default_value=default_value,
            description="The LBR model in use.",
            choices=["iiwa7", "iiwa14", "med7", "med14"],
        )

    @staticmethod
    def arg_robot_name(default_value: str = "lbr") -> DeclareLaunchArgument:
        return DeclareLaunchArgument(
            name="robot_name",
            default_value=default_value,
            description="The robot's name.",
        )

    @staticmethod
    def arg_port_id(default_value: str = "30200") -> DeclareLaunchArgument:
        return DeclareLaunchArgument(
            name="port_id",
            default_value=default_value,
            description="Port ID of the FRI communication. Valid in range [30200, 30209].\n"
            "\tUsefull in multi-robot setups.",
        )

    @staticmethod
    def arg_mode(default_value: str = "mock") -> DeclareLaunchArgument:
        return DeclareLaunchArgument(
            name="mode",
            default_value=default_value,
            description="The mode to launch in.",
            choices=[
                "mock",
                "hardware",
                "gazebo",
            ],
        )

    @staticmethod
    def param_robot_name() -> Dict[str, LaunchConfiguration]:
        return {"robot_name": LaunchConfiguration("robot_name", default="lbr")}

    @staticmethod
    def param_port_id() -> Dict[str, LaunchConfiguration]:
        return {"port_id": LaunchConfiguration("port_id", default="30200")}

    @staticmethod
    def param_mode() -> Dict[str, LaunchConfiguration]:
        return {"mode": LaunchConfiguration("mode", default="mock")}

    @staticmethod
    def node_static_tf(
        tf: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        parent: Optional[Union[LaunchConfiguration, str]] = None,
        child: Optional[Union[LaunchConfiguration, str]] = None,
        **kwargs,
    ) -> Node:
        if len(tf) != 6:
            raise ValueError("tf must be a list of 6 floats.")
        label = ["--x", "--y", "--z", "--roll", "--pitch", "--yaw"]
        tf = [str(x) for x in tf]
        return Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            output="screen",
            arguments=[item for pair in zip(label, tf) for item in pair]
            + [
                "--frame-id",
                parent,
                "--child-frame-id",
                child,
            ],
            **kwargs,
        )
