import pytest
from mockito import mock, spy, verify

from ...src.logic.DataProcessingEntity import DataProcessingEntity


@pytest.mark.usefixtures('unstub')
class TestDataProcessingEntity:
    def setup_class(self):
        self.__depth_estimation = mock()
        self.__object_detection = mock()
        self.__database_handler = mock()
        self.__position_reconstruction = mock()
        self.__data_processing_entity = DataProcessingEntity(0, 0, 0, 0, 0, self.__depth_estimation, self.__object_detection, self.__database_handler, self.__position_reconstruction, False)

    def test_when_ProcessData_then_ProcessingEntitiesCalledExactlyOnce(self):
        spy(self.__depth_estimation)
        spy(self.__object_detection)

        self.__data_processing_entity.process_frame([[[]]])

        verify(self.__depth_estimation).process_frame(...)
        verify(self.__object_detection).process_frame(...)