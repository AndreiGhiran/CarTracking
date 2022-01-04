import socket
import pickle
import struct

from threading import Lock

from .DataProcessingEntity import DataProcessingEntity


# Uses dependency injection for DataProcessingEntity
class UDPEndpoint:
    def __init__(self, frame_size: int, data_processing_entity: DataProcessingEntity):
        self.__frame_size = frame_size
        self.__can_start = True
        self.__is_running = False
        self.__is_running_lock = Lock() # Thread-safe
        self.__data_processing_entity = data_processing_entity

    def run(self):
        if self.get_is_running():
            raise Exception('UDPEndpoint already running.')

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('', 0))

        print(udp_socket.getsockname()[1]) # Send port to Dispatcher

        self.__set_is_running(True)

        allowed_address = None
        while self.get_is_running():
            data, sender_address = udp_socket.recvfrom(65535)
            if allowed_address is None:
                allowed_address = sender_address
            elif allowed_address != sender_address:
                print('Another client attempted to send data to the endpoint. Current sender: {}. Allowed sender: {}.'.format(sender_address, allowed_address))
                continue

            frame = pickle.loads(data)

            self.__data_processing_entity.process_frame(frame)

        udp_socket.close()

    def stop(self):
        if not self.get_is_running():
            raise Exception('UDPEndpoint not running.')
        self.__set_is_running(False)

    def get_is_running(self):
        self.__is_running_lock.acquire()
        is_running = self.__is_running
        self.__is_running_lock.release()

        return is_running

    def __set_is_running(self, is_running):
        self.__is_running_lock.acquire()
        self.__is_running = is_running
        self.__is_running_lock.release()