import requests
import sys
import socket
import cv2
import pickle
import struct

from configparser import ConfigParser
import json


VIDEO_FILE_NAME = sys.argv[1]
VIDEO_FILE_PATH = '../data/{}'.format(VIDEO_FILE_NAME)

CAMERA_LATITUDE = sys.argv[2]
CAMERA_LONGITUDE = sys.argv[3]
CAMERA_ROTATION_X = sys.argv[4]
CAMERA_ROTATION_Y = sys.argv[5]


config_parser = ConfigParser()
config_parser.read('../configuration/data_processing_authority.config')
data_processing_authority_dispatcher_data = {
    'ip': config_parser.get('dispatcher', 'ip'),
    'port': config_parser.get('dispatcher', 'port')
}


def dispatch(frame_size_x, frame_size_y, latitude, longitude, rotation_x, rotation_y):
    url = '{}:{}/dispatch'.format(data_processing_authority_dispatcher_data['ip'], data_processing_authority_dispatcher_data['port'])
    data = json.dumps({
        'frame_size_x': frame_size_x,
        'frame_size_y': frame_size_y,
        'latitude': latitude,
        'longitude': longitude,
        'rotation_x': rotation_x,
        'rotation_y': rotation_y
    })
    response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
    data_processing_authority_port = response.json()['port']

    return data_processing_authority_port

def get_frame_size(video_file_path):
    video_capture = cv2.VideoCapture(video_file_path)
    frame_size_x, frame_size_y = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video_capture.release()

    return int(frame_size_x), int(frame_size_y)

def stream_frames(data_processing_authority_data, video_file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (data_processing_authority_data['ip'], data_processing_authority_data['port'])
    
    video_capture = cv2.VideoCapture(video_file_path)

    while video_capture.isOpened():
        video_not_ended, frame = video_capture.read()

        if video_not_ended:
            serialized_frame = pickle.dumps(frame)

            client_socket.sendall(
                struct.pack('L', len(serialized_frame) + serialized_frame),
                server_address
            )
        else:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

if __name__ == '__main__':
    frame_size_x, frame_size_y = get_frame_size(VIDEO_FILE_PATH)

    data_processing_authority_port = dispatch(
        frame_size_x,
        frame_size_y,
        CAMERA_LATITUDE,
        CAMERA_LONGITUDE,
        CAMERA_ROTATION_X,
        CAMERA_ROTATION_Y
    )

    data_processing_authority_data = {
        'ip': data_processing_authority_dispatcher_data['ip'],
        'port': data_processing_authority_port
    }

    stream_frames(data_processing_authority_data, VIDEO_FILE_PATH)