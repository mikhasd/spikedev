from serial import Serial
from serial.serialutil import CR
from ujsonrpc import decode, RPCError, RPCResponse, RPCNotification, encode_message
import json
from model.notifications import decode as decode_notification, SensorNotification, BatteryStatusNotification
from model.requests.motor import MotorSetPositionRequest, MotorRunForDegreesRequest
from model.requests import display
import traceback

connection = Serial(port='/dev/serial/by-id/usb-LEGO_System_A_S_LEGO_Technic_Large_Hub_in_FS_Mode_3659375B3238-if00', baudrate=115200)
connection.flushInput()

req = encode_message(display.ScratchDisplayClearRequest('1547'))
#req = encode_message(hub.SwitchModeRequest('abc1', 'play'))
connection.write(req.encode('utf-8'))

req = encode_message(display.ScratchDisplaySetPixelRequest('9512', 4, 4, 9))
#req = encode_message(hub.SwitchModeRequest('abc1', 'play'))
connection.write(req.encode('utf-8'))


#connection.write(program_execute)
# Discard first
connection.read_until(terminator=CR)
while True:
    buffer = connection.read_until(terminator=CR)
    msg = str(buffer, 'utf-8')    
    
    try:
        msg = json.loads(msg)
        decoded = decode(msg)
        if decoded.is_error():
            err: RPCError = decoded
            print('error {}'.format(err.exception))
        elif decoded.is_response():
            res: RPCResponse = decoded
            print('response {}'.format(res.result))
            if res.result == 'done':
                connection.close()
                exit()
        elif decoded.is_notification():
            notification: RPCNotification = decoded
            spike_notification = decode_notification(notification)
            if not isinstance(spike_notification, SensorNotification) and not isinstance(spike_notification, BatteryStatusNotification):
                print(spike_notification)            

    except Exception as err:
        print(msg)
        print(err)
        traceback.print_exc()
