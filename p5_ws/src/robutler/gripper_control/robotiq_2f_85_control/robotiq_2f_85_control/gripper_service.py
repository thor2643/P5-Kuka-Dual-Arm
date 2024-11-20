
from .Robotiq2F85Driver import Robotiq2F85Driver
from time import sleep

from rclpy.node import Node
import rclpy

from robotiq_2f_85_interfaces.srv import Robotiq2F85GripperCommand



class Robotiq2F85GripperService(Node):
    def __init__(self):
        super().__init__('gripper_2f_service_async')
        self.detector_srv = self.create_service(Robotiq2F85GripperCommand, 'gripper_2f_service', self.gripper_callback)

        # Initialize the driver with the gripper's serial number
        self.gripper = Robotiq2F85Driver(serial_number='DA8BRYE3')
        self.gripper.reset()


    def gripper_callback(self, request, response):
        self.get_logger().info('Incoming request')
        width = request.width
        speed = request.speed
        force = request.force
        self.get_logger().info(f'Using gripper with following values:\n width: {width}\nspeed: {speed}\n force: {force}\n')

        self.gripper.go_to(opening=width, speed=speed, force=force)
        sleep(1)

        response.success = True
        return response


def main(args=None):
    rclpy.init(args=args)

    Gripper = Robotiq2F85GripperService()

    rclpy.spin(Gripper) 

    rclpy.shutdown()


if __name__ == '__main__':
    main()