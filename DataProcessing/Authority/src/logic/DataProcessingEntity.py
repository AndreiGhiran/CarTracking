import cv2

from typing import List

from .DatabaseHandler import DatabaseHandler
from .algorithms.DepthEstimation import DepthEstimation
from .algorithms.ObjectDetection import ObjectDetection
from .algorithms.PositionReconstruction import PositionReconstruction


CONFIDENCE_SCORE_MIN = 0.2

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

            cv2.imshow('Depth', resized_depth_frame)
            cv2.imshow('Objects', frame_copy)
            cv2.waitKey(1)

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
