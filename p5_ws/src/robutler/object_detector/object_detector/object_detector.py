import rclpy
from rclpy.node import Node
import pyrealsense2 as rs
import cv2
import numpy as np
import json
import os
import time

#ROS stuff
from project_interfaces.srv import GetObjectInfo
from project_interfaces.srv import DefineObjectInfo
from geometry_msgs.msg import Point


class RealSenseCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Enable color stream
        self.config.enable_stream(
            rs.stream.color, 640, 480, rs.format.bgr8, 30
        )

        # Enable depth stream
        self.config.enable_stream(
            rs.stream.depth, 640, 480, rs.format.z16, 30
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
      

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.detector_srv = self.create_service(GetObjectInfo, 'get_object_info', self.get_object_information)
        self.threshold_adjust_srv = self.create_service(DefineObjectInfo, 'define_object_info', self.define_object_thresholds)

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

    
    #The callback function for the detector service
    def get_object_information(self, request, response):
        object = request.object_name
        self.get_logger().info(f'Requested to find {object}\n')

        if object in self.lego_bricks:
            self.capture_aligned_frames()
            self.find_object(self.get_color_image(), object)

            response.object_count = len(self.found_objects)

            for obj in self.found_objects:
                point = Point()
                point.x = float(self.found_objects[obj]['center_coords'][0])
                point.y = float(self.found_objects[obj]['center_coords'][1])
                point.z = float(self.found_objects[obj]['center_coords'][2])

                response.centers.append(point)
                response.orientations.append(self.found_objects[obj]['rotated_rect'][2])
                response.grasp_widths.append(self.found_objects[obj]['width'])

            self.get_logger().info(f'Found {response.object_count} {object}\n')

            # Clear the found objects dictionary
            self.found_objects.clear()
        else:
            self.get_logger().info('Object thresholds not available. Consider adding the object by running the adjust_hsv option at startup.\n')
            response.object_count = 0

        return response
    
    # The callback function for the threshold adjust service    
    def define_object_thresholds(self, request, response):
        object = request.object_name
        self.get_logger().info(f'Requested to define {object}\n')

        # Get Image
        self.capture_aligned_frames()
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


    def capture_aligned_frames(self):
        with self.realsense_camera as cam:
            frames = cam.wait_for_frames()
            aligned_frames = self.realsense_camera.align.process(frames)

            # Retrieve the depth frame
            self.depth_frame = aligned_frames.get_depth_frame()
            self.color_frame = aligned_frames.get_color_frame()
            
            if not self.depth_frame or not self.color_frame:
                print("No depth or color frame captured.")
                

    def show_depth_map(self):
        cv2.namedWindow("Depth Map", cv2.WINDOW_AUTOSIZE)

        while True:
            self.capture_aligned_frames()

            # Convert the depth frame to a NumPy array
            depth_image = np.asanyarray(self.depth_frame.get_data())

            #depth_image = cv2.rotate(depth_image, cv2.ROTATE_180)

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
            self.capture_aligned_frames()

            # Convert the frame to a NumPy array for OpenCV
            color_frame = self.get_color_image()

            # Show the frame using OpenCV's imshow
            cv2.imshow("Image", cv2.rotate(color_frame, cv2.ROTATE_180))

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def get_color_image(self):
        #return cv2.rotate(np.asanyarray(self.color_frame.get_data()), cv2.ROTATE_180)
        return np.asanyarray(self.color_frame.get_data())

    def show_image(self, image):
        cv2.imshow("Image", cv2.rotate(image, cv2.ROTATE_180))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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

                self.found_objects[f"{object_name}_{i}"] = {'bounding_box': (x, y, x + w, y + h), 
                                                            'rotated_bounding_box': box, 
                                                            'rotated_rect': rect}

                # Get the center of the bounding box from the rect variable
                center_x, center_y = int(rect[0][0]), int(rect[0][1])

                # Retrieve the world coordinates of the center
                center_coordinates = self.get_cartesian_coordinates(center_x, center_y)

                if center_coordinates is not None:
                    # Add center coordinates to the dictionary
                    self.found_objects[f"{object_name}_{i}"].update({'center_coords': center_coordinates})
                else:
                    print("Failed to calculate center coordinates of the object.")

                width_point_1, width_point_2 = box[0], box[1] 
                height_point_1, height_point_2 = box[1], box[2]

                width_point_1_metric = self.get_cartesian_coordinates(width_point_1[0], width_point_1[1])
                width_point_2_metric = self.get_cartesian_coordinates(width_point_2[0], width_point_2[1])
                height_point_1_metric = self.get_cartesian_coordinates(height_point_1[0], height_point_1[1])
                height_point_2_metric = self.get_cartesian_coordinates(height_point_2[0], height_point_2[1])


                if width_point_1_metric is not None and width_point_2_metric is not None:
                    # Calculate the width of the bounding box
                    width = np.linalg.norm(width_point_1_metric[:2] - width_point_2_metric[:2])
                    height = np.linalg.norm(height_point_1_metric[:2] - height_point_2_metric[:2])

                    # Add width and height of object to the dictionary
                    self.found_objects[f"{object_name}_{i}"].update({'width': width, 'height': height})
                else:
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

        # Create a point cloud
        pc = rs.pointcloud()
        points = pc.calculate(self.depth_frame)
        pc.map_to(self.color_frame)

        # Get the vertices of the point cloud
        vertices = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, 3)

        # Get the width and height of the depth image
        width = self.depth_frame.get_width()

        # Calculate the index in the point cloud corresponding to the 2D pixel
        index = pixel_y * width + pixel_x

        # Ensure the index is within bounds
        if 0 <= index < len(vertices):
            # Access the 3D coordinates corresponding to the pixel
            cartesian_coordinates = vertices[index]

            #print(f"Cartesian coordinates for pixel ({pixel_x}, {pixel_y}): {cartesian_coordinates}")

            # Rotate the Cartesian coordinates 180 degrees around the z-axis
            # Because the camera has been flipped 180 degrees
            #rotation_matrix = np.array([[-1, 0, 0],
            #                            [0, -1, 0],
            #                            [0, 0, 1]])

            #rotated_coordinates = np.dot(rotation_matrix, cartesian_coordinates)

            #return rotated_coordinates
            return cartesian_coordinates
        else:
            print(f"Pixel coordinates ({pixel_x}, {pixel_y}) are out of bounds.")
            return None

    def show_cartesian_coordinates(self):
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                # Adjust the x, y coordinates to reflect a rotated image
                height, width, _ = color_image.shape
                adjusted_x = width - x
                adjusted_y = height - y
                coordinates = self.get_cartesian_coordinates(adjusted_x, adjusted_y)
                #coordinates = self.get_cartesian_coordinates(x, y)
                if coordinates is not None:
                    print(f"Cartesian coordinates at ({x}, {y}): {coordinates}")

        cv2.namedWindow("Image with Coordinates")
        cv2.setMouseCallback("Image with Coordinates", mouse_callback)

        self.capture_aligned_frames()
        color_image = self.get_color_image()

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


