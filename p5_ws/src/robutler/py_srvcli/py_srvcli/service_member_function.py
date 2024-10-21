from project_interfaces.srv import GetSixInts                                                           
#ROS2 KUKA FRI imports
from lbr_fri_idl.msg import LBRJointPositionCommand, LBRState # Joint control message, Data from KUKA

import rclpy
from rclpy.node import Node
from copy import deepcopy
import numpy as np

class MoveRobotInWorld(Node):

    def __init__(self, node_name: str, namespace: str) -> None:
        super().__init__('move_robot_in_world')  # Adjusted node name
        self._lbr_joint_position_command = LBRJointPositionCommand()
        
        self.goal1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Ensure these are floats
        self.goal2 = []
        
        self.goal1init = True
        self.goal2init = False

        # Create the service with correct message type and name
        self.srv = self.create_service(GetSevenInts, 'get_seven_ints', self.get_seven_ints_callback)

        # Create publisher to command joint positions
        self._lbr_joint_position_command_pub = self.create_publisher(LBRJointPositionCommand, "command/joint_position", 1) 

        # Create subscription to state
        self._lbr_state = None
        self._lbr_state_sub_ = self.create_subscription(LBRState, "state", self._on_lbr_state, 1)

    def get_seven_ints_callback(self, request, response):
        """Handle incoming service requests to set the goal position."""
        self.goal2 = [request.a, request.b, request.c, request.d, request.e, request.f, request.g]
        print(f"Goal2 values received from client: {self.goal2}")
        
        response.succes = True  # Use correct field 'succes'
        self.get_logger().info(
            'Incoming request\n a: %f b: %f c: %f d: %f e: %f f: %f g: %f' % 
            (request.a, request.b, request.c, request.d, request.e, request.f, request.g)
        )
        return response

    # Runs when message is received from "state"
    def _on_lbr_state(self, lbr_state: LBRState) -> None:
        """Handle incoming state data and update joint positions accordingly."""
        if self._lbr_state is None:
            self._lbr_state = lbr_state
        
        # Initialize the published message with current joint positions.
        self._lbr_joint_position_command.joint_position = deepcopy(self._lbr_state.measured_joint_position)

        self.get_logger().info(f"Current measured joint positions: {self._lbr_state.measured_joint_position}")
        
        if lbr_state.session_state == 4:  # KUKA::FRI::COMMANDING_ACTIVE == 4
            # Basic robot movement from goal 1 to goal 2 and back
            if self.goal1init:
                difference = np.subtract(self.goal1, self._lbr_state.measured_joint_position)
                
                # Check if all differences are <= 0.1 to stop infinite interpolation
                if np.all(np.abs(difference) <= 0.1):
                    self.goal1init = False
                    self.goal2init = True
                else:
                    for i in range(len(self._lbr_joint_position_command.joint_position)):
                        self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)
                    self.get_logger().info(f"Sending joint position command: {self._lbr_joint_position_command.joint_position}")

            # Move to goal2
            elif self.goal2init:
                difference = np.subtract(self.goal2, self._lbr_state.measured_joint_position)

                if np.all(np.abs(difference) <= 0.1):
                    self.goal1init = True
                    self.goal2init = False
                else:
                    for i in range(len(self._lbr_joint_position_command.joint_position)):
                        self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)
                    self.get_logger().info(f"Sending joint position command: {self._lbr_joint_position_command.joint_position}")

        self._lbr_state = lbr_state


def main(args=None):
    # Initialize ROS2 and class
    rclpy.init(args=args)
    node = MoveRobotInWorld("robot_control_world_axis", '/lbr')
    rclpy.spin(node)  # Keep the node running
    rclpy.shutdown()

if __name__ == '__main__':
    main()
