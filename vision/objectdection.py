from ultralytics import YOLOWorld
import pyrealsense2 as rs
import numpy as np
import cv2


class RealSense:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(
            rs.stream.depth, 640, 480, rs.format.z16, 30
        )
        self.config.enable_stream(
            rs.stream.color, 640, 480, rs.format.bgr8, 30
        )

    def __enter__(self):
        self.pipeline.start(self.config)
        return self.pipeline

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipeline.stop()


class ObjectDetector:
    def __init__(self):
        self.model = YOLOWorld("yolov8x-world.pt")
        # results = self.model.predict("test.jpg")
        self.realsense_camera = RealSense

    def detect_all(self) -> None:
        with self.realsense_camera() as cam:
            is_q_key_pressed = (cv2.waitKey(1) & 0xFF == ord('q'))
            while not is_q_key_pressed:
                frames = cam.wait_for_frames()
                color_frame = frames.get_color_frame()
                color_image = np.asanyarray(color_frame.get_data())
                # results = self.model(color_image)
                # print(results)
                cv2.imshow("color", color_image)

    def detect_frame(self) -> None:
        with self.realsense_camera() as cam:
            frames = cam.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            results = self.model(color_image, stream=True)
            print(results)

            is_q_key_pressed = (cv2.waitKey(1) & 0xFF == ord('q'))
            while not is_q_key_pressed:
                cv2.imshow("color", color_image)

        cv2.destroyAllWindows()
        # results[0].show()


if __name__ == "__main__":
    # cam = RealSense()
    # cam.get_image()
    # cam.get_image("test.jpg")
    obj = ObjectDetector()
    obj.detect_frame()
