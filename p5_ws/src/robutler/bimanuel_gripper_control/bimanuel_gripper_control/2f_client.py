# Basic ROS2
import rclpy
from rclpy.node import Node

# ROS2 interfaces
from project_interfaces.srv import RobotIQ2FOutput

# Debugging - Remove these from the finished solution
import time

class Move2F(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self._2f_controller = RobotIQ2FOutput.Request()

        self.state = 0 # Debugging

        self._2f_controller_cli = self.create_client(RobotIQ2FOutput, 
        "Robotiq2FGripper/OutputService") 

        # Wait for the service to be available
        while not self._2f_controller_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        # We need to somehow give the LLM access to these functions? - Ask Silas

        # Quick itteration through the basic controls of the RobotIQ 3F gripper
        while True:
            self.get_logger().info(str(self.state))
            time.sleep(1)

            if self.state == 0:
                self.gripper_bootup()
            elif self.state == 1:
                self.close_gripper()
            elif self.state == 2:
                self.open_gripper()
            elif self.state == 3:
                self.close_gripper_50()
            elif self.state == 4:
                self.open_gripper()
                break

            self.state += 1
        # This is all just to test functionallity, we will have to abstract, and let the LLM decide most variables :)


    def gripper_bootup(self): # Bootup Sequence, should only be called once.     
        self._2f_controller.output_registers.r_act = 1 # Active Gripper
        self._2f_controller.output_registers.r_ard = 1 # Open on ATR Trigger
        self._2f_controller.output_registers.r_gto = 1 # Go To Position
        self._2f_controller.output_registers.r_atr = 0 # Stop Automatic Release
        self._2f_controller.output_registers.r_pra = 0 # Open Gripper
        self._2f_controller.output_registers.r_spa = 255 # Max Speed
        self._2f_controller.output_registers.r_fra = 0 # Minimum Force

        # Publish command to gripper
        self.future = self._2f_controller_cli.call_async(self._2f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def open_gripper(self): # Bootup Sequence, should only be called once.     
        self._2f_controller.output_registers.r_act = 1 # Active Gripper
        self._2f_controller.output_registers.r_ard = 1 # Open on ATR Trigger
        self._2f_controller.output_registers.r_gto = 1 # Go To Position
        self._2f_controller.output_registers.r_atr = 0 # Stop Automatic Release
        self._2f_controller.output_registers.r_pra = 0 # Open Gripper
        self._2f_controller.output_registers.r_spa = 255 # Max Speed
        self._2f_controller.output_registers.r_fra = 0 # Minimum Force

        # Publish command to gripper
        self.future = self._2f_controller_cli.call_async(self._2f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def close_gripper(self): # Bootup Sequence, should only be called once.     
        self._2f_controller.output_registers.r_act = 1 # Active Gripper
        self._2f_controller.output_registers.r_ard = 1 # Open on ATR Trigger
        self._2f_controller.output_registers.r_gto = 1 # Go To Position
        self._2f_controller.output_registers.r_atr = 0 # Stop Automatic Release
        self._2f_controller.output_registers.r_pra = 1 # Close Gripper
        self._2f_controller.output_registers.r_spa = 255 # Max Speed
        self._2f_controller.output_registers.r_fra = 0 # Minimum Force

        # Publish command to gripper
        self.future = self._2f_controller_cli.call_async(self._2f_controller)
        rclpy.spin_until_future_complete(self, self.future)


    def close_gripper_50(self): # Bootup Sequence, should only be called once.     
        self._2f_controller.output_registers.r_act = 1 # Active Gripper
        self._2f_controller.output_registers.r_ard = 1 # Open on ATR Trigger
        self._2f_controller.output_registers.r_gto = 1 # Go To Position
        self._2f_controller.output_registers.r_atr = 0 # Stop Automatic Release
        self._2f_controller.output_registers.r_pra = 128 # Close Gripper 50%
        self._2f_controller.output_registers.r_spa = 255 # Max Speed
        self._2f_controller.output_registers.r_fra = 0 # Minimum Force

        # Publish command to gripper
        self.future = self._2f_controller_cli.call_async(self._2f_controller)
        rclpy.spin_until_future_complete(self, self.future)



def main(args=None):
    rclpy.init(args=args)
    node = Move2F("two_finger_command_publisher")
    rclpy.spin(node) 
    rclpy.shutdown()


if __name__ == '__main__':
    main()
