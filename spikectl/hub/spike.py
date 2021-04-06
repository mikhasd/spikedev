from typing import Type, Optional, Union

from serial import Serial
from serial.tools.list_ports import comports

from spikectl import ujsonrpc

from .serial import RawSerialHub, EmptyBuffer
from spikectl.model import *


_DEFAULT_BAUDRATE = 115200


class SpikeHubException(Exception): pass


class SpikeHub(RawSerialHub):

    __slots__ = ['name']

    def __init__(self, connection: Serial):
        super().__init__(connection)
    
    def listen_notification(self, notification_type: Type = BaseNotification) -> Optional[BaseNotification]:

        match: BaseNotification = None

        def notification_listener(msg: ujsonrpc.RPCBaseMessage) -> bool:
            if msg.is_notification():
                notification = decode_notification(msg)
                if isinstance(notification, notification_type):
                    nonlocal match
                    match = notification                    
                    return False
            return True
        
        try:
            self.listen(notification_listener)            
            return match
        except EmptyBuffer:
            return None

    def listen_response(self, idx: str) -> Optional[Union[ujsonrpc.RPCResponse, ujsonrpc.RPCError]]:

        match: Union[ujsonrpc.RPCResponse, ujsonrpc.RPCError] = None

        def response_listener(msg: ujsonrpc.RPCBaseMessage) -> bool:
            if msg.is_response() or msg.is_error():
                if msg.id == idx:
                    nonlocal match
                    match = msg
                    return False
            return True
        
        try:
            self.listen(response_listener)
            return match
        except EmptyBuffer:
            return None
    
    
    def _invoke(self, request: ujsonrpc.RPCRequest) -> Optional[any]:
        self.send(request)
        response = self.listen_response(request.id)
        if response.is_error():
            raise SpikeHubException(response.exception)
        return response.result


    
    def trigger_current_state(self):
        request = TriggerCurrentStateRequest()
        self.send(request)

    def _init(self):
        self.trigger_current_state()
        n = self.listen_notification(InfoStatusNotification)
        self.name = n.name

    def display_clear(self):
        request = ScratchDisplayClearRequest()
        self.send(request)
        return self._invoke(request)

    def display_set_pixel(self, x: int, y: int, brightness: int):
        assert 0 <= x <= 4 and 0 <= y <= 4 , 'x and y must be between 0 and 4'
        request = ScratchDisplaySetPixelRequest(x, y, brightness)
        return self._invoke(request)
        
    def set_button_color(self, color: int):
        assert 0 <= color <= 10, 'color must be between 0 and 10'
        request = ScratchCenterButtonLightRequest(color)
        return self._invoke(request)


def find_hub(name: str) -> SpikeHub:
    
    lego_hub_ports = [port for port in comports()
        if port.product and 'LEGO Technic Large Hub' in port.product]
    
    for port in lego_hub_ports:

        hub = SpikeHub(Serial(port.device, baudrate=_DEFAULT_BAUDRATE, timeout=1))
        hub.trigger_current_state()
        notification = hub.listen_notification(InfoStatusNotification)        

        if notification.name == name:
            hub._init()
            return hub
        else:
            hub.close()
    
    return None