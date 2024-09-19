#Basics
import sys
from copy import deepcopy
import math
import numpy as np

#RosPy imports
import rclpy
from rclpy.node import Node

#ROS2 KUKA FRI imports
from lbr_fri_idl.msg import LBRJointPositionCommand, LBRState # Joint control message, Data from KUKA


class MoveRobotInWorld(Node):
    def __init__(self, node_name: str, namespace: str, location_args: list[float]) -> None: # NOTE: -> None to ensure compile error if the node tries to return anything.
        super().__init__(node_name, namespace=namespace)
        self.location_args = location_args
        self._lbr_joint_position_command = LBRJointPositionCommand()
        
        self.goal1 = [0,0,0,0,0,0,0]
        self.goal2 = [0,0,0,0,0,0,math.pi/2]
        
        self.goal1init = True
        self.goal2init = False

        print(str(self.location_args))

        # Create publisher to command/joint_position
        self._lbr_joint_position_command_pub = self.create_publisher(LBRJointPositionCommand, 
        "command/joint_position", 1) 

        # Create subscription to state
        self._lbr_state = None
        self._lbr_state_sub_ = self.create_subscription(LBRState, 
        "state", self._on_lbr_state, 1)

    # Runs when message recived from "state"
    def _on_lbr_state(self, lbr_state: LBRState) -> None:
        # Synchronize lbr_state with current robot state
        if self._lbr_state is None:
            self._lbr_state = lbr_state
        
        # Initilize the published message with current joint positions.
        self._lbr_joint_position_command.joint_position = deepcopy(self._lbr_state.measured_joint_position)
        
        print(str(self._lbr_state.measured_joint_position))

        if lbr_state.session_state == 4:  # KUKA::FRI::COMMANDING_ACTIVE == 4
            # We want to do a basic robot movement via hardcoding, which moves the robot from goal 1 to goal 2 and back
            if self.goal1init == True:
                if self.goal1 == self._lbr_state.measured_joint_position:
                    self.goal1init = False
                    self.goal2init = True
                else:
                    difference = np.subtract(self.goal1, self._lbr_state.measured_joint_position)
                    for i in len(self._lbr_joint_position_command.joint_position):
                        self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)

            if self.goal2init == True:
                if self.goal2 == self._lbr_state.measured_joint_position:
                    self.goal1init = True
                    self.goal2init = False
                else:
                    difference = np.subtract(self.goal2, self._lbr_state.measured_joint_position)
                    for i in len(self._lbr_joint_position_command.joint_position):
                        self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)

        self._lbr_state = lbr_state

def main():
    # TODO: Make a seperate program for the LLM to update the target location by publishing to a message. So this program just reads that message,
    # as the current system only allows for one position per run of the code. 
    location_args = sys.argv[1:] # Take additional argument inputs from terminal, needed to set desired positon

    # Sanity check for number of inputs
    if len(location_args) != 6:
        sys.exit(f"Function recived " + str(len(location_args)) + 
        " inputs, but expected 6 in the following format; x y z roll pitch yaw.")

    # Sanity check for input type
    for arg in location_args: 
        try:
            checked_value_float = float(arg)
            if "." not in arg:
                checked_value_int = int(arg)

        except ValueError:
            sys.exit(f"Function recived input of type '{type(arg).__name__}' but only expected inputs of type; int, float.")

        # Convert all entries to floats, to avoid type variance issues
        location_args = [float(arg) for arg in location_args]

    # TODO: Create a sanity check, to check if inputs are within the robots workspace. NOTE: We need a cell setup to do this.


    # Intilize ROS2 and Class
    rclpy.init(args=None)
    rclpy.spin(MoveRobotInWorld("robot_control_world_axis", '/lbr', location_args))
    rclpy.shutdown()
    return 0

if __name__ == "__main__":
    main()