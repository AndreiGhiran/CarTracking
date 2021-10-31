import requests
import sys
import socket
import cv2
import pickle
import struct

from configparser import ConfigParser
from flask import jsonify


VIDEO_FILE_NAME = sys.arv[1]
VIDEO_FILE_PATH = '../data/{}'.format(VIDEO_FILE_NAME)

CAMERA_LATITUDE = sys.argv[2]
CAMERA_LONGITUDE = sys.argv[3]
CAMERA_ROTATION_X = sys.argv[4]
CAMERA_ROTATION_Y = sys.argv[5]


config_parser = ConfigParser()
config_parser.read('../configuration/fulfillment_authority.config')
fulfillment_authority_dispatcher_data = {
    'ip': config_parser.get('dispatcher', 'ip'),
    'port': config_parser.get('dispatcher', 'port')
}


def dispatch(frame_size_x, frame_size_y, latitude, longitude, rotation_x, rotation_y):
    url = '{}:{}'.format(fulfillment_authority_dispatcher_data['ip'], fulfillment_authority_dispatcher_data['port'])
    data = jsonify({
        'frame_size_x': frame_size_x,
        'frame_size_y': frame_size_y,
        'latitude': latitude,
        'longitude': longitude,
        'rotation_x': rotation_x,
        'rotation_y': rotation_y
    })
    response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
    fulfillment_authority_port = response.json()['port']

    return fulfillment_authority_port

def get_frame_size(video_file_path):
    video_capture = cv2.VideoCapture(video_file_path)
    frame_size_x, frame_size_y = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video_capture.release()

    return frame_size_x, frame_size_y

def stream_frames(fulfillment_authority_data, video_file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (fulfillment_authority_data['ip'], fulfillment_authority_data['port'])
    
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

    fulfillment_authority_port = dispatch(
        frame_size_x,
        frame_size_y,
        CAMERA_LATITUDE,
        CAMERA_LONGITUDE,
        CAMERA_ROTATION_X,
        CAMERA_ROTATION_Y
    )

    fulfillment_authority_data = {
        'ip': fulfillment_authority_dispatcher_data['ip'],
        'port': fulfillment_authority_port
    }

    stream_frames(fulfillment_authority_data, VIDEO_FILE_PATH)