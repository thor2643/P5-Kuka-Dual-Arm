# Basic ROS2
import rclpy
from rclpy.node import Node

# ROS2 interfaces
from robotiq_3f_gripper_ros2_interfaces.srv import Robotiq3FGripperOutputService

# Debugging - Remove these from the finished solution
import time


class Move3F(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self._3f_controller = Robotiq3FGripperOutputService.Request()

        self.state = 0

        self._3f_controller_cli = self.create_client(Robotiq3FGripperOutputService, 
        "Robotiq3FGripper/OutputRegistersService") 

        # Wait for the service to be available
        while not self._3f_controller_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        # We need to somehow give the LLM access to these functions? - Ask Silas

        # Quick itteration through the basic controls of the RobotIQ 3F gripper
        while True:
            self.get_logger().info(str(self.state))
            time.sleep(1)

            if self.state == 0:
                self.gripper_bootup()
            elif self.state == 1:
                self.close_gripper_basic()
            elif self.state == 2:
                self.open_gripper()
            elif self.state == 3:
                self.close_gripper_pinch()
            elif self.state == 4:
                self.open_gripper()
            elif self.state == 5:
                self.close_gripper_wide()
            elif self.state == 6:
                self.open_gripper()
            elif self.state == 7:
                self.close_gripper_scissor()
            elif self.state == 8:
                self.open_gripper()
                break

            self.state += 1
        # This is all just to test functionallity, we will have to abstract, and let the LLM decide most variables :)


    def gripper_bootup(self): # Bootup Sequence, should only be called once.     
        self._3f_controller.output_registers.r_act = 1 # Active Gripper
        self._3f_controller.output_registers.r_mod = 0 # Basic Gripper Mode
        self._3f_controller.output_registers.r_gto = 1 # Go To Position
        self._3f_controller.output_registers.r_atr = 0 # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = 0 # Open Gripper
        self._3f_controller.output_registers.r_spa = 255 # Max Speed
        self._3f_controller.output_registers.r_fra = 0 # Minimum Force

        # Publish command to gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def open_gripper(self):  # Open Gripper
        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 0  # Basic Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = 0  # Open Gripper
        self._3f_controller.output_registers.r_spa = 255  # Max Speed
        self._3f_controller.output_registers.r_fra = 0  # Minimum Force

        # Publish command to gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)
        rclpy.spin_until_future_complete(self, self.future)



    def close_gripper_basic(self):  # Close Gripper in Basic Mode
        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 0  # Basic Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = 110  # Close Gripper
        self._3f_controller.output_registers.r_spa = 255  # Max Speed
        self._3f_controller.output_registers.r_fra = 0  # Minimum Force

        # Publish command to gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def close_gripper_pinch(self):  # Close Gripper in Pinch Mode
        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 1  # Pinch Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = 110  # Close Gripper
        self._3f_controller.output_registers.r_spa = 255  # Max Speed
        self._3f_controller.output_registers.r_fra = 125  # Minimum Force

        # Publish command to gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def close_gripper_wide(self):
        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 2  # Wide Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = 125  # Close Gripper
        self._3f_controller.output_registers.r_spa = 255  # Max Speed
        self._3f_controller.output_registers.r_fra = 0  # Minimum Force

        # Publish command to gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def close_gripper_scissor(self):
        self._3f_controller.output_registers.r_act = 1  # Active Gripper
        self._3f_controller.output_registers.r_mod = 3  # Scissor Gripper Mode
        self._3f_controller.output_registers.r_gto = 1  # Go To Position
        self._3f_controller.output_registers.r_atr = 0  # Stop Automatic Release
        self._3f_controller.output_registers.r_pra = 255  # Close Gripper
        self._3f_controller.output_registers.r_spa = 255  # Max Speed
        self._3f_controller.output_registers.r_fra = 0  # Minimum Force

        # Publish command to gripper
        self.future = self._3f_controller_cli.call_async(self._3f_controller)
        rclpy.spin_until_future_complete(self, self.future)


def main(args=None):
    rclpy.init(args=args)
    node = Move3F("three_finger_command_publisher")
    rclpy.spin(node) 
    rclpy.shutdown()


if __name__ == '__main__':
    main()