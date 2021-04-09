from __future__ import annotations
from typing import Type, Optional, Union, Callable, List

from serial import Serial
from serial.tools.list_ports import comports

from spikectl import ujsonrpc

from .serial import RawSerialHub, EmptyBuffer
from spikectl.model import *


_DEFAULT_BAUDRATE = 115200


class SpikeHubException(Exception): pass

HubTask = Callable[[ujsonrpc.RPCBaseMessage], bool]

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
    
    def wait(self, *tasks: List[HubTask]):

        def task_wait_listener(msg: ujsonrpc.RPCBaseMessage) -> bool:
            nonlocal tasks
            tasks = [task for task in tasks if not task(msg)]            
            return len(tasks) > 0
    
        self.listen(task_wait_listener)

    def _invoke(self, request: ujsonrpc.RPCRequest) -> HubTask:
        self.send(request)

        def response_listener(msg: ujsonrpc.RPCBaseMessage) -> bool:
            nonlocal request
            if msg.is_response() or msg.is_error():                
                return msg.id == request.id
            return False
            

        return response_listener
    
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

    def set_pixel(self, x: int, y: int, brightness: int) -> HubTask:
        assert 0 <= x <= 4 and 0 <= y <= 4 , 'x and y must be between 0 and 4'
        request = ScratchDisplaySetPixelRequest(x, y, brightness)
        return self.hub._invoke(request)

    def display_image(self, image: str, duration: int = 0) -> HubTask:
        assert image is not None, 'image must be present'
        assert len(image) is 29, 'image must be present'
        if duration is None:
            request = ScratchDisplayImageRequest(image)
        else:
            request = ScratchDisplayImageForRequest(image, duration)
        return self.hub._invoke(request)

    def display_text(self, text: str) -> HubTask:
        assert text is not None, 'tex is expected'
        request = ScratchDisplayTextRequest(text)
        return self.hub._invoke(request)
        
    def set_button_color(self, color: int) -> HubTask:
        assert 0 <= color <= 10, 'color must be between 0 and 10'
        request = ScratchCenterButtonLightRequest(color)
        return self.hub._invoke(request)


class Motor:

    __slots__ = ['hub', 'port']

    def __init__(self, hub: SpikeHub, port: str):
        self.hub = hub
        self.port = port

    def run_timed(self, time: int, speed: int, stall: bool = True, stop: int = 1) -> HubTask:
        assert time >= 0, 'time must be a positive number of milliseconds'
        assert -100 <= speed <= 100, f'speed must be between -100 and 100 per cent: {speed}'
        request = MotorRunTimedRequest(self.port, time, speed, stall, stop)
        return self.hub._invoke(request)

    def go_to_relative(self, position: int, speed: int, stall: bool = True, stop: int = 1) -> HubTask:
        assert -100 <= speed <= 100, f'speed must be between -100 and 100 per cent: {speed}'
        request = MotorGoToRelativePositionRequest(self.port, position, speed, stall, stop)
        return self.hub._invoke(request)

    def start(self, speed: int, stall: bool = True) -> HubTask:
        assert -100 <= speed <= 100, f'speed must be between -100 and 100 per cent: {speed}'
        request = MotorStartRequest(self.port, speed, stall)
        return self.hub._invoke(request)

    def stop(self, stop: int = 1) -> HubTask:
        request = MotorStopRequest(self.port, stop)
        return self.hub._invoke(request)

    def power(self, power: int, stall: bool = True) -> HubTask:
        assert -100 <= power <= 100, 'power must be between -100 and 100 per cent'
        request = MotorPowerRequest(self.port, power, stall)
        return self.hub._invoke(request)

    def set_current_position(self, offset: int) -> HubTask:
        request = MotorSetPositionRequest(self.port, offset)
        return self.hub._invoke(request)

    def rotate(self, speed: int, degrees: int, stall: bool = True, stop: int = 1) -> HubTask:
        assert -100 <= speed <= 100, f'speed must be between -100 and 100 per cent: {speed}'
        request = MotorRunForDegreesRequest(self.port, speed, degrees, stall, stop)
        return self.hub._invoke(request)

    def go_to(self, speed: int, position: int, direction: str = 'shortest', stall: bool = True, stop: int = 1) -> HubTask:
        assert -100 <= speed <= 100, f'speed must be between -100 and 100 per cent: {speed}'
        request = MotorGoDirectionToPositionRequest(self.port, speed, position, direction, stall, stop)
        return self.hub._invoke(request)


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