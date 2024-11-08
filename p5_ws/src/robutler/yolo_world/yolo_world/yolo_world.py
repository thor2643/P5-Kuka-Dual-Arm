#Yolo World
from ultralytics import YOLOWorld    #pip install ultralytics

#Image processing
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

#ROS NODE
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image   #, CameraInfo

class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')
        
        # Create a subscriber to the topic you want to read from
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/aligned_depth_to_color/image_raw',  # Topic name
            self.listener_callback_depth,  # Callback function
            10  # Queue size
        )
        
        
         # Create a subscriber to the topic you want to read from
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/color/image_raw',  # Topic name
            self.listener_callback_color,  # Callback function
            10  # Queue size
        )
        
        
        self.subscription  # Prevent unused variable warning
        self.bridge = CvBridge()  # Initialize CvBridge here

        

    def listener_callback_depth(self, msg):
        try:
            # Convert the ROS Image message to OpenCV image (16-bit single-channel)
            depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

            if True: #True: gets a tresholded colormap. False all depth data are used in normalisation
                # Define the depth range (in millimeters) to display
                min_depth = 0  # Minimum depth to display (e.g., 500 mm)
                max_depth = 6000  # Maximum depth to display (e.g., 2000 mm)

                # 1. Threshold the depth image to the specified range
                # Set values outside the range to zero (or another placeholder value)
                depth_img = np.where((depth_img >= min_depth) & (depth_img <= max_depth),depth_img, 0)
            
            # Optionally normalize depth values to a range [0,255] for visualization
            img_normalized = cv2.normalize(depth_img, None, 0, 255, cv2.NORM_MINMAX)

            # Convert the 16-bit depth image to 8-bit for visualization
            img_8bit = np.uint8(img_normalized)
            img_8bit = cv2.applyColorMap(img_8bit, cv2.COLORMAP_JET)

            # Display the image
            cv2.imshow("Depth Image", img_8bit)
            cv2.waitKey(1)  # Refresh the window

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting image: {e}')


        return depth_img, img_8bit  #The first is the actual depth data, the second is for display

    def listener_callback_color(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            color_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR by default)
            color_img_bgr = cv2.cvtColor(color_img, cv2.COLOR_RGB2BGR)

            #Apply yolo world
            self.apply_yolo_world(color_img_bgr)

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting color image: {e}')

        return color_img  # Return the actual color image data if needed elsewhere in the program

    def apply_yolo_world(self, img):
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes

        # Define custom classes
        if False: 
            model.set_classes(["brick", "lego", "laptop"])

        # Execute inference with the YOLOv8s-world model on the specified image
        results = model.predict(img)

        # Convert the result to an OpenCV-compatible format and display it
        result_image = results[0].plot()  # plot() returns an image array with annotations

        # Display the image in a single window
        cv2.imshow("YOLO Detection", result_image)  # Window name "YOLO Detection" remains consistent
        cv2.waitKey(1)  # Small delay to allow window to refresh
        


def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


####################################slet herefter når færdig
"""
class RealSenseCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Enable color stream
        self.config.enable_stream(
            rs.stream.color, 1280, 720, rs.format.bgr8, 30
        )

        # Enable depth stream
        self.config.enable_stream(
            rs.stream.depth, 1280, 720, rs.format.z16, 30
        )

        # Reset the camera to default settings (avoids an error when starting the pipeline)
        ctx = rs.context()
        devices = ctx.query_devices()
        for dev in devices:
            dev.hardware_reset()
        print("reset done")

        # Placeholder for calibrated values
        self.calibrated_exposure = 166
        self.calibrated_white_balance = 4600

    def calibrate_camera(self):
        # Start the pipeline temporarily for calibration
        self.pipeline.start(self.config)

        # Alignment setup
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)

        # Access the color sensor
        color_sensor = self.pipeline.get_active_profile().get_device().query_sensors()[1]

        # Enable auto-exposure and auto-white-balance
        color_sensor.set_option(rs.option.enable_auto_exposure, 1)
        color_sensor.set_option(rs.option.enable_auto_white_balance, 1)

        # Allow time for auto-exposure and auto-white-balance to stabilize
        for _ in range(30):
            frames = self.pipeline.wait_for_frames()

        # Retrieve and store the settled values
        self.calibrated_exposure = color_sensor.get_option(rs.option.exposure)
        self.calibrated_white_balance = color_sensor.get_option(rs.option.white_balance)
        
        print(f"Calibrated exposure: {self.calibrated_exposure}")
        print(f"Calibrated white balance: {self.calibrated_white_balance}")

        # Stop the pipeline after calibration
        self.pipeline.stop()
        
    def __enter__(self):
        self.pipeline.start(self.config)

        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)

        color_sensor = self.pipeline.get_active_profile().get_device().query_sensors()[1]

         # If calibrated values exist, apply them
        if self.calibrated_exposure and self.calibrated_white_balance:
            color_sensor.set_option(rs.option.enable_auto_exposure, 0)
            color_sensor.set_option(rs.option.enable_auto_white_balance, 0)
            color_sensor.set_option(rs.option.exposure, self.calibrated_exposure)
            color_sensor.set_option(rs.option.white_balance, self.calibrated_white_balance)
        else:
            # If no calibrated values are present, enable auto settings
            color_sensor.set_option(rs.option.enable_auto_exposure, 1)
            color_sensor.set_option(rs.option.enable_auto_white_balance, 1)

        return self.pipeline

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipeline.stop()
"""
