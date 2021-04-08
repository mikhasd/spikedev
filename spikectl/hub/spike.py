from __future__ import annotations
from typing import Type, Optional, Union, Callable

from serial import Serial
from serial.tools.list_ports import comports

from spikectl import ujsonrpc

from .serial import RawSerialHub, EmptyBuffer
from spikectl.model import *


_DEFAULT_BAUDRATE = 115200


class SpikeHubException(Exception): pass


class SpikeHub(RawSerialHub):

    def __init__(self, connection: Serial):
        super().__init__(connection)

    def listen_notifications(self, listener: Callable[[ujsonrpc.RPCNotification], bool], notification_type: Type = BaseNotification):

        def notification_listener(msg: ujsonrpc.RPCBaseMessage) -> bool:
            if msg.is_notification():
                notification = decode_notification(msg)
                if isinstance(notification, notification_type):
                    return listener(notification)
            return True
        
        try:
            self.listen(notification_listener)
        except EmptyBuffer:
            return None
    
    def listen_notification(self, notification_type: Type = BaseNotification) -> Optional[BaseNotification]:

        match: BaseNotification = None

        def notification_listener(notification: BaseNotification) -> bool:
            nonlocal match
            match = notification                    
            return False
        
        try:
            self.listen_notifications(notification_listener, notification_type)
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

    @property
    def display(self) -> Display:
        return Display(self)
    
    def motor(self, port: str) -> Motor:
        assert port in ['A', 'B', 'C', 'D', 'E', 'F'], 'port must be a letter between A and F'
        return Motor(self, port)

class Display:

    __slots__ = ['hub']

    def __init__(self, hub: SpikeHub):
        self.hub = hub
    
    def clear(self):
        request = ScratchDisplayClearRequest()
        self.hub._invoke(request)

    def set_pixel(self, x: int, y: int, brightness: int):
        assert 0 <= x <= 4 and 0 <= y <= 4 , 'x and y must be between 0 and 4'
        request = ScratchDisplaySetPixelRequest(x, y, brightness)
        self.hub._invoke(request)

    def display_image(self, image: str, duration: int = 0):
        assert image is not None, 'image must be present'
        assert len(image) is 29, 'image must be present'
        if duration is None:
            request = ScratchDisplayImageRequest(image)
        else:
            request = ScratchDisplayImageForRequest(image, duration)
        self.hub._invoke(request)

    def display_text(self, text: str):
        assert text is not None, 'tex is expected'
        request = ScratchDisplayTextRequest(text)
        self.hub._invoke(request)
        
    def set_button_color(self, color: int):
        assert 0 <= color <= 10, 'color must be between 0 and 10'
        request = ScratchCenterButtonLightRequest(color)
        self.hub._invoke(request)


class Motor:

    __slots__ = ['hub', 'port']

    def __init__(self, hub: SpikeHub, port: str):
        self.hub = hub
        self.port = port

    def run_timed(self, time: int, speed: int, stall: bool = True, stop: int = 1):
        assert time >= 0, 'time must be a positive number of milliseconds'
        assert -100 <= speed <= 100, 'speed must be between -100 and 100 per cent'
        request = MotorRunTimedRequest(self.port, time, speed, stall, stop)
        self.hub._invoke(request)

    def go_to_relative(self, position: int, speed: int, stall: bool = True, stop: int = 1):
        assert -100 <= speed <= 100, 'speed must be between -100 and 100 per cent'
        request = MotorGoToRelativePositionRequest(self.port, position, speed, stall, stop)
        self.hub._invoke(request)

    def start(self, speed: int, stall: bool = True, stop: int = 1):        
        assert -100 <= speed <= 100, 'speed must be between -100 and 100 per cent'
        request = MotorStartRequest(self.port, speed, stall, stop)
        self.hub._invoke(request)

    def stop(self, stop: int = 1):                
        request = MotorStopRequest(self.port, stop)
        self.hub._invoke(request)

    def power(self, power: int, stall: bool = True):
        assert -100 <= power <= 100, 'power must be between -100 and 100 per cent'
        request = MotorPowerRequest(self.port, power, stall)
        self.hub._invoke(request)

    def set_current_position(self, offset: int):
        request = MotorSetPositionRequest(self.port, offset)
        self.hub._invoke(request)

    def rotate(self, speed: int, degrees: int, stall: bool = True, stop: int = 1):
        assert -100 <= speed <= 100, 'speed must be between -100 and 100 per cent'
        request = MotorRunForDegreesRequest(self.port, speed, degrees, stall, stop)
        self.hub._invoke(request)

    def go_to(self, speed: int, position: int, direction: str = 'shortest', stall: bool = True, stop: int = 1):
        assert -100 <= speed <= 100, 'speed must be between -100 and 100 per cent'
        request = MotorGoDirectionToPositionRequest(self.port, speed, position, direction, stall, stop)
        self.hub._invoke(request)


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