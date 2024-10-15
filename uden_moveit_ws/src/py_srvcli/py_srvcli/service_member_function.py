from tutorial_interfaces.srv import GetSixInts                                                           
#ROS2 KUKA FRI imports
from lbr_fri_idl.msg import LBRJointPositionCommand, LBRState # Joint control message, Data from KUKA

import rclpy
from rclpy.node import Node

#Basics
import sys
from copy import deepcopy
import math
import numpy as np



class MoveRobotInWorld(Node):

    def __init__(self, node_name: str, namespace: str) -> None: # NOTE: -> None to ensure compile error if the node tries to return anything.
        super().__init__('node_name')
        self._lbr_joint_position_command = LBRJointPositionCommand()
        
        self.goal1 = [0,0,0,0,0,0,0]
        self.goal2 = []
        
        self.goal1init = True
        self.goal2init = False

        #Now we create the Service Node:
        self.srv = self.create_service(GetSixInts, 'get_six_ints', self.get_six_ints_callback)       #i know the naming convention is not up to date TODo

    def get_six_ints_callback(self, request, response):
        self.goal2 = [request.a, request.b, request.c, request.d, request.e, request.f, request.g]
        print(self.goal2)
        response.succes = True                                                   
        self.get_logger().info('Incoming request\na: %f b: %f c: %f d: %f e: %f f: %f g: %f' % (request.a, request.b, request.c, request.d, request.e, request.f, request.g))  
        
        # Create publisher to command/joint_position
        self._lbr_joint_position_command_pub = self.create_publisher(LBRJointPositionCommand, 
        "command/joint_position", 1) 

        # Create subscription to state
        self._lbr_state = None
        self._lbr_state_sub_ = self.create_subscription(LBRState, 
        "state", self._on_lbr_state, 1)
        return response   #OBS måske lukkes der for vores sub og pub når dette gøres.

    # Runs when message recived from "state"
    def _on_lbr_state(self, lbr_state: LBRState) -> None:
        # Synchronize lbr_state with current robot state
        if self._lbr_state is None:
            self._lbr_state = lbr_state
        
        # Initilize the published message with current joint positions.
        self._lbr_joint_position_command.joint_position = deepcopy(self._lbr_state.measured_joint_position)

        if lbr_state.session_state == 4:  # KUKA::FRI::COMMANDING_ACTIVE == 4
            # We want to do a basic robot movement via hardcoding, which moves the robot from goal 1 to goal 2 and back
            if self.goal1init == True:
                difference = np.subtract(self.goal1, self._lbr_state.measured_joint_position)
                
                # Check if all differences are <= 0.1 to stop infinite interpolation
                if np.all(np.abs(difference) <= 0.1):
                    self.goal1init = False
                    self.goal2init = True
                else:
                    for i in range(len(self._lbr_joint_position_command.joint_position)):
                        self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)

            # Pratically idential functionallity as code above, but the goal is moved.
            if self.goal2init == True:
                difference = np.subtract(self.goal2, self._lbr_state.measured_joint_position)

                if np.all(np.abs(difference) <= 0.1):
                    self.goal1init = True
                    self.goal2init = False
                else:
                    for i in range(len(self._lbr_joint_position_command.joint_position)):
                        self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    
                    self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command)

        self._lbr_state = lbr_state


def main(args=None):
    # TODO: Make a seperate program for the LLM to update the target location by publishing to a message. So this program just reads that message,
    # as the current system only allows for one position per run of the code. 
    #location_args = sys.argv[1:] # Take additional argument inputs from terminal, needed to set desired positon

    # Intilize ROS2 and Class
    rclpy.init(args=args)
    rclpy.spin(MoveRobotInWorld("robot_control_world_axis", '/lbr')) #Change namespace of node to /lbr
    rclpy.shutdown()

if __name__ == '__main__':
    main()




"""
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

"""