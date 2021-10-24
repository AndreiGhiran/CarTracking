import sys

from logic.DatabaseHandler import DatabaseHandler
from logic.UDPEndpoint import UDPEndpoint
from logic.DataProcessingEntity import DataProcessingEntity
from logic.algorithms.DepthEstimation import DepthEstimation
from logic.algorithms.ObjectDetection import ObjectDetection


IP = '0.0.0.0'
PORT = int(sys.argv[1])

FRAME_SIZE_X = int(sys.argv[2])
FRAME_SIZE_Y = int(sys.argv[3])
FRAME_SIZE = FRAME_SIZE_X * FRAME_SIZE_Y * 3

LATITUDE = float(sys.argv[4])
LONGITUDE = float(sys.argv[5])
ROTATION_X = float(sys.argv[6])
ROTATION_Y = float(sys.argv[7])

DB_USER = sys.argv[8]
DB_PASS = sys.argv[9]
DB_HOST = sys.argv[10]
DB_SCHEMA = sys.argv[11]


if __name__ == "__main__":
    database_handler = DatabaseHandler(DB_USER, DB_PASS, DB_HOST, DB_SCHEMA)
    database_handler.insert_camera(LATITUDE, LONGITUDE, ROTATION_X, ROTATION_Y)

    depth_estimation = DepthEstimation()
    object_detection = ObjectDetection()
    data_processing_entity = DataProcessingEntity(LATITUDE, LONGITUDE, ROTATION_X, ROTATION_Y, depth_estimation, object_detection, database_handler)

    udp_endpoint = UDPEndpoint(IP, PORT, FRAME_SIZE, data_processing_entity)
    udp_endpoint.run()