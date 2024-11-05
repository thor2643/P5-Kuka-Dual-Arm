import sys

from project_interfaces.srv import MoveCommand
import rclpy
from rclpy.node import Node


class RobotClientAsync(Node):

    def __init__(self):
        super().__init__('robot_client_async')
        self.cli = self.create_client(MoveCommand, 'move_command')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = MoveCommand.Request()

    def send_request(self):
        self.req.position.x = float(0.0)
        self.req.position.y = float(0.5)
        self.req.position.z = float(1.8)
        self.req.orientation.w = float(1.0)
 
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    minimal_client = RobotClientAsync()
    response = minimal_client.send_request()
    minimal_client.get_logger().info(f"Got: {response.result}")

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()