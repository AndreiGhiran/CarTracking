from typing import List

from .DatabaseHandler import DatabaseHandler
from .algorithms.DepthEstimation import DepthEstimation
from .algorithms.ObjectDetection import ObjectDetection
from .algorithms.PositionReconstruction import PositionReconstruction


CONFIDENCE_SCORE_MIN = 0.15


# Uses dependency injection for DepthEstimation and ObjectDetection
class DataProcessingEntity:

    def __init__(self, camera_id: int, latitude: float, longitude: float, rotation_x: float, rotation_y: float, depth_estimation: DepthEstimation, object_detection: ObjectDetection, database_handler: DatabaseHandler, position_reconstruction: PositionReconstruction):
        
        self.__camera_id = camera_id

        self.__database_handler = database_handler
        self.__depth_estimation = depth_estimation
        self.__object_detection = object_detection
        self.__position_reconstruction = position_reconstruction

        self.__classes = self.__object_detection.get_classes()
        self.__car_classes = self.__object_detection.get_car_classes()
        self.__other_classes = self.__object_detection.get_other_classes()

    def process_frame(self, frame):

        depth_frame = self.__depth_estimation.process_frame(frame)
        detected_objects = self.__object_detection.process_frame(frame)

        if detected_objects is None:
            return

        detected_objects = [
            {
                'box': detected_objects['boxes'][i],
                'is_car': self.__classes[detected_objects['labels'][i]] in self.__car_classes
            }
            for i in range(len(detected_objects['boxes'])) if detected_objects['scores'][i] >= CONFIDENCE_SCORE_MIN
        ]

        cars_positions = []
        obstacles_positions = []
        for i in range(len(detected_objects)):
            box_vertices_absolute_positions = self.__position_reconstruction.get_box_vertices_absolute_positions(detected_objects[i]['box'], depth_frame)

            box_1_longitude = box_vertices_absolute_positions[0][0]
            box_1_latitude = box_vertices_absolute_positions[0][1]
            box_2_longitude = box_vertices_absolute_positions[1][0]
            box_2_latitude = box_vertices_absolute_positions[1][1]
            box_3_longitude = box_vertices_absolute_positions[2][0]
            box_3_latitude = box_vertices_absolute_positions[2][1]
            box_4_longitude = box_vertices_absolute_positions[3][0]
            box_4_latitude = box_vertices_absolute_positions[3][1]

            if detected_objects[i]['is_car']:
                cars_positions.append((
                    box_1_latitude,
                    box_1_longitude,
                    box_2_latitude,
                    box_2_longitude,
                    box_3_latitude,
                    box_3_longitude,
                    box_4_latitude,
                    box_4_longitude
                ))
            else:
                obstacles_positions.append((
                    box_1_latitude,
                    box_1_longitude,
                    box_2_latitude,
                    box_2_longitude,
                    box_3_latitude,
                    box_3_longitude,
                    box_4_latitude,
                    box_4_longitude
                ))

        self.__database_handler.insert_cars(self.__camera_id, cars_positions)
        self.__database_handler.insert_obstacles(self.__camera_id, obstacles_positions)
