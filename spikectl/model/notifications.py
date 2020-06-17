from __future__ import annotations

from base64 import b64decode
from enum import Enum
from typing import List, Optional, Callable, Dict

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

    # noinspection PyUnusedLocal
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
    data = notification.parameters
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
    stack_id = b64decode(notification.parameters)
    return StackStartNotification(stack_id)


def _decode_stack_stop(notification: RPCNotification) -> StackStopNotification:
    stack_id = b64decode(notification.parameters)
    return StackStopNotification(stack_id)


def _decode_vm_state(notification: RPCNotification) -> VmStateNotification:
    [target, variables, lists, store] = notification.parameters
    return VmStateNotification(
        target,
        variables,
        lists,
        store
    )


def _decode_program_running(notification: RPCNotification) -> ProgramRunningNotification:
    [project_id, running] = notification.parameters
    return ProgramRunningNotification(
        project_id,
        running
    )


def _decode_info_status(notification: RPCNotification) -> InfoStatusNotification:
    [encoded_name] = notification.parameters
    encoded_name_utf8_bytes = b64decode(encoded_name)
    name = str(encoded_name_utf8_bytes, 'utf-8')
    return InfoStatusNotification(
        name
    )


def _decode_error(notification: RPCNotification) -> ErrorNotification:
    [error_type, message] = notification.parameters
    return ErrorNotification(
        error_type,
        message
    )


class NotificationType(Enum):
    Sensor = 0, _decode_sensor_notification
    Storage = 1, _decode_storage_information
    Battery = 2, _decode_battery_status
    Button = 3, _decode_button_event
    GESTURE_STATUS_NOTIFICATION = 4
    DISPLAY_STATUS_NOTIFICATION = 5
    FIRMWARE_STATUS_NOTIFICATION = 6
    StackStart = 7, _decode_stack_start
    StackStop = 8, _decode_stack_stop
    Info = 9, _decode_info_status
    Error = 10, _decode_error
    VMState = 11, _decode_vm_state
    ProgramRunning = 12, _decode_program_running

    def __new__(cls, *args, **kwargs):
        idx = args[0]
        obj = object.__new__(cls)
        obj._value_ = idx
        return obj

    # noinspection PyUnusedLocal
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

    # noinspection PyPropertyDefinition
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
    def type(self) -> NotificationType: return NotificationType.Sensor

    def __str__(self):
        return f'SensorNotification [accelerometer: {self.accelerometer}, gyroscope: {self.gyroscope}, ' \
               f'position: {self.position}, time: {self.time}, leds: {self.leds}, A: {self.A}, B: {self.B}, ' \
               f'C: {self.C}, D: {self.D}, E: {self.E}, F: {self.F}] '


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

    def __init__(self, total: int, available: int, pct: float, unit: str, slots: Dict[str, SlotInformation]):
        self.total = total
        self.available = available
        self.pct = pct
        self.unit = unit
        self.slots = slots

    @property
    def type(self) -> NotificationType: return NotificationType.Storage

    def __str__(self) -> str:
        return f'StorageInformationNotification [total: {self.total}, available: {self.available}, pct: {self.pct}, ' \
               f'unit: {self.unit}, slots: {self.slots}]'


class BatteryStatusNotification(BaseNotification):

    def __init__(self, voltage: float, percentage: int):
        self.voltage = voltage
        self.percentage = percentage

    @property
    def type(self) -> NotificationType: return NotificationType.Battery

    def __str__(self) -> str:
        return f'BatteryStatusNotification [voltage: {self.voltage}, percentage: {self.percentage}]'


class ButtonNotification(BaseNotification):

    def __init__(self, button: str, pressed: bool):
        self.button = button
        self.pressed = pressed

    @property
    def type(self) -> NotificationType: return NotificationType.Button

    def __str__(self) -> str:
        return f'ButtonNotification [button: {self.button}, pressed: {self.pressed}]'


class StackStartNotification(BaseNotification):

    def __init__(self, stack_id: str):
        self.stack_id = stack_id

    @property
    def type(self) -> NotificationType: return NotificationType.StackStart

    def __str__(self) -> str:
        return f'StackStartNotification [stack_id: {self.stack_id}]'


class StackStopNotification(BaseNotification):

    def __init__(self, stack_id: str):
        self.stack_id = stack_id

    @property
    def type(self) -> NotificationType: return NotificationType.StackStop

    def __str__(self) -> str:
        return f'StackStopNotification [stack_id: {self.stack_id}]'


class VmStateNotification(BaseNotification):

    def __init__(self, target: str, variables, lists, store):
        self.target = target
        self.variables = variables
        self.lists = lists
        self.store = store

    @property
    def type(self) -> NotificationType: return NotificationType.VMState

    def __str__(self) -> str:
        return 'VmStateNotification [target: {}, variables: {}, lists: {}, store: {}]'.format(
            self.type,
            self.target,
            self.variables,
            self.lists,
            self.store
        )


class ProgramRunningNotification(BaseNotification):

    def __init__(self, project_id: str, running: bool):
        self.project_id = project_id
        self.running = running

    @property
    def type(self) -> NotificationType: return NotificationType.ProgramRunning

    def __str__(self) -> str:
        return f'ProgramRunningNotification [project_id: {self.project_id}, running: {self.running}]'


class InfoStatusNotification(BaseNotification):

    def __init__(self, name: str):
        self.name = name

    @property
    def type(self) -> NotificationType: return NotificationType.ProgramRunning

    def __str__(self) -> str:
        return f'InfoStatusNotification [name: {self.name}]'


class ErrorNotification(BaseNotification):

    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        self.message = message

    @property
    def type(self) -> NotificationType: return NotificationType.Error

    def __str__(self) -> str:
        return f'ErrorNotification [error_type: {self.error_type}, message: {self.message}]'


def decode(notification: RPCNotification) -> Optional[BaseNotification]:
    notification_type = NotificationType.value_of(notification.method)
    return notification_type.decoder(notification) if notification_type is not None else None
