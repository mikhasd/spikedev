from spikectl.ujsonrpc import RPCRequest


class MotorRunTimedRequest(RPCRequest):

    def __init__(self, port: str, time: int, speed: int, stall: bool = True, stop: int = 1, idx: str = None):
        super().__init__('scratch.motor_run_timed', {
            'port': port,
            'time': time,
            'speed': speed,
            'stall': stall,
            'stop': stop
        }, idx=idx)


class MotorGoToRelativePositionRequest(RPCRequest):

    def __init__(self, port: str, position: int, speed: int, stall: bool = True, stop: int = 1, idx: str = None):
        super().__init__('scratch.motor_go_to_relative_position', {
            'port': port,
            'position': position,
            'speed': speed,
            'stall': stall,
            'stop': stop
        }, idx=idx)


class MotorStartRequest(RPCRequest):

    def __init__(self, port: str, speed: int, stall: bool = True, idx: str = None):
        super().__init__('scratch.motor_start', {
            'port': port,            
            'speed': speed,
            'stall': stall,            
        }, idx=idx)


class MotorPowerRequest(RPCRequest):

    def __init__(self, port: str, power: int, stall: bool = True, idx: str = None):
        super().__init__('scratch.motor_pwm', {
            'port': port,            
            'power': power,
            'stall': stall,            
        }, idx=idx)


class MotorStopRequest(RPCRequest):

    def __init__(self, port: str, stop: any, idx: str = None):
        super().__init__('scratch.motor_stop', {
            'port': port,            
            'stop': stop
        }, idx=idx)


class MotorSetPositionRequest(RPCRequest):

    def __init__(self, port: str, offset: int, idx: str = None):
        super().__init__('scratch.motor_set_position', {
            'port': port,
            'offset': offset
        }, idx=idx)


class MotorRunForDegreesRequest(RPCRequest):

    def __init__(self, port: str, speed: int, degrees: int, stall: bool = True, stop: int = 1, idx: str = None):
        super().__init__('scratch.motor_run_for_degrees', {
            'port': port,
            'speed': speed,
            'degrees': degrees,
            'stall': stall,
            'stop': stop
        }, idx=idx)

class MotorGoDirectionToPositionRequest(RPCRequest):
    # "port":"B","position":0,"speed":100,"direction":"shortest","stall":true,"stop":1
    # clockwise
    # anticlockwise
    # shortest
    def __init__(self, port: str, speed: int, position: int, direction: str, stall: bool = True, stop: int = 1, idx: str = None):        
        super().__init__('scratch.motor_go_direction_to_position', {
            'port': port,
            'speed': speed,
            'position': position,
            'direction': direction,
            'stall': stall,
            'stop': stop
        }, idx=idx)
