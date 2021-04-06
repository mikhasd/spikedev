from typing import Callable, Type, Optional
import json

from serial import Serial
from serial.serialutil import CR
from serial.tools.list_ports import comports

from spikectl.model import TriggerCurrentStateRequest, InfoStatusNotification, BaseNotification, decode_notification

from spikectl import ujsonrpc


class SerialException(Exception): pass


class EmptyBuffer(SerialException): pass


class RawSerialHub(object):

    __slots__ = ['connection']

    def __init__(self, connection: Serial):
        self.connection = connection
        connection.flushInput()
        # Discard first message
        connection.read_until(terminator=CR)
    
    def listen(self, listener: Callable[[ujsonrpc.RPCBaseMessage], bool]):        

        while True:
            buffer = self.connection.read_until(terminator=CR)
            if not buffer:
                raise EmptyBuffer()
            json_str = str(buffer, 'utf-8')
            json_obj = json.loads(json_str)
            msg = ujsonrpc.decode(json_obj)            
            if not listener(msg):                
                return

    def send(self, message: ujsonrpc.RPCRequest):        
        json_str = ujsonrpc.encode(message)
        buffer = json_str.encode('utf-8')
        self.connection.write(buffer)

    def close(self):
        self.connection.close()
