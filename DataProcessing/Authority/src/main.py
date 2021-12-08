import sys

from logic.DatabaseHandler import DatabaseHandler
from logic.UDPEndpoint import UDPEndpoint
from logic.DataProcessingEntity import DataProcessingEntity
from logic.algorithms.DepthEstimation import DepthEstimation
from logic.algorithms.ObjectDetection import ObjectDetection
from logic.algorithms.PositionReconstruction import PositionReconstruction


FOCAL_LENGTH_X = 35.
FOCAL_LENGTH_Y = 35.

FRAME_SIZE_X = int(sys.argv[1])
FRAME_SIZE_Y = int(sys.argv[2])
FRAME_SIZE = FRAME_SIZE_X * FRAME_SIZE_Y * 3

LATITUDE = float(sys.argv[3])
LONGITUDE = float(sys.argv[4])
ROTATION_X = float(sys.argv[5])
ROTATION_Y = float(sys.argv[6])

DB_USER = sys.argv[7]
DB_PASS = sys.argv[8]
DB_HOST = sys.argv[9]
DB_SCHEMA = sys.argv[10]


if __name__ == "__main__":
    database_handler = DatabaseHandler(DB_USER, DB_PASS, DB_HOST, DB_SCHEMA)
    camera_id = database_handler.insert_camera(LATITUDE, LONGITUDE, ROTATION_X, ROTATION_Y)

    depth_estimation = DepthEstimation()
    object_detection = ObjectDetection()
    position_reconstruction = PositionReconstruction(LATITUDE, LONGITUDE, ROTATION_X, ROTATION_Y, FOCAL_LENGTH_X, FOCAL_LENGTH_Y)
    data_processing_entity = DataProcessingEntity(camera_id, LATITUDE, LONGITUDE, ROTATION_X, ROTATION_Y, depth_estimation, object_detection, database_handler, position_reconstruction)

    udp_endpoint = UDPEndpoint(FRAME_SIZE, data_processing_entity)
    udp_endpoint.run()