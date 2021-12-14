import numpy as np

from sympy import sin, cos, sqrt, acos, atan2, pi
from typing import Tuple


GEOGRAPHICAL_UNIT_TO_METERS = 111000
MIDAS_DEPTH_UNIT_TO_METER = 10


# Recreates latitude and longitude, given an object's bounding box and the depth of each bounding box vertex
class PositionReconstruction:

    def __init__(self, latitude: float, longitude: float, rotation_x: float, rotation_y: float, focal_length_x: float, focal_length_y: float):

        self.__latitude = latitude
        self.__longitude = longitude
        self.__rotation_x = rotation_x
        self.__rotation_y = rotation_y
        self.__focal_length_x = focal_length_x
        self.__focal_length_y = focal_length_y

    def get_box_vertices_absolute_positions(self, box_coords, depth_image):

        if box_coords[0] >= depth_image.shape[0]:
            box_coords[0] = depth_image.shape[0] - 1
        if box_coords[1] >= depth_image.shape[1]:
            box_coords[1] = depth_image.shape[1] - 1
        if box_coords[2] >= depth_image.shape[0]:
            box_coords[2] = depth_image.shape[0] - 1
        if box_coords[3] >= depth_image.shape[1]:
            box_coords[3] = depth_image.shape[1] - 1

        # Bottom-left, bottom-right, top-left, top-right
        vertices_coords = list((
            (box_coords[0], box_coords[1]),
            (box_coords[2], box_coords[1]),
            (box_coords[0], box_coords[3]),
            (box_coords[2], box_coords[3])
        ))

        vertices_depth = list((
            depth_image[round(float(vertices_coords[i][0].item()))][round(float(vertices_coords[i][1].item()))] / MIDAS_DEPTH_UNIT_TO_METER
            for i in range(len(vertices_coords))
        ))

        box_vertices_absolute_positions = list((
            self.__get_absolute_position(vertices_coords[i][0], vertices_coords[i][1], vertices_depth[i])
            for i in range(len(vertices_coords))
        ))

        return box_vertices_absolute_positions

    def __get_absolute_position(self, pixel_x, pixel_y, depth):

        relative_x, relative_y, relative_z = self.__get_relative_position(pixel_x, pixel_y, depth)

        object_latitude = self.__latitude + relative_y / GEOGRAPHICAL_UNIT_TO_METERS
        object_longitude = self.__longitude + relative_x / GEOGRAPHICAL_UNIT_TO_METERS

        return (object_longitude, object_latitude)

    def __get_relative_position(self, pixel_x, pixel_y, depth):

        # As per https://stackoverflow.com/questions/31265245/extracting-3d-coordinates-given-2d-image-points-depth-map-and-camera-calibratio

        x = pixel_x * depth / self.__focal_length_x
        y = pixel_y * depth / self.__focal_length_y
        z = depth

        # Normalize, considering camera rotation
        r, theta, phi = self.__cartesian_to_spherical_coords(x, y, z)
        theta -= self.__rotation_x
        phi -= self.__rotation_y

        x, y, z = self.__spherical_to_cartesian_coords(r, theta, phi)

        return x, y, z

    def __cartesian_to_spherical_coords(self, x, y, z):

        r = float(sqrt(x * x + y * y + z * z))
        theta = float(acos(z / r) * 180 / pi)
        phi = float(atan2(y, x) * 180 / pi)

        return (r, theta, phi)

    def __spherical_to_cartesian_coords(self, r, theta, phi):

        x = float(r * sin(theta) * cos(phi))
        y = float(r * sin(theta) * sin(phi))
        z = float(r * cos(theta))

        return (x, y, z)
