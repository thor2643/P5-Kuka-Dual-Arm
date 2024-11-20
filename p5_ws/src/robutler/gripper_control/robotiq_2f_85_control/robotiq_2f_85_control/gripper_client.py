from robotiq_2f_85_interfaces.srv import Robotiq2F85GripperCommand
import rclpy
from rclpy.node import Node
import sys

class GripperClient(Node):

    def __init__(self):
        super().__init__('gripper_client')
        self.cli = self.create_client(Robotiq2F85GripperCommand, 'gripper_2f_service')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Robotiq2F85GripperCommand.Request()

    def send_request(self, width, speed, force):
        self.req.width = float(width)
        self.req.speed = float(speed)
        self.req.force = float(force)
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 4:
        print("Usage: gripper_client.py <width> <speed> <force>")
        return

    width = sys.argv[1]
    speed = sys.argv[2]
    force = sys.argv[3]

    gripper_client = GripperClient()
    gripper_client.send_request(width, speed, force)

    while rclpy.ok():
        rclpy.spin_once(gripper_client)
        if gripper_client.future.done():
            try:
                response = gripper_client.future.result()
            except Exception as e:
                gripper_client.get_logger().info('Service call failed %r' % (e,))
            else:
                gripper_client.get_logger().info('Result: %r' % (response,))
            break

    gripper_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()