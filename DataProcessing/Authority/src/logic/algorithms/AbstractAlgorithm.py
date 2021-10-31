from abc import ABC, abstractmethod
from typing import List


class AbstractAlgorithm(ABC):
    @abstractmethod
    def process_frame(self, frame: List[List[List[int]]]):
        pass