#message
from project_interfaces.action import JointValues    

#ROS2 imports
import rclpy
from rclpy.action import ActionServer  # action specific import
from rclpy.node import Node


class MoveRobotInWorld(Node):

    def __init__(self, node_name: str, namespace: str) -> None:
        super().__init__('node_name')

        # Initialize action server
        self._action_server = ActionServer(
            self,
            JointValues,
            'JointValues',
            self.JointValues_callback
        )

    # Callback to handle incoming joint values
    def JointValues_callback(self, goal_handle):
        # Log the received joint values
        self.get_logger().info(f"Received Joint Values: "
                               f"joint_1: {goal_handle.request.joint_1}, "
                               f"joint_2: {goal_handle.request.joint_2}, "
                               f"joint_3: {goal_handle.request.joint_3}, "
                               f"joint_4: {goal_handle.request.joint_4}, "
                               f"joint_5: {goal_handle.request.joint_5}, "
                               f"joint_6: {goal_handle.request.joint_6}, "
                               f"joint_7: {goal_handle.request.joint_7}")

        # Feedback is optional for now, so we just simulate some progress
        feedback_msg = JointValues.Feedback()
        feedback_msg.progress = True
        goal_handle.publish_feedback(feedback_msg)

        # Mark the goal as successful
        goal_handle.succeed()

        # Return the result
        result = JointValues.Result()
        result.success = True
        return result


def main(args=None):
    # Initialize ROS2 and class
    rclpy.init(args=args)
    node = MoveRobotInWorld("robot_control_world_axis", '/lbr')

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
