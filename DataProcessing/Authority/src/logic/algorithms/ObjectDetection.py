import torch
import numpy as np
import cv2

from torchvision.models import detection
from typing import List

from .AbstractAlgorithm import AbstractAlgorithm


CLASSES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

MODELS = {
    'frcnn-resnet': detection.fasterrcnn_resnet50_fpn,
    'frcnn-mobilenet': detection.fasterrcnn_mobilenet_v3_large_320_fpn,
    'retinanet': detection.retinanet_resnet50_fpn
}


class ObjectDetection(AbstractAlgorithm):
    def __init__(self):
        self.__classes = CLASSES
        self.__model = MODELS['frcnn-mobilenet'](pretrained=True, progress=True, num_classes=len(CLASSES), pretrained_backbone=True)
        self.__model.eval()

    def get_classes(self) -> List[str]:
        return self.__classes

    def process_frame(self, frame: List[List[List[int]]]):
        return self.__get_objects(frame)

    def __get_objects(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.transpose((2, 0, 1))
        image = np.expand_dims(image, axis=0)
        image = image / 255.0
        image = torch.FloatTensor(image)
        
        detections = self.__model(image)[0]

        return detections