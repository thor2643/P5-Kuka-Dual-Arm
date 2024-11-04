# Basic ROS2
import rclpy
from rclpy.node import Node

# Executor and callback imports
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# ROS2 interfaces
from project_interfaces.msg import RobotIQ2FInputReg
from project_interfaces.srv import RobotIQ2FOutput

# Others
import time, threading, math
from pymodbus.client import ModbusTcpClient


class GripperServiceServer(Node):
    '''
    Notes:
    * This code takes "HEAVY" inspiration from the 3F gripper control service published by a previous year of study, their project can be found at:
    * https://github.com/andreasHovaldt/LLM-Planner-for-Bimanual-object-manipulation
    * For ease of code review, note that every section changed by us, will have a comment containing at least a "*"


    * Starts a service server for controlling the gripper.
    * The service uses the RobotIQ2FOutput.srv custom interface (which uses "RobotIQ2FOutput" msg for interacting with it)
    * Publishes status of gripper to the Robotiq2FGripper/Input topic (Using "RobotIQ2FInput" msg)
    * Default IP is ...? and the port is 502 (Modbus port)
    '''
    def __init__(self):
        super().__init__("two_finger_service")
        
        # Declare parameters for node
        self.declare_parameter("gripper_address", "...")  # * TODO: Add a unique ip adress for the 2F gripper
        address = self.get_parameter("gripper_address").get_parameter_value().string_value
        
        self.get_logger().info(f"Gripper service starting on {address}...")
        
        # Variable Init
        self.gripper_connection_init(address)
        self.output_register_command = [9,0,0,0,128,0]  #[action_request,0,0,start_pos,start_speed,start_force] - * This forces a bootup sequence - 9 for Go To & Activate
        self.lock = threading.Lock() # * Modbus is made for Java, so we need to emulate java threading?

        # Callback groups
        self.group_1 = MutuallyExclusiveCallbackGroup() # gripper service
        self.group_2 = MutuallyExclusiveCallbackGroup() # gripper read input registers timer
        
        # msgs init
        self.input_registers = RobotIQ2FInputReg()
        
        # Publisher
        self._input_register_pub = self.create_publisher(RobotIQ2FInputReg, "Robotiq2FGripper/Input", 10)
        
        # Service
        self._output_register_service = self.create_service(RobotIQ2FOutput, "Robotiq2FGripper/OutputService", self.service_callback, callback_group=self.group_1)

        # Timer
        self._read_input_timer = self.create_timer(0.1, self.read_input_registers, callback_group=self.group_2)
        
        self.get_logger().info("Gripper service start-up successful!")


    def gripper_connection_init(self, address):
        self.client = ModbusTcpClient(address) # Create client object
        self.client.connect() # Connect client to gripper


    def service_callback(self, request, response):
        output_registers_list = self.output_registers_msg_to_list(request.output_registers) # Convert msg to list
        self.send_data(output_registers_list) # Send list to gripper
        
        
        while True:
            time.sleep(0.2) # Let the gripper process the msg for the given amount of time

            # Assign status to variables
            gSTA = self.input_registers.g_sta
            gIMC = self.input_registers.g_imc
            self.get_logger().info(f"gSTA = {gSTA}    gIMC = {gIMC}")

            # Check the gripper activation, mode, and position has reached stop point
            if gSTA != 0 and gIMC == 3:
                self.get_logger().info("Register message successfully completed")
                response.success = True
                break
        
        return response


    def send_data(self, data):   
        """Send a command to the Gripper - the method takes a list of uint8 as an argument.\n
        The meaning of each variable depends on the Gripper model (see support.robotiq.com for more details)"""

        # Make sure data has an even number of elements   
        if(len(data) % 2 == 1):
            data.append(0)   
        
        # Initiate message as an empty list
        message = []    
        
        # Fill message by combining two bytes in one register
        for i in range(0, int(len(data)/2)):
            message.append((data[2*i] << 8) + data[2*i+1])
        
        # print(f"write_registers({message})") # Debug  
        with self.lock:
            self.client.write_registers(0, message)


    def output_registers_msg_to_list(self, output_registers_msg):
        '''
        Class function converts given Robotiq2FOutput msg to a list\n
        List example: [byte_0_int, 0, 0, rPRA, rSPA, rFRA]\n
        byte0: "00{rARD}{rATR}{rGTO}00{rACT}"
        '''
        
        rACT = output_registers_msg.r_act # Activation
        rARD = output_registers_msg.r_ard # * Auto relase direction
        rGTO = output_registers_msg.r_gto # Go to pos
        rATR = output_registers_msg.r_atr # Auto release
        
        byte_0_bits = f"00{rARD}{rATR}{rGTO}00{rACT}" # * Changed to follow 2f format [2 bits - Reserved, rARD, rATR, rGTO, 2 bits - Reserved, rACT]
        byte_0_int = int(byte_0_bits, base=2)
        
        rPRA = output_registers_msg.r_pra # Target pos
        rSPA = output_registers_msg.r_spa # Grip speed
        rFRA = output_registers_msg.r_fra # Grip force
        
        output_registers_list = [byte_0_int, 0, 0, rPRA, rSPA, rFRA]
        
        return output_registers_list


    def read_input_registers(self, numBytes=4):
        '''
        Class function for reading input registers from gripper and publishing this to the input register topic using the Robotiq3FGripperInputRegisters message type
        '''
        
        numRegs = int(math.ceil(numBytes/2))

        with self.lock:
            response = self.client.read_input_registers(0,numBytes)
        
        response_byte_array = []

        for i in range(0, numRegs): # Splits the 16 bit registers from pymodbus into 2x 8 bit registers (uint8) 
            response_byte_array.append((response.getRegister(i) & 0xFF00) >> 8)
            response_byte_array.append(response.getRegister(i) & 0x00FF)
            
        
        # Setting Gripper status register
        response_byte0_bit_string = format(response_byte_array[0], '08b') # Format int to 8 bits
        
        # * Notice that bits 5 & 6 are not present, they are reserved by the gripper
        self.input_registers.g_act = int(response_byte0_bit_string[7], base=2)   # gACT ->       Initialization status       -> 1 = Gripper activation
        self.input_registers.g_gto = int(response_byte0_bit_string[4], base=2)   # gGTO -> Activation and mode change status -> 11 = Done and ready
        self.input_registers.g_sta = int(response_byte0_bit_string[2:4], base=2) # gIMC -> Activation and mode change status -> 11 = Done and ready
        self.input_registers.g_obj = int(response_byte0_bit_string[0:2], base=2) # gSTA ->           Motion status           -> 11 = Completed successfully
        
        # Setting Position request echo register
        self.input_registers.g_pr = response_byte_array[3]

        # * Setting Actual Position request echo register
        self.input_registers.g_po = response_byte_array[4]

        # * Setting Current request echo register
        self.input_registers.g_cu = response_byte_array[5]
        
        # Publish input registers to the topic: /Robotiq3FGripper/InputRegisters
        self._input_register_pub.publish(self.input_registers)













    def shutdown_callback(self):
        self.get_logger().warn("Shutting down...")


def main(args=None):
    rclpy.init(args=args)

    # Instansiate node class
    control_service_server_node = GripperServiceServer()

    # Create executor
    executor = MultiThreadedExecutor()
    executor.add_node(control_service_server_node)

    
    try:
        # Run executor
        executor.spin()
        
    except KeyboardInterrupt:
        pass
    
    finally:
        # Shutdown executor
        control_service_server_node.shutdown_callback()
        executor.shutdown()




if __name__ == "__main__":
    main()