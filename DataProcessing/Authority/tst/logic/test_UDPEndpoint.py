import pytest

from ...src.logic.UDPEndpoint import UDPEndpoint


@pytest.mark.usefixtures('unstub')
class TestUDPEndpoint:
    def setup_class(self):
        self.__udp_endpoint = UDPEndpoint(0, None)

    def test_when_ServerRunning_then_RaiseExceptionOnRun(self, when):
        when(self.__udp_endpoint).get_is_running().thenReturn(True)

        with pytest.raises(Exception):
            self.__udp_endpoint.run()

    def test_when_StopServer_then_ModifyRunningValue(self, when):
        when(self.__udp_endpoint).get_is_running().thenReturn(True)

        self.__udp_endpoint.stop()

        assert self.__udp_endpoint.get_is_running() == True

    def test_when_ServerNotRunning_then_RaiseExceptionOnStop(self, when):
        when(self.__udp_endpoint).get_is_running().thenReturn(False)

        with pytest.raises(Exception):
            self.__udp_endpoint.stop()