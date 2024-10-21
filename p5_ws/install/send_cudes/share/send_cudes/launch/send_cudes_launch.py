from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

from typing import List
from launch import LaunchContext, LaunchDescription, LaunchDescriptionEntity
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration

# LBR imports
from lbr_bringup.description import LBRDescriptionMixin
from lbr_bringup.move_group import LBRMoveGroupMixin
     
    
def hidden_setup(context: LaunchContext) -> List[LaunchDescriptionEntity]:
    ld = LaunchDescription()

    #Disable gazebo time i think
    use_sim_time = False
    
    model = "iiwa7";
    mode = "mock";

    # generate moveit configs
    moveit_configs = LBRMoveGroupMixin.moveit_configs_builder("iiwa7",package_name="moveit2_launch")

    # launch demo node
    ld.add_action(
        Node(
            package="send_cudes",
            executable="send_cudes",
            parameters=[
                moveit_configs.to_dict(),
                LBRDescriptionMixin.param_robot_name(),
            ],
        )
    )
    return ld.entities


def generate_launch_description() -> LaunchDescription:
    ld = LaunchDescription()

    ld.add_action(LBRDescriptionMixin.arg_model())
    ld.add_action(LBRDescriptionMixin.arg_mode())

    ld.add_action(OpaqueFunction(function=hidden_setup))

    return ld
    
  

