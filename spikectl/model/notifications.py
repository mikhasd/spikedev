from __future__ import annotations
from base64 import b64decode
from enum import Enum
from typing import List, Optional, Callable, Union, Dict

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


class SensorType(Enum):
    LPF2_FLIPPER_MOTOR_SMALL = 65, [1, 2, 3, 0]
    LPF2_FLIPPER_MOTOR_MEDIUM = 48, [1, 2, 3, 0]
    LPF2_FLIPPER_MOTOR_LARGE = 49, [1, 2, 3, 0]
    LPF2_FLIPPER_COLOR = 61, [1, 0]
    LPF2_FLIPPER_DISTANCE = 62
    LPF2_FLIPPER_FORCE = 63, [0, 1, 4]
    LPF2_ACCELERATION = 57
    LPF2_GYRO = 58
    LPF2_ORIENTATION = 59
    LPF2_STONE_GREY_MOTOR_MEDIUM = 75, [1, 2, 3, 0]
    LPF2_STONE_GREY_MOTOR_LARGE = 76, [1, 2, 3, 0]

    def __new__(cls, *args, **kwargs):
        idx = args[0]
        obj = object.__new__(cls)
        obj._value_ = idx
        return obj

    def __init__(self, idx: int, modes: Optional[List[int]] = None):
        super(Enum, self).__init__()
        self.modes = modes if modes else [0]

    def __str__(self):
        return self.name

    @classmethod
    def value_of(cls, idx: int) -> Optional[SensorType]:
        for st in cls:
            if st.value == idx:
                return st

        return None


def _decode_battery_status(notification: RPCNotification) -> BatteryStatusNotification:
    [voltage, percentage] = notification.parameters
    return BatteryStatusNotification(
        voltage,
        percentage
    )


def _decode_storage_information(notification: RPCNotification) -> StorageInformationNotification:
    data = notification.data
    return StorageInformationNotification(
        data.total,
        data.available,
        data.pct,
        data.unit,
        data.slots
    )


def __format_external_sensor(data: any, idx: int):
    type_idx, values = data[idx]
    sensor_type = SensorType.value_of(type_idx)
    if sensor_type is None:
        return None

    return {
        "type": sensor_type,
        "data": values
    }


def _decode_sensor_notification(notification: RPCNotification) -> SensorNotification:
    data = notification.parameters
    accelerometer = data[SensorDataIndex.Accelerometer.value]
    gyroscope = data[SensorDataIndex.Gyroscope.value]
    position = data[SensorDataIndex.Position.value]
    time = data[SensorDataIndex.Time.value]
    leds = data[SensorDataIndex.Display.value]
    a = __format_external_sensor(data, SensorDataIndex.PortA.value)
    b = __format_external_sensor(data, SensorDataIndex.PortB.value)
    c = __format_external_sensor(data, SensorDataIndex.PortC.value)
    d = __format_external_sensor(data, SensorDataIndex.PortD.value)
    e = __format_external_sensor(data, SensorDataIndex.PortE.value)
    f = __format_external_sensor(data, SensorDataIndex.PortF.value)
    return SensorNotification(
        accelerometer,
        gyroscope,
        position,
        time,
        leds,
        a,
        b,
        c,
        d,
        e,
        f
    )


def _decode_button_event(notification: RPCNotification) -> ButtonNotification:
    [button, state] = notification.parameters
    return ButtonNotification(
        button,
        state > 0
    )


def _decode_stack_start(notification: RPCNotification) -> StackStartNotification:
    data = b64decode(notification.parameters)
    return StackStartNotification(data)


def _decode_stack_stop(notification: RPCNotification) -> StackStopNotification:
    data = b64decode(notification.parameters)
    return StackStartNotification(data)


class NotificationType(Enum):
    SENSOR_DATA = 0, _decode_sensor_notification
    STORAGE_INFO = 1, _decode_storage_information
    BATTERY_STATUS = 2, _decode_battery_status
    BUTTON_EVENT = 3, _decode_button_event
    GESTURE_STATUS_NOTIFICATION = 4
    DISPLAY_STATUS_NOTIFICATION = 5
    FIRMWARE_STATUS_NOTIFICATION = 6
    STACK_START_NOTIFICATION = 7, _decode_stack_start
    STACK_STOP_NOTIFICATION = 8, _decode_stack_stop
    INFO_STATUS_NOTIFICATION = 9
    ERROR_NOTIFICATION = 10
    VM_STATE_NOTIFICATION = 11

    def __new__(cls, *args, **kwargs):
        idx = args[0]
        obj = object.__new__(cls)
        obj._value_ = idx
        return obj

    def __init__(self, idx: int, decoder: Callable[[RPCNotification], BaseNotification] = None):
        super(Enum, self).__init__()
        self.decoder = decoder if decoder else lambda n: n

    def __str__(self):
        return self.name

    @classmethod
    def value_of(cls, idx: int) -> Optional[NotificationType]:
        for st in cls:
            if st.value == idx:
                return st

        return None


