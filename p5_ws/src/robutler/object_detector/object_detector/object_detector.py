#Yolo World
from ultralytics import YOLOWorld    #pip install ultralytics

#Image processing
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import json
import os



#ROS stuff
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import DefineObjectInfo
from geometry_msgs.msg import Point
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo



#the following is the ros2 launch command for the realsense camera with user settings
"""
ros2 launch realsense2_camera rs_launch.py 

If you want to chance any parameters do it in the launch file. and remember to colcon build the package after you have made the changes.

"""



class RealSenseCamera(Node):
    def __init__(self):
        super().__init__('my_subscriber_node')
        
        # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/aligned_depth_to_color/image_raw',  # Topic name
            self.convert_to_depth_img,  # Callback function
            10  # Queue size
        )
        
         # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            Image,  # Message type
            '/camera/camera/color/image_raw',  # Topic name
            self.convert_to_color_img,  # Callback function
            10  # Queue size
        )

         # Create a subscriber to the topic 
        self.subscription = self.create_subscription(
            CameraInfo,  # Message type
            '/camera/camera/aligned_depth_to_color/camera_info',  # Topic name
            self.camera_info_callback,  # Callback function
            10  # Queue size
        )
        
        self.subscription  # Prevent unused variable warning
        self.bridge = CvBridge()  

        #Image frames for depth and color
        self.color_img = None
        self.depth_img = None
        self.camera_info = None

        
    def convert_to_depth_img(self, msg):
        try:
            # Convert the ROS Image message to OpenCV image (16-bit single-channel)
            self.depth_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting image: {e}')

    def convert_to_color_img(self, msg):
        try:
            # Convert the ROS Image message to an OpenCV image
            color_img_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
            
            # Convert RGB to BGR for OpenCV display (OpenCV uses BGR by default)
            self.color_img = cv2.cvtColor(color_img_rgb, cv2.COLOR_RGB2BGR)

        except CvBridgeError as e:
            self.get_logger().error(f'Error converting color image: {e}')

    def camera_info_callback(self, msg):
        self.camera_info = msg.k


