from typing import List

from .DatabaseHandler import DatabaseHandler
from .algorithms.DepthEstimation import DepthEstimation
from .algorithms.ObjectDetection import ObjectDetection


# Uses dependency injection for DepthEstimation and ObjectDetection
class DataProcessingEntity:
    def __init__(self, latitude: float, longitude: float, rotation_x: float, rotation_y: float, depth_estimation: DepthEstimation, object_detection: ObjectDetection, database_handler: DatabaseHandler):
        self.__database_handler = database_handler
        self.__depth_estimation = depth_estimation
        self.__object_detection = object_detection

    def process_frame(self, frame: List[List[List[int]]]):
        depth_frame = self.__depth_estimation.process_frame(frame)
        detected_objects = self.__object_detection.process_frame(frame)