from serial import Serial
from serial.serialutil import CR
from ujsonrpc import request, decode, RPCError, RPCResponse, RPCNotification
import json
from model import notifications

connection = Serial(port='COM3', baudrate=115200)
connection.flushInput()

program_execute = bytes(request('ABC123', 'program_execute', {"slotid": 0}), 'ascii')
connection.write(program_execute)
while True:
    buffer = connection.read_until(terminator=CR)
    msg = str(buffer, 'utf-8')
    try:
        msg = json.loads(msg)
        decoded = decode(msg)
        if decoded.is_error():
            err: RPCError = decoded
            print(err.exception)
        elif decoded.is_response():
            print('response')
            res: RPCResponse = decoded
            print(res.result)
        elif decoded.is_notification():
            notification: RPCNotification = decoded
            spike_notification = notifications.decode(notification)
            print(spike_notification)

    except Exception as err:
        print(msg)
        print(err)