class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.detector_srv = self.create_service(GetObjectInfo, 'get_object_info', self.get_object_information)
        self.threshold_adjust_srv = self.create_service(DefineObjectInfo, 'define_object_info', self.define_object_thresholds)
        self.yolo_world_srv = self.create_service(GetObjectInfo, 'get_object_info_yolo', self.get_object_information_yolo)

        self.image_publisher = self.create_publisher(Image, 'video_frames', 10)

        # Instantiate the RealSenseCamera object
        self.realsense_camera = RealSenseCamera()

        self.object_file = 'src/robutler/object_detector/object_detector/lego_bricks_config.json'

        # Dictionary to store object detection descriptions e.g. color range, size range
        self.lego_bricks = {}
        self.load_object_descriptions() #Loads json file with saved descriptions into lego bricks

        # Create a dictionary to store found objects with relevant information
        self.found_objects = {}

        #Frames for depth and color
        self.depth_frame = None   
        self.color_frame = None
        self.camera_info = None
        self.yolo_results = None

        # Publish initial image to GUI
        self.retrieve_aligned_frames()
        image = self.get_color_image()
        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(cv2.rotate(image, cv2.ROTATE_180)))


    def retrieve_aligned_frames(self):      
        # Retrieve aligned frames from the RealSense camera by spinning the node untill new frames are available

        while self.realsense_camera.depth_img is None or self.realsense_camera.color_img is None or self.realsense_camera.camera_info is None:
                rclpy.spin_once(self.realsense_camera)

        while np.array_equal(self.realsense_camera.depth_img, self.depth_frame) or np.array_equal(self.realsense_camera.color_img, self.color_frame):
                rclpy.spin_once(self.realsense_camera)
        
        self.depth_frame = self.realsense_camera.depth_img
        self.color_frame = self.realsense_camera.color_img
        self.camera_info = self.realsense_camera.camera_info
        
        
    
    #The callback function for the detector service
    def get_object_information(self, request, response):
        object = request.object_name
        self.get_logger().info(f'Requested to find {object}\n')

        self.found_objects.clear()

        if object in self.lego_bricks:
            self.retrieve_aligned_frames()

            image = self.get_color_image()
            _, rotated_bounding_boxes, _ = self.find_object(image, object)

            image_with_bbx = self.draw_rotated_boxes(image.copy(), rotated_bounding_boxes)
            image_with_bbx = cv2.rotate(image_with_bbx, cv2.ROTATE_180)

            response.object_count = len(self.found_objects)

            img_x = self.color_frame.shape[1]
            img_y = self.color_frame.shape[0]

            for i, obj in enumerate(self.found_objects):
                point = Point()
                point.x = float(self.found_objects[obj]['center_coords'][0])
                point.y = float(self.found_objects[obj]['center_coords'][1])
                point.z = float(self.found_objects[obj]['center_coords'][2])

                response.centers.append(point)
                response.orientations.append(self.found_objects[obj]['rotated_rect'][2])

                if self.found_objects[obj]['width'] is not None:
                    response.grasp_widths.append(self.found_objects[obj]['width'])
                else:
                    response.grasp_widths.append(0)

                # Extract the x, y couple from rotated_bounding_boxes with the highest y value
                print(rotated_bounding_boxes)

                point_idx = np.argmax([point[1] for point in rotated_bounding_boxes[i]])

                image_with_bbx =cv2.putText(
                                    image_with_bbx, 
                                    obj,                #object name
                                    (img_x-rotated_bounding_boxes[i][point_idx][0], img_y-rotated_bounding_boxes[i][point_idx][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA
                                )

            self.get_logger().info(f'Found {response.object_count} {object}\n')

            self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image_with_bbx))

            print("I have moved on")

            # Clear the found objects dictionary
            self.found_objects.clear()
        else:
            self.get_logger().info('Object thresholds not available. Consider adding the object by running the adjust_hsv option at startup.\n')
            response.object_count = 0

        print("I am now returning")
        return response
    
    
    #The callback function for the detector service
    def get_object_information_yolo(self, request, response):
        object = request.object_name
        self.get_logger().info(f'Requested to find {object} with Yolo World\n')

        self.retrieve_aligned_frames()
        image = self.get_color_image()
        image = cv2.rotate(image, cv2.ROTATE_180)

        #Apply Yolo World, data is stored in self.yolo_results
        self.apply_yolo_world(image, object, verbose=False)

        if len(self.yolo_results[0].boxes.data) == 0:
            self.get_logger().info(f'No {object} found\n')
            self.apply_yolo_world(image, object, verbose=False, name_objects = True)
            image = self.yolo_results[0].plot()
            self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image))
            response.object_count = 0
            return response

        for i in range(len(self.yolo_results[0].boxes.data)):
            x_min, y_min, x_max, y_max, _, _ = self.yolo_results[0].boxes.data[i]  #confidence and class
            response.object_count += 1
            cartesian_coordinates = self.get_cartesian_coordinates(int((x_min + x_max) / 2), int((y_min + y_max) / 2))
            print(cartesian_coordinates)
            print(type(cartesian_coordinates))
            point = Point()
            point.x = float(cartesian_coordinates[0])
            point.y = float(cartesian_coordinates[1])
            point.z = float(cartesian_coordinates[2])
            response.centers.append(point)
            response.orientations.append(0)
            response.grasp_widths.append(min(x_max - x_min, y_max - y_min))
 

        image_with_bbx = self.yolo_results[0].plot()

        self.get_logger().info(f'Found {response.object_count} {object}\n')

        self.image_publisher.publish(self.realsense_camera.bridge.cv2_to_imgmsg(image_with_bbx))
            
        return response
    
    # The callback function for the threshold adjust service    
    def define_object_thresholds(self, request, response):
        object = request.object_name
        self.get_logger().info(f'Requested to define {object}\n')

        # Get Image
        self.retrieve_aligned_frames()
        image = self.get_color_image()

        if image is None:
            self.get_logger().info("Failed to capture image from camera.")
            response.success = False
            return response
            
        #Manually adjust the HSV thresholds and size range
        lower_bound, upper_bound, min_size, max_size = self.adjust_hsv_and_size_thresholds(image, object)
        self.get_logger().info(f"Lower Bound: {lower_bound}")
        self.get_logger().info(f"Upper Bound: {upper_bound}")
        self.get_logger().info(f"Min Size: {min_size}")
        self.get_logger().info(f"Max Size: {max_size}")

        response.success = True

        return response
   
    def show_depth_map(self):
        cv2.namedWindow("Depth Map", cv2.WINDOW_AUTOSIZE)

        while True:
            self.retrieve_aligned_frames()

            # Convert the depth frame to a NumPy array
            depth_image = np.asanyarray(self.depth_frame)

            #depth_image = cv2.rotate(depth_image, cv2.ROTATE_180)

            if True: #True: gets a tresholded colormap. False all depth data are used in normalisation
                # Define the depth range (in millimeters) to display
                min_depth = 0  # Minimum depth to display  0 m
                max_depth = 3000  # Maximum depth to display 3m

                # 1. Threshold the depth image to the specified range
                # Set values outside the range to 0 (this can be chanced if needed).
                depth_image = np.where((depth_image >= min_depth) & (depth_image <= max_depth),depth_image, 0)

            # Normalize the depth image for display
            depth_image = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)
            depth_image = np.uint8(depth_image)

            # Apply a colormap to the depth image
            depth_colormap = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            # Show the depth map using OpenCV's imshow
            cv2.imshow("Depth Map", depth_colormap)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        cv2.destroyAllWindows()
        
    def show_frame(self):
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
        while True:
            self.retrieve_aligned_frames()

            # Convert the frame to a NumPy array for OpenCV
            color_frame = self.get_color_image()

            # Show the frame using OpenCV's imshow
            cv2.imshow("Image", cv2.rotate(color_frame, cv2.ROTATE_180))

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def get_color_image(self):
        return np.asanyarray(self.color_frame)

    def show_image(self, image):
        cv2.imshow("Image", cv2.rotate(image, cv2.ROTATE_180))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def apply_yolo_world(self, img, object_name, name_objects = False, verbose = False):
        model = YOLOWorld("yolov8l-world.pt")  # or select yolov8{s/m/l}-world.pt for different sizes

        if name_objects == False:
            model.set_classes([object_name])

        # Execute inference with the YOLOv8l-world model on the specified image
        self.yolo_results = model.predict(img)

        #the following prints the results of the yolo model without the class contrains
        if name_objects:
            objects_found = []
            for i in range(len(self.yolo_results[0].boxes.data)):
                objects_found.append(model.names[int(self.yolo_results[0].boxes.data[i][5])])

            self.get_logger().info(f'No {object_name} were found, but a {objects_found} was located.\n')

    def find_object(self, image, object_name):
        # Get features from dictionary
        object_features = self.lego_bricks.get(object_name)

        if not object_features:
            print(f"Object {object_name} not found in dictionary.")
            return None

        color_lower = np.array(object_features['color_range'][0], dtype=np.uint8)
        color_upper = np.array(object_features['color_range'][1], dtype=np.uint8)
        size_min, size_max = object_features['size_range']

        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Threshold the image to get only selected color
        mask = cv2.inRange(hsv, color_lower, color_upper)


        # Morphological operations to remove small noise and fill gaps
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        # Find contours (or blobs)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Lists to store bounding boxes
        rotated_bounding_boxes = []
        bounding_boxes = []

        i=0
        for contour in contours:
            # Calculate area to filter by size
            area = cv2.contourArea(contour)

            if size_min < area < size_max:
                # Get the bounding box for the contour
                x, y, w, h = cv2.boundingRect(contour)
                bounding_boxes.append((x, y, x + w, y + h))

                # Get the minimum area rectangle for the contour
                rect = cv2.minAreaRect(contour) # returns ((center_x, center_y), (width, height), angle)
                box = cv2.boxPoints(rect)       # returns the four vertices of the rectangle
                box = np.int0(box)
                rotated_bounding_boxes.append(box)

                self.found_objects[f"{object_name}_{i+1}"] = {'bounding_box': (x, y, x + w, y + h), 
                                                            'rotated_bounding_box': box, 
                                                            'rotated_rect': rect}

                # Get the center of the bounding box from the rect variable
                center_x, center_y = int(rect[0][0]), int(rect[0][1])

                # Retrieve the world coordinates of the center
                center_coordinates = self.get_cartesian_coordinates(center_x, center_y)

                if center_coordinates is not None:
                    # Add center coordinates to the dictionary
                    self.found_objects[f"{object_name}_{i+1}"].update({'center_coords': center_coordinates})
                else:
                    print("Failed to calculate center coordinates of the object.")

                width_point_1, width_point_2 = box[0], box[1] 
                height_point_1, height_point_2 = box[1], box[2]

                width_point_1_metric = self.get_cartesian_coordinates(width_point_1[0], width_point_1[1])
                width_point_2_metric = self.get_cartesian_coordinates(width_point_2[0], width_point_2[1])
                height_point_1_metric = self.get_cartesian_coordinates(height_point_1[0], height_point_1[1])
                height_point_2_metric = self.get_cartesian_coordinates(height_point_2[0], height_point_2[1])

                
                if width_point_1_metric is not None and width_point_2_metric is not None and height_point_1_metric is not None and height_point_2_metric is not None:
                    # Calculate the width of the bounding box
                    width = np.linalg.norm(width_point_1_metric[:2] - width_point_2_metric[:2])
                    height = np.linalg.norm(height_point_1_metric[:2] - height_point_2_metric[:2])

                    # Add width and height of object to the dictionary
                    self.found_objects[f"{object_name}_{i+1}"].update({'width': width, 'height': height})
                else:
                    self.found_objects[f"{object_name}_{i+1}"].update({'width': None, 'height': None})
                    print("Failed to calculate width and height of the object.")

                
                # Consider using this to distinguish between different objects
                #aspect_ratio = min(width, height) / max(width, height)

                
                i += 1

        # Consider implementing the conversion from pixel to world coordinates here
        # Use the method shown in the link below to calibrate the camera and get the intrinsic parameters
        # https://www.fdxlabs.com/calculate-x-y-z-real-world-coordinates-from-a-single-camera-using-opencv/
                

        # Return list of bounding boxes for the detected object as well as the mask
        return bounding_boxes, rotated_bounding_boxes, mask

    def draw_rotated_boxes(self, image, rotated_bounding_boxes):
        for box in rotated_bounding_boxes:
            cv2.drawContours(image, [box], 0, (0, 0, 255), 2)
        return image

    def draw_boxes(self, image, bounding_boxes):
        for box in bounding_boxes:
            cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        return image
    
    # Function to create trackbars for adjusting HSV thresholds and size range
    def adjust_hsv_and_size_thresholds(self, image, object_name=None):
        def nothing(x):
            pass

        # Create a button to save the new object and its boundaries
        def save_object(x):
            self.save_object_descriptions()
            print(f"Object {object_name} and its boundaries have been saved.")
            self.close_windows = True

        self.close_windows = False

        if object_name is None:
            # Ask user for object name
            object_name = input("Enter the name of the object you want to adjust: ")
        
        if object_name not in self.lego_bricks:
            # If the object is not already in the dictionary, initialize it with default values
            self.lego_bricks[object_name] = {'color_range': ([0, 0, 0], [255, 255, 255]), 'size_range': (500, 2000)}

        # Create a window
        cv2.namedWindow('Trackbars')
        
        # Create trackbars for lower and upper HSV values
        cv2.createTrackbar('Lower H', 'Trackbars', self.lego_bricks[object_name]['color_range'][0][0], 255, nothing)
        cv2.createTrackbar('Lower S', 'Trackbars', self.lego_bricks[object_name]['color_range'][0][1], 255, nothing)
        cv2.createTrackbar('Lower V', 'Trackbars', self.lego_bricks[object_name]['color_range'][0][2], 255, nothing)
        cv2.createTrackbar('Upper H', 'Trackbars', self.lego_bricks[object_name]['color_range'][1][0], 255, nothing)
        cv2.createTrackbar('Upper S', 'Trackbars', self.lego_bricks[object_name]['color_range'][1][1], 255, nothing)
        cv2.createTrackbar('Upper V', 'Trackbars', self.lego_bricks[object_name]['color_range'][1][2], 255, nothing)
        
        # Create trackbars for minimum and maximum size
        cv2.createTrackbar('Min Size', 'Trackbars', self.lego_bricks[object_name]['size_range'][0], 10000, nothing)
        cv2.createTrackbar('Max Size', 'Trackbars', self.lego_bricks[object_name]['size_range'][1], 10000, nothing)

        cv2.createTrackbar('Save Object descriptions', 'Trackbars', 0, 1, save_object)

        while True:
            # Get the current positions of trackbars
            lower_h = cv2.getTrackbarPos('Lower H', 'Trackbars')
            lower_s = cv2.getTrackbarPos('Lower S', 'Trackbars')
            lower_v = cv2.getTrackbarPos('Lower V', 'Trackbars')
            upper_h = cv2.getTrackbarPos('Upper H', 'Trackbars')
            upper_s = cv2.getTrackbarPos('Upper S', 'Trackbars')
            upper_v = cv2.getTrackbarPos('Upper V', 'Trackbars')
            min_size = cv2.getTrackbarPos('Min Size', 'Trackbars')
            max_size = cv2.getTrackbarPos('Max Size', 'Trackbars')

            # Update the lego_bricks dictionary with current values
            self.lego_bricks[object_name]['color_range'] = ([lower_h, lower_s, lower_v], [upper_h, upper_s, upper_v])
            self.lego_bricks[object_name]['size_range'] = (min_size, max_size)

            # Use find_object to get bounding boxes with the current settings
            bounding_boxes, rotated_bounding_boxes, mask = self.find_object(image, object_name)

            # Apply mask to the original image using the current HSV range
            lower_bound = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
            upper_bound = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)

            result = cv2.bitwise_and(image, image, mask=mask)

            # Draw rectangles showing selected HSV range and size bounds
            color_lower = cv2.cvtColor(np.uint8([[lower_bound]]), cv2.COLOR_HSV2BGR)[0][0]
            color_upper = cv2.cvtColor(np.uint8([[upper_bound]]), cv2.COLOR_HSV2BGR)[0][0]

            # Calculate side length of the squares based on the size bounds
            min_side = int(np.sqrt(min_size))
            max_side = int(np.sqrt(max_size))

            # Draw rectangles to represent the lower and upper bounds visually
            cv2.rectangle(result, (10, 10), (10 + min_side, 10 + min_side), color_lower.tolist(), -1)
            cv2.rectangle(result, (130, 10), (130 + max_side, 10 + max_side), color_upper.tolist(), -1)

            # Draw bounding boxes on the result image
            image_copy = image.copy()
            result_with_boxes = self.draw_boxes(image_copy, bounding_boxes)
            result_with_boxes = self.draw_rotated_boxes(result_with_boxes, rotated_bounding_boxes)

            # Show the resulting image
            cv2.imshow('Image with Bounding Boxes', cv2.rotate(result_with_boxes, cv2.ROTATE_180))
            cv2.imshow('The Masked Image', cv2.rotate(result, cv2.ROTATE_180))  

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q') or self.close_windows:
                break

        # Clean up
        cv2.destroyAllWindows()

        # Return the final selected thresholds and size range
        return lower_bound, upper_bound, min_size, max_size

    def get_cartesian_coordinates(self, pixel_x, pixel_y):
        # The camera info message .K contains the camera intrinsics
        #[ fx   0  cx ]
        #[  0  fy  cy ]
        #[  0   0   1 ]

        # Get the camera intrinsics
        fx = self.camera_info[0]
        fy = self.camera_info[4]
        cx = self.camera_info[2]
        cy = self.camera_info[5]

        if pixel_x < 0 or pixel_x >= self.depth_frame.shape[1] or pixel_y < 0 or pixel_y >= self.depth_frame.shape[0]:
            print("Pixel coordinates out of bounds.")
            return None
        
        if self.depth_frame[pixel_y, pixel_x] == 0:
            print("No depth data available at the selected pixel.")
            return None

        print(f"size of depth frame: {self.depth_frame.shape}")

        # Calculate the x, y, z coordinates
        z = self.depth_frame[pixel_y, pixel_x] / 1000  # Convert to meters
        x = ((pixel_x - cx) * z / fx) 
        y = ((pixel_y - cy) * z / fy) 
        

        return np.array([x, y, z])
        
    def show_cartesian_coordinates(self):
        self.retrieve_aligned_frames()
        color_image = self.get_color_image()

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                # Adjust the x, y coordinates to reflect a rotated image
                height, width, _ = color_image.shape
                adjusted_x = width - x
                adjusted_y = height - y
                coordinates = self.get_cartesian_coordinates(adjusted_x, adjusted_y)
                if coordinates is not None:
                    print(f"Cartesian coordinates at ({x}, {y}): {coordinates}")

        cv2.namedWindow("Image with Coordinates")
        cv2.setMouseCallback("Image with Coordinates", mouse_callback)

    
        while True:
            cv2.imshow("Image with Coordinates", cv2.rotate(color_image, cv2.ROTATE_180))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def load_object_descriptions(self):
        if os.path.exists(self.object_file):
            with open(self.object_file, 'r') as file:
                self.lego_bricks = json.load(file)
        else:
            print("No object descriptions found. Creating a new file.")
            self.save_object_descriptions()

    def save_object_descriptions(self):
        with open(self.object_file, 'w') as file:
            json.dump(self.lego_bricks, file, indent=4)

    def test_precision_recall(self):
        def nothing(x):
            pass

        # Load the object descriptions
        self.load_object_descriptions()

        # Base directory for saving test images
        base_dir = "test_results"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Find the next available test number
        test_numbers = [int(d.split('_')[1]) for d in os.listdir(base_dir) if d.startswith("test_")]
        test_number = max(test_numbers, default=0) + 1  # Increment the highest test number or start at 1

        # Create a folder for this test run
        test_dir = os.path.join(base_dir, f"test_{test_number}")
        os.makedirs(test_dir)

        print(f"Saving test results in: {test_dir}")

        # Dictionary to store metrics for each color
        results = {}

        # Loop through each brick color in the config file
        for brick_color, features in self.lego_bricks.items():
            print(f"Testing for {brick_color}...")

            # Create a subdirectory for the brick color
            color_dir = os.path.join(test_dir, brick_color)
            if not os.path.exists(color_dir):
                os.makedirs(color_dir)

            self.retrieve_aligned_frames()
            image = self.get_color_image()

            if image is None:
                print(f"Failed to capture image from camera for {brick_color}.")
                continue

            # Detect objects
            bounding_boxes, rotated_bounding_boxes, _ = self.find_object(image, brick_color)

            # Debugging: Check if bounding boxes are detected
            if not bounding_boxes:
                print(f"No bounding boxes detected for {brick_color}.")
                results[brick_color] = {
                    "True Positives": 0,
                    "False Positives": 0,
                    "False Negatives": 10,
                    "Precision": 0.0,
                    "Recall": 0.0,
                }
                continue

            # Draw bounding boxes on the image
            try:
                image_with_boxes = self.draw_boxes(image.copy(), bounding_boxes)
                image_with_boxes = self.draw_rotated_boxes(image_with_boxes, rotated_bounding_boxes)
            except Exception as e:
                print(f"Error drawing bounding boxes: {e}")
                continue

            # DEBUGGING: Save the image with bounding boxes for later analysis
            """
            debug_path = os.path.join(color_dir, f"{brick_color}_debug.png")
            cv2.imwrite(debug_path, cv2.rotate(image_with_boxes, cv2.ROTATE_180))
            print(f"Debug image saved at {debug_path}.")
            """
            
            # Create a window with sliders
            window_name = f"Testing {brick_color}"
            cv2.namedWindow(window_name)

            # Add sliders
            cv2.createTrackbar("False Positives", window_name, 0, 10, nothing)
            cv2.createTrackbar("False Negatives", window_name, 0, 10, nothing)
            cv2.createTrackbar("Send Data", window_name, 0, 1, nothing)

            while True:
                # Display the image with bounding boxes
                cv2.imshow(window_name, cv2.rotate(image_with_boxes, cv2.ROTATE_180))

                # Read the slider values
                false_positives = cv2.getTrackbarPos("False Positives", window_name)
                false_negatives = cv2.getTrackbarPos("False Negatives", window_name)
                send_data = cv2.getTrackbarPos("Send Data", window_name)

                # If "Send Data" slider is set to 1, capture data and move to next
                if send_data == 1:
                    true_positives = len(bounding_boxes) - false_positives
                    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
                    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

                    # Save results for the current color
                    results[brick_color] = {
                        "True Positives": true_positives,
                        "False Positives": false_positives,
                        "False Negatives": false_negatives,
                        "Precision": precision,
                        "Recall": recall,
                    }

                    # Save the image with precision/recall in the filename
                    image_filename = f"{brick_color}_precision_{precision:.2f}_recall_{recall:.2f}.png"
                    image_path = os.path.join(color_dir, image_filename)
                    cv2.imwrite(image_path, cv2.rotate(image_with_boxes, cv2.ROTATE_180))
                    print(f"Saved detection image for {brick_color} at {image_path}.")

                    # Reset "Send Data" slider and close the window
                    cv2.setTrackbarPos("Send Data", window_name, 0)
                    cv2.destroyWindow(window_name)
                    break

                # Add a short wait to allow OpenCV to process events
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("User exited.")
                    cv2.destroyAllWindows()
                    return

        # Save all results to a summary file and CSV
        summary_path = os.path.join(test_dir, "summary.txt")
        csv_path = os.path.join(test_dir, "results.csv")
        with open(summary_path, "w") as summary_file:
            summary_file.write("Precision and Recall per Brick Color:\n")
            for color, metrics in results.items():
                summary_file.write(f"{color}: {metrics}\n")

        import pandas as pd
        df = pd.DataFrame.from_dict(results, orient="index")
        df.to_csv(csv_path, index_label="Brick Color")
        print(f"Saved summary at {summary_path}")
        print(f"Saved results CSV at {csv_path}")

        print("Test completed!")


    def get_user_input(self, prompt):
        """
        Use console input instead of GUI input for simplicity.
        """
        while True:
            try:
                user_input = int(input(prompt))
                return user_input
            except ValueError:
                print("Invalid input. Please enter a number.")

    def save_image(self, save_folder="captured_images"):
        """
        Captures and saves an image in a specified folder with an incremented filename.
        """
        # Ensure the save folder exists
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Retrieve the current frame
        self.retrieve_aligned_frames()
        image = self.get_color_image()

        if image is None:
            print("Failed to capture image from camera.")
            return

        # Find the next available file name
        existing_files = [f for f in os.listdir(save_folder) if f.endswith(".jpg")]
        next_index = len(existing_files) + 1
        file_name = f"image_{next_index}.jpg"
        file_path = os.path.join(save_folder, file_name)

        # Save the image
        cv2.imwrite(file_path, cv2.rotate(image, cv2.ROTATE_180))  # Rotate if needed
        print(f"Image saved: {file_path}")


