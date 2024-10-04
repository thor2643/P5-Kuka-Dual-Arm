from ultralytics import YOLOWorld
import pyrealsense2 as rs
import numpy as np
import cv2


class RealSenseCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # self.config.enable_stream(
        #     rs.stream.depth, 640, 480, rs.format.z16, 30
        # )
        self.config.enable_stream(
            rs.stream.color, 640, 480, rs.format.bgr8, 30
        )

    def __enter__(self):
        self.pipeline.start(self.config)

        color_sensor = self.pipeline.get_active_profile().get_device().query_sensors()[1]

        # set options for color sensor
        color_sensor.set_option(rs.option.brightness, 0)
        color_sensor.set_option(rs.option.exposure, 166)
        color_sensor.set_option(rs.option.white_balance, 4200)

        return self.pipeline

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipeline.stop()


class ObjectDetector:
    def __init__(self):
        self.model = YOLOWorld("yolov8x-world.pt")
        self.realsense_camera = RealSenseCamera
        self.detection_groups = dict()

    def detect_frame(self) -> None:
        with self.realsense_camera() as cam:
            frames = cam.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_frame = np.asanyarray(color_frame.get_data())

            results = self.model(color_frame, verbose=False, stream=False)[0]

            for detection in results.boxes:
                x, y, *_ = detection.xywh[0]
                idx = int(detection.cls[0])
                key = results.names[idx]

                self._insert_into_detection_groups(key=key, info=(x, y))

            return self.detection_groups

    def _insert_into_detection_groups(self, key: str, info: tuple[int, int]) -> None:
            if key in self.detection_groups.keys():
                self.detection_groups[key].append(info)
            else:
                self.detection_groups[key] = [info]



if __name__ == "__main__":
    obj = ObjectDetector()
    print(obj.detect_frame())
