from typing import List, Optional
from enum import Enum
from ujsonrpc import RPCNotification


class SensorDataIndex(Enum):
    PortA = 0
    PortB = 1
    PortC = 2
    PortD = 3
    PortE = 4
    PortF = 5
    Accelerometer = 6
    Gyroscope = 7
    Position = 8
    Display = 9
    Time = 10


class SensorType:

    def __init__(self, idx: int, modes: Optional[List[int]]):
        self.idx = idx
        self.modes = modes if modes else [0]


class SensorTypes:
    LPF2_FLIPPER_MOTOR_SMALL = SensorType(65, [1, 2, 3, 0])
    LPF2_FLIPPER_MOTOR_MEDIUM = SensorType(48, [1, 2, 3, 0])
    LPF2_FLIPPER_MOTOR_LARGE = SensorType(49, [1, 2, 3, 0])
    LPF2_FLIPPER_COLOR = SensorType(61, [1, 0])
    LPF2_FLIPPER_DISTANCE = SensorType(62)
    LPF2_FLIPPER_FORCE = SensorType(63, [0, 1, 4])
    LPF2_ACCELERATION = SensorType(57)
    LPF2_GYRO = SensorType(58)
    LPF2_ORIENTATION = SensorType(59)
    LPF2_STONE_GREY_MOTOR_MEDIUM = SensorType(75, [1, 2, 3, 0])
    LPF2_STONE_GREY_MOTOR_LARGE = SensorType(76, [1, 2, 3, 0])

    __values: List[SensorType] = None

    @staticmethod
    def values() -> List[SensorType]:
        if not SensorTypes.__values:
            SensorTypes.__values = [sensor_type for name, sensor_type in SensorType.__dict__.items() if '__' not in name]
        return SensorTypes.__values.copy()

    @staticmethod
    def value_of(idx: int) -> Optional[SensorType]:
        if not SensorTypes.__values:
            SensorTypes.__values = [sensor_type for name, sensor_type in SensorType.__dict__.items() if '__' not in name]

        for st in SensorTypes.__values:
            if st.idx == idx:
                return st

        return None



SENSOR_TYPE_NAMES = {idx: name for name, idx in SensorType.__dict__.items() if '__' not in name}


class NotificationMethod:
    SENSOR_DATA = 0
    STORAGE_INFO = 1
    BATTERY_STATUS = 2
    BUTTON_EVENT = 3
    GESTURE_STATUS_NOTIFICATION = 4
    DISPLAY_STATUS_NOTIFICATION = 5
    FIRMWARE_STATUS_NOTIFICATION = 6
    STACK_START_NOTIFICATION = 7
    STACK_STOP_NOTIFICATION = 8
    INFO_STATUS_NOTIFICATION = 9
    ERROR_NOTIFICATION = 10
    VM_STATE_NOTIFICATION = 11


NOTIFICATION_METHODS = [idx for method, idx in NotificationMethod.__dict__.items() if '__' not in method]
NOTIFICATION_METHOD_NAMES = [method for method, _ in NotificationMethod.__dict__.items() if '__' not in method]


def __format_external_sensor(data: any, idx: int):
    type, values = data[idx]
    if type == 0:
        return None

    return {
        "type": SENSOR_TYPE_NAMES[type],
        "data": values
    }


def __decode_sensor_notification(notification: RPCNotification):
    data = notification.parameters
    accelerometer = data[SensorDataIndex.Accelerometer]
    gyroscope = data[SensorDataIndex.Gyroscope]
    position = data[SensorDataIndex.Position]
    time = data[SensorDataIndex.Time]
    leds = data[SensorDataIndex.Display]
    A = __format_external_sensor(data, SensorDataIndex.PortA)
    B = __format_external_sensor(data, SensorDataIndex.PortB)
    C = __format_external_sensor(data, SensorDataIndex.PortC)
    D = __format_external_sensor(data, SensorDataIndex.PortD)
    E = __format_external_sensor(data, SensorDataIndex.PortE)
    F = __format_external_sensor(data, SensorDataIndex.PortF)
    notification_type = NOTIFICATION_METHOD_NAMES[notification.method]
    return {
        "type": notification_type,
        "accelerometer": accelerometer,
        "gyroscope": gyroscope,
        "position": position,
        "time": time,
        "leds": leds,
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "E": E,
        "F": F,
    }


def is_known_notification_method(notification: RPCNotification) -> bool:
    return notification.method in NOTIFICATION_METHODS


def decode(notification: RPCNotification):
    if notification.method == NotificationMethod.SENSOR_DATA:
        sensor_notification = __decode_sensor_notification(notification)
        return sensor_notification
    return notification
