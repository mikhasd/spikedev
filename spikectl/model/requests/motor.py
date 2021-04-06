from spikectl.ujsonrpc import RPCRequest


class MotorRunTimedRequest(RPCRequest):

    def __init__(self, idx: str, port: str, time: int, speed: int, stall: bool = True, stop: int = 1):
        super().__init__(idx, 'scratch.motor_run_timed', {
            'port': port,
            'time': time,
            'speed': speed,
            'stall': stall,
            'stop': stop
        })


class MotorGoToRelativePositionRequest(RPCRequest):

    def __init__(self, idx: str, port: str, position: int, speed: int, stall: bool = True, stop: int = 1):
        super().__init__(idx, 'scratch.motor_go_to_relative_position', {
            'port': port,
            'position': position,
            'speed': speed,
            'stall': stall,
            'stop': stop
        })


class MotorStartRequest(RPCRequest):

    def __init__(self, idx: str, port: str, speed: int, stall: bool = True):
        super().__init__(idx, 'scratch.motor_start', {
            'port': port,            
            'speed': speed,
            'stall': stall,            
        })


class MotorPowerRequest(RPCRequest):

    def __init__(self, idx: str, port: str, power: int, stall: bool = True):
        super().__init__(idx, 'scratch.motor_pwm', {
            'port': port,            
            'power': power,
            'stall': stall,            
        })


class MotorStopRequest(RPCRequest):

    def __init__(self, idx: str, port: str, stop: any):
        super().__init__(idx, 'scratch.motor_stop', {
            'port': port,            
            'stop': stop
        })


class MotorSetPositionRequest(RPCRequest):

    def __init__(self, idx: str, port: str, offset: int):
        super().__init__(idx, 'scratch.motor_set_position', {
            'port': port,
            'offset': offset
        })


class MotorRunForDegreesRequest(RPCRequest):

    def __init__(self, idx: str, port: str, speed: int, degrees: int, stall: bool = True, stop: int = 1):        
        super().__init__(idx, 'scratch.motor_run_for_degrees', {
            'port': port,
            'speed': speed,
            'degrees': degrees,
            'stall': stall,
            'stop': stop
        })

class MotorGoDirectionToPositionRequest(RPCRequest):
    # "port":"B","position":0,"speed":100,"direction":"shortest","stall":true,"stop":1
    # clockwise
    # anticlockwise
    # shortest
    def __init__(self, idx: str, port: str, speed: int, position: int, direction: str, stall: bool = True, stop: int = 1):        
        super().__init__(idx, 'scratch.motor_go_direction_to_position', {
            'port': port,
            'speed': speed,
            'position': position,
            'direction': direction,
            'stall': stall,
            'stop': stop
        })
