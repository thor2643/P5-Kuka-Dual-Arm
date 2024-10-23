#message
from project_interfaces.action import JointValues    

#ROS2 KUKA FRI imports
from lbr_fri_idl.msg import LBRJointPositionCommand, LBRState # Joint control message, Data from KUKA

#ROS2 imports
import rclpy
from rclpy.action import ActionServer #action specefic import
from rclpy.node import Node

#Basics
import sys
from copy import deepcopy
import math
import numpy as np

class MoveRobotInWorld(Node):

    def __init__(self, node_name: str, namespace: str) -> None: # NOTE: -> None to ensure compile error if the node tries to return anything.
        super().__init__('node_name')
        self._action_server = ActionServer(  #Maybe this should be moved below the subscription like it was in the previous code
            self,
            JointValues,
            'JointValues',
            self.JointValues_callback)
        
        self._lbr_joint_position_command = LBRJointPositionCommand()
        
        #initisalize goal and control feedback
        self.goal= [0,0,0,0,0,0,0]
        self.control_feedback = 0

        # Create publisher to command/joint_position
        self._lbr_joint_position_command_pub = self.create_publisher(LBRJointPositionCommand, 
        "command/joint_position", 1) # Publishes the joint position command to the robot
        
        # Create subscription to state
        self._lbr_state = None
        self._lbr_state_sub_ = self.create_subscription(LBRState, 
        "state", self._on_lbr_state, 1) #gets called each time the state of the robot chances, so _on_lbr_state can be used to move the robot and so on 



    def JointValues_callback(self, goal_handle):  #Sets the goal position to the recieved values and sends back a confirmation response
        self.goal = [goal_handle.joint_1, goal_handle.joint_2, goal_handle.joint_3, goal_handle.joint_4, goal_handle.joint_5, goal_handle.joint_6, goal_handle.joint_7]                                                 
        self.get_logger().info('Incoming request\n joint_1: %f 2: %f 3: %f 4: %f 5: %f 6: %f 7: %f' % (goal_handle.joint_1, goal_handle.joint_2, goal_handle.joint_3, goal_handle.joint_4, goal_handle.joint_5, goal_handle.joint_6, goal_handle.joint_7))

        feedback_msg = JointValues.Feedback()
        feedback_msg.progress = True 

        print('Goal before: ' + str(self.goal))  
        self.goal = [goal_handle.joint_1, goal_handle.joint_2, goal_handle.joint_3, goal_handle.joint_4, goal_handle.joint_5, goal_handle.joint_6, goal_handle.joint_7]
        print('Goal after:' + str(self.goal))  

        #here our code must be checking if goal is reached. if it isnt we keep sending feedback and not the result
        while np.all(np.abs(np.subtract(self.goal, self._lbr_state.measured_joint_position)) >= 0.1): #Maybe this should be based on a bool variable that is set to True when the goal is reached
            feedback_msg.progress = True #telling the client that the goal has not been reached yet, but the robot is working on it
            self.control_feedback += 1 
            if self.control_feedback % 10 == 0:   #chance this based on need or use rclpy.sleep()
                goal_handle.publish_feedback(feedback_msg) #OBS this might spam the client
            

        goal_handle.succeed() #Marks the goal as successfully completed, 
        #meaning the requested task was fulfilled.

        result = JointValues.Result()
        result.success = True #As goal has been reached, the result/succes is set to True
        return result
        

    # Runs when message recived from "state"
    def _on_lbr_state(self, lbr_state: LBRState) -> None:

        print('State recieved')

        # Synchronize lbr_state with current robot state
        if self._lbr_state is None:
            self._lbr_state = lbr_state
        
        # Initilize the published message with current joint positions. This is done to enable that we can move it in increments
        self._lbr_joint_position_command.joint_position = deepcopy(self._lbr_state.measured_joint_position)

        if lbr_state.session_state == 4:  # KUKA::FRI::COMMANDING_ACTIVE == 4 #Cecking if the robat are ready to recive commands           

            difference = np.subtract(self.goal, self._lbr_state.measured_joint_position) #used to check if the robot is at the desired location
                    
            # Check if all differences are <= 0.1 to stop infinite interpolation
            if np.all(np.abs(difference) <= 0.1):
                pass #This happens when the robot is at the desired location and the robot should not move
            else: #in the Case where a client has given a new desired goal2 the following code will move the robot to the new goal2 # We want to do a basic robot movement via hardcoding, which moves the robot from goal 1 to goal 2 and back
                for i in range(len(self._lbr_joint_position_command.joint_position)): #Iterates through all joints
                    self._lbr_joint_position_command.joint_position[i] += difference[i] * (1 / 100)
                    
                self._lbr_joint_position_command_pub.publish(self._lbr_joint_position_command) #moves the robot

        self._lbr_state = lbr_state


def main(args=None):
    # Intilize ROS2 and Class
    rclpy.init(args=args)
    node = MoveRobotInWorld("robot_control_world_axis", '/lbr')

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        print("shutting down")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

"""
def main(args=None):
    # TODO: Make a seperate program for the LLM to update the target location by publishing to a message. So this program just reads that message,
    # as the current system only allows for one position per run of the code. 
    #location_args = sys.argv[1:] # Take additional argument inputs from terminal, needed to set desired positon

    # Intilize ROS2 and Class
    rclpy.init(args=args)
    node = MoveRobotInWorld("robot_control_world_axis", '/lbr')

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        print("shutting down")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
"""
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