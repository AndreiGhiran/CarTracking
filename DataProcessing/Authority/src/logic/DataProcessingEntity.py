import cv2
import numpy as np

from typing import List
from statistics import mean

from .DatabaseHandler import DatabaseHandler
from .algorithms.DepthEstimation import DepthEstimation
from .algorithms.ObjectDetection import ObjectDetection
from .algorithms.PositionReconstruction import PositionReconstruction


CONFIDENCE_SCORE_MIN = 0.15

CV2_IMSHOW_RESIZE = (480, 320)


# Uses dependency injection for DepthEstimation and ObjectDetection
class DataProcessingEntity:

    def __init__(self, camera_id: int, latitude: float, longitude: float, rotation_x: float, rotation_y: float, depth_estimation: DepthEstimation, object_detection: ObjectDetection, database_handler: DatabaseHandler, position_reconstruction: PositionReconstruction, verbose: bool):
        
        self.__camera_id = camera_id

        self.__database_handler = database_handler
        self.__depth_estimation = depth_estimation
        self.__object_detection = object_detection
        self.__position_reconstruction = position_reconstruction

        self.__classes = self.__object_detection.get_classes()
        self.__car_classes = self.__object_detection.get_car_classes()
        self.__other_classes = self.__object_detection.get_other_classes()

        self.__verbose = verbose

    def process_frame(self, frame):

        depth_frame = self.__depth_estimation.process_frame(frame)

        detected_objects = self.__object_detection.process_frame(frame)

        if detected_objects is None:
            return

        detected_objects = [
            {
                'box': detected_objects['boxes'][i],
                'is_car': self.__classes[detected_objects['labels'][i]] in self.__car_classes,
                'confidence': detected_objects['scores'][i],
                'label': self.__classes[detected_objects['labels'][i]]
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

        if self.__verbose:
            resized_depth_frame = cv2.resize(depth_frame, CV2_IMSHOW_RESIZE, interpolation=cv2.INTER_AREA) / 255.
            resized_frame = cv2.resize(frame, CV2_IMSHOW_RESIZE, interpolation=cv2.INTER_AREA)
            frame_copy = resized_frame.copy()
            for detected_object in detected_objects:
                box = detected_object['box'].detach().cpu().numpy()
                is_car = detected_object['is_car']
                confidence = detected_object['confidence']
                object_class = detected_object['label']

                (startX, startY, endX, endY) = box.astype('int')
                startX = round(startX * frame_copy.shape[1] / frame.shape[1])
                endX = round(endX * frame_copy.shape[1] / frame.shape[1])
                startY = round(startY * frame_copy.shape[0] / frame.shape[0])
                endY = round(endY * frame_copy.shape[0] / frame.shape[0])

                label = '{}: {:.2f}%'.format(object_class, confidence * 100)
                color = (0, 255, 0) if is_car else (255, 0, 0)

                cv2.rectangle(frame_copy, (startX, startY), (endX, endY), color, 2)
                startY = startY - 15 if startY - 15 > 15 else startY + 15

                cv2.putText(frame_copy, label, (startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            entities_map = self.__create_entities_map(cars_positions, obstacles_positions)

            cv2.imshow('Depth', resized_depth_frame)
            cv2.imshow('Objects', frame_copy)
            cv2.imshow('Map', entities_map)
            cv2.waitKey(1)


    def __create_entities_map(self, cars_positions, obstacles_positions):
        width = CV2_IMSHOW_RESIZE[0]
        height = CV2_IMSHOW_RESIZE[0]
        entities_map = np.zeros((height, width, 3), np.uint8)

        if len(cars_positions) == 0 and len(obstacles_positions) == 0:
            return entities_map

        cars_map_coords = [
            (
                mean([car_position[0], car_position[2], car_position[4], car_position[6]]),
                mean([car_position[1], car_position[3], car_position[5], car_position[7]])
            ) for car_position in cars_positions
        ]
        obstacles_map_coords = [
            (
                mean([obstacle_position[0], obstacle_position[2], obstacle_position[4], obstacle_position[6]]),
                mean([obstacle_position[1], obstacle_position[3], obstacle_position[5], obstacle_position[7]])
            ) for obstacle_position in obstacles_positions
        ]

        min_latitude = min(cars_map_coords + obstacles_map_coords, key=lambda x: x[0])[0]
        min_longitude = min(cars_map_coords + obstacles_map_coords, key=lambda x: x[1])[1]
        max_latitude = max(cars_map_coords + obstacles_map_coords, key=lambda x: x[0])[0]
        max_longitude = max(cars_map_coords + obstacles_map_coords, key=lambda x: x[1])[1]

        factor = 10 / 100

        min_latitude -= factor * (max_latitude - min_latitude)
        min_longitude -= factor * (max_longitude - min_longitude)
        max_latitude += factor * (max_latitude - min_latitude)
        max_longitude += factor * (max_longitude - min_longitude)

        if max_longitude == min_longitude:
            max_longitude = min_longitude + 1
        if max_latitude == min_latitude:
            max_latitude = min_latitude + 1

        for car_map_coord in cars_map_coords:
            x = round(width / (max_longitude - min_longitude) * (car_map_coord[0] - min_longitude))
            y = height - round(height / (max_latitude - min_latitude) * (car_map_coord[1] - min_latitude))
            entities_map = cv2.circle(entities_map, (x, y), radius=5, color=(0, 255, 0), thickness=-1)

        for obstacle_map_coord in obstacles_map_coords:
            x = round(width / (max_longitude - min_longitude) * (obstacle_map_coord[0] - min_longitude))
            y = height - round(height / (max_latitude - min_latitude) * (obstacle_map_coord[1] - min_latitude))
            entities_map = cv2.circle(entities_map, (x, y), radius=5, color=(255, 0, 0), thickness=-1)

        return entities_map
