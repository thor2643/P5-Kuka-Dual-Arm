#Basics
import sys
from copy import deepcopy

#RosPy imports
import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import GetParameters # <- Don't know if we need this currently, it's used to get the parameters of services

#ROS2 KUKA FRI imports
from lbr_fri_idl.msg import LBRJointPositionCommand, LBRState # Joint control message, Data from KUKA


class MoveRobotInWorld(Node):
    def __init__(self, node_name: str, location_args: list[float]) -> None: # NOTE: -> None to ensure compile error if the node tries to return anything.
        super().__init__(node_name)
        
        self.location_args = location_args
        self._lbr_joint_position_command = LBRJointPositionCommand()

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
            # NOTE: It seems the joints are pushed by 1, so [6] referes to the 7th joint. [0] to 1 and so on
            
            # NOTE: Test code to move robots 7th joint to 45 degrees
            if self._lbr_joint_position_command.joint_position[6] != 3.14/2:

                # Calculate the difference between the current and target angle
                angle_diff = (3.14/2) - self._lbr_joint_position_command.joint_position[6]

                # Adjust for wraparound to ensure shortest rotation
                if angle_diff > pi:  # If the difference is more than 180 degrees
                    angle_diff -= 2 * pi  # Take the shorter route counter-clockwise
                elif angle_diff < -pi:
                    angle_diff += 2 * pi  # Take the shorter route clockwise
                
                if abs(angle_diff) > 0.01:  # If there's still a significant difference (e.g., greater than 0.01 radians)
                    self._lbr_joint_position_command.joint_position[6] += angle_diff * (1 / 400)  # Slow movement, 100 Hz, 4 seconds
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)

            """
            self._lbr_joint_position_command.joint_position[6]
            """


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
    rclpy.spin(MoveRobotInWorld("robot_control_world_axis", location_args))
    rclpy.shutdown()
    return 0

if __name__ == "__main__":
    main()