def main(args=None):
    rclpy.init(args=args)

    # Create an ObjectDetector instance
    detector = ObjectDetector()


    #this was commented out
    rclpy.spin(detector) 

    # Insert the code snippet below to run the node with a menu
    """
    while True:
        # Ask use which function to run
        print("\nChoose a function to run:")
        print("1. Show Frame")
        print("2. Find Object using traditional vision techniques")
        print("3. find Object using YOLO")
        print("4. Adjust HSV and Size Thresholds")
        print("5. Show Depth Map")
        print("6. Print Cartesian Coordinates")
        print("7. Spin the node")
        print("8. Calibrate Camera")
        print("9. Test Precision and Recall")
        print("10. Take raw image")
        print("11. Exit\n")
       

        choice = input("Enter your choice: ")


        if choice == '1':
            #Show the current frame from the camera
            detector.show_frame()

        elif choice == '2':
            #Find an object in the image
            detector.retrieve_aligned_frames()
            image = detector.get_color_image()

            if image is None:
                print("Failed to capture image from camera.")
                continue

            #Find a specific object available in the dictionary
            object_name = input("Enter the name of the object you want to find: ")
            bounding_boxes, rotated_bounding_boxes, _ = detector.find_object(image, object_name)

            if bounding_boxes:
                print(f"{object_name} found in the image.")
                image_bbxs = detector.draw_boxes(image.copy(), bounding_boxes)
                image_bbxs = detector.draw_rotated_boxes(image_bbxs, rotated_bounding_boxes)
                detector.show_image(image_bbxs)
            else:
                print(f"{object_name} not found in the image.")


        elif choice == '3': #YOLO
            #Find an object in the image
            detector.retrieve_aligned_frames()
            image = detector.get_color_image()

            if image is None:
                print("Failed to capture image from camera.")
                continue

            detector.apply_yolo_world(image)

        elif choice == '4':
            detector.retrieve_aligned_frames()
            image = detector.get_color_image()

            if image is None:
                print("Failed to capture image from camera.")
                continue

            #Manually adjust the HSV thresholds and size range
            lower_bound, upper_bound, min_size, max_size = detector.adjust_hsv_and_size_thresholds(image)
            print(f"Lower Bound: {lower_bound}")
            print(f"Upper Bound: {upper_bound}")
            print(f"Min Size: {min_size}")
            print(f"Max Size: {max_size}")

        elif choice == '5':
            detector.show_depth_map()

        elif choice == '6':
            
            detector.show_cartesian_coordinates()

        elif choice == '7':
            rclpy.spin(detector) 

        elif choice == '8':
            detector.realsense_camera.calibrate_camera()               

        elif choice == '9':
            detector.test_precision_recall()

        elif choice == '10':
            detector.save_image()

        elif choice == '11':
            break

        else:
            print("Invalid choice. Please try again.")
    """

    rclpy.shutdown()


if __name__ == '__main__':
    main()