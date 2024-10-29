import sys

from project_interfaces.srv import GetObjectInfo
import rclpy
from rclpy.node import Node


class DetectorClientAsync(Node):

    def __init__(self):
        super().__init__('detector_client_async')
        self.cli = self.create_client(GetObjectInfo, 'get_object_info')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetObjectInfo.Request()

    def send_request(self, object):
        self.req.object_name = object
 
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    minimal_client = DetectorClientAsync()
    response = minimal_client.send_request(sys.argv[1])
    minimal_client.get_logger().info(f"Found {response.object_count}")

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()