class BaseNotification:

    @property
    def type(self) -> NotificationType: pass


class SensorNotification(BaseNotification):

    def __init__(self, accelerometer, gyroscope, position, time, leds, a, b, c, d, e, f):
        self.accelerometer = accelerometer
        self.gyroscope = gyroscope
        self.position = position
        self.time = time
        self.leds = leds
        self.A = a
        self.B = b
        self.C = c
        self.D = d
        self.E = e
        self.F = f

    @property
    def type(self) -> NotificationType: NotificationType.SENSOR_DATA

    def __str__(self):
        return 'SensorNotification [type: {}, accelerometer: {}, gyroscope: {}, position: {}, time: {}, leds: {}, A: {}, B: {}, C: {}, D: {}, E: {}, F: {}]'.format(
            self.type,
            self.accelerometer,
            self.gyroscope,
            self.position,
            self.time,
            self.leds,
            self.A,
            self.B,
            self.C,
            self.D,
            self.E,
            self.F
        )


# noinspection PyPropertyDefinition
class SlotInformation:

    @property
    def name(self) -> str: pass

    @property
    def id(self) -> str: pass

    @property
    def project_id(self) -> str: pass

    @property
    def modified(self) -> int: pass

    @property
    def type(self) -> str: pass

    @property
    def created(self) -> int: pass

    @property
    def size(self) -> int: pass


class StorageInformationNotification(BaseNotification):

    def __init__(self, total: int, available: int, pct: float, unit: Union['kb', 'mb'],
                 slots: Dict[str, SlotInformation]):
        self.total = total
        self.available = available
        self.pct = pct
        self.unit = unit
        self.slots = slots

    @property
    def type(self) -> NotificationType: NotificationType.STORAGE_INFO

    def __str__(self) -> str:
        return 'StorageInformationNotification [type: {}, total: {}, available: {}, pct: {}, unit: {}, slots: {}]'.format(
            self.type,
            self.total,
            self.available,
            self.pct,
            self.unit,
            self.slots
        )


class BatteryStatusNotification(BaseNotification):

    def __init__(self, voltage: float, percentage: int):
        self.voltage = voltage
        self.percentage = percentage

    @property
    def type(self) -> NotificationType: NotificationType.BATTERY_STATUS

    def __str__(self) -> str:
        return 'BatteryStatusNotification [type: {}, voltage: {}, percentage: {}]'.format(
            self.type,
            self.voltage,
            self.percentage
        )


class ButtonNotification(BaseNotification):

    def __init__(self, button: str, pressed: bool):
        self.button = button
        self.pressed = pressed

    @property
    def type(self) -> NotificationType: NotificationType.BUTTON_EVENT

    def __str__(self) -> str:
        return 'ButtonNotification [type: {}, button: {}, pressed: {}]'.format(
            self.type,
            self.button,
            self.pressed
        )


class StackStartNotification(BaseNotification):

    def __init__(self, data):
        self.data = data

    @property
    def type(self) -> NotificationType: NotificationType.STACK_START_NOTIFICATION

    def __str__(self) -> str:
        return 'StackStartNotification [type: {}, data: {}]'.format(
            self.type,
            self.data,
        )


class StackStopNotification(BaseNotification):

    def __init__(self, data):
        self.data = data

    @property
    def type(self) -> NotificationType: NotificationType.STACK_STOP_NOTIFICATION

    def __str__(self) -> str:
        return 'StackStopNotification [type: {}, data: {}]'.format(
            self.type,
            self.data,
        )


Notification = Union[
    BaseNotification, SensorNotification, StorageInformationNotification, BatteryStatusNotification, ButtonNotification,
    StackStartNotification, StackStartNotification]


def decode(notification: RPCNotification) -> Optional[Notification]:
    notification_type = NotificationType.value_of(notification.method)
    return notification_type.decoder(notification) if notification_type is not None else None
