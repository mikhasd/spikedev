import { RPCRequest } from '../ujsonrpc.js'

export class MotorRunTimedRequest extends RPCRequest {

    constructor(port, time, speed, stall = true, stop = 1, idx) {
        super('scratch.motor_run_timed', {
            'port': port,
            'time': (time),
            'speed': (speed),
            'stall': stall,
            'stop': (stop)
        }, idx)
    }
}


export class MotorGoToRelativePositionRequest extends RPCRequest {

    constructor(port, position, speed, stall = true, stop = 1, idx) {
        super('scratch.motor_go_to_relative_position', {
            'port': port,
            'position': (position),
            'speed': (speed),
            'stall': stall,
            'stop': (stop)
        }, idx)
    }
}

export class MotorStartRequest extends RPCRequest {

    constructor(port, speed, stall = true, idx) {
        super('scratch.motor_start', {
            'port': port,
            'speed': (speed),
            'stall': stall,
        }, idx)
    }
}

export class MotorPowerRequest extends RPCRequest {

    constructor(port, power, stall = true, idx) {
        super('scratch.motor_pwm', {
            'port': port,
            'power': (power),
            'stall': stall,
        }, idx)
    }
}

export class MotorStopRequest extends RPCRequest {

    constructor(port, stop, idx) {
        super('scratch.motor_stop', {
            'port': port,
            'stop': stop
        }, idx)
    }
}

export class MotorSetPositionRequest extends RPCRequest {

    constructor(port, offset, idx) {
        super('scratch.motor_set_position', {
            'port': port,
            'offset': (offset)
        }, idx)
    }
}

export class MotorRunForDegreesRequest extends RPCRequest {

    constructor(port, speed, degrees, stall = true, stop = 1, idx) {
        super('scratch.motor_run_for_degrees', {
            'port': port,
            'speed': (speed),
            'degrees': (degrees),
            'stall': stall,
            'stop': (stop)
        }, idx)
    }
}

export class MotorGoDirectionToPositionRequest extends RPCRequest {
    // "port":"B","position":0,"speed":100,"direction":"shortest","stall":true,"stop":1
    // clockwise
    // anticlockwise
    // shortest
    constructor(port, speed, position, direction, stall = true, stop = 1, idx) {
        super('scratch.motor_go_direction_to_position', {
            'port': port,
            'speed': (speed),
            'position': (position),
            'direction': direction,
            'stall': stall,
            'stop': (stop)
        }, idx)
    }
}