def main(args=None):
    rclpy.init(args=args)

    # Load the image you provided
    image_path = 'src/object_detector/Cell_Image_Example.jpg'
    image_example = cv2.imread(image_path)

    detector = ObjectDetector()

    while True:
        # Ask use which function to run
        print("\nChoose a function to run:")
        print("1. Show Frame")
        print("2. Find Object")
        print("3. Adjust HSV and Size Thresholds")
        print("4. Show Depth Map")
        print("5. Print Cartesian Coordinates")
        print("6. Spin the node")
        print("7. Calibrate Camera")
        print("8. Exit\n")

        choice = input("Enter your choice: ")


        if choice == '1':
            #Show the current frame from the camera
            detector.show_frame()

        elif choice == '2':
            #Find an object in the image
            detector.capture_aligned_frames()
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

        elif choice == '3':
            detector.capture_aligned_frames()
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

        elif choice == '4':
            detector.show_depth_map()

        elif choice == '5':
            detector.show_cartesian_coordinates()

        elif choice == '6':
            rclpy.spin(detector) 

        elif choice == '7':
            detector.realsense_camera.calibrate_camera()               

        elif choice == '8':
            break

        else:
            print("Invalid choice. Please try again.")

    rclpy.shutdown()


if __name__ == '__main__':
    main()

    # TODO: Integrate to ROS2
