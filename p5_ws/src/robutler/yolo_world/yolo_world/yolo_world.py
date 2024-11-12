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
