import torch

from typing import List

from .AbstractAlgorithm import AbstractAlgorithm


class DepthEstimation(AbstractAlgorithm):
    def __init__(self):
        self.__model = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
        self.__model.eval()

        midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
        self.__preprocess = midas_transforms.small_transform

    def process_frame(self, frame: List[List[List[int]]]) -> List[List[List[int]]]:
        return self.__estimate_depth(frame)

    def __estimate_depth(self, image):
        image_tensor = self.__preprocess(image)

        with torch.no_grad():
            prediction = self.__model(image_tensor)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=image.shape[:2],
                mode='bicubic',
                align_corners=False,
            ).squeeze()
        prediction = prediction.detach().cpu().numpy()
        
        return prediction