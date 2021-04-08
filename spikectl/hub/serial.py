from typing import Callable, Optional
import json
from time import time

from serial import Serial
from serial.serialutil import CR

from spikectl import ujsonrpc


class SerialException(Exception): pass


class EmptyBuffer(SerialException): pass


class RawSerialHub(object):

    __slots__ = ['connection']

    def __init__(self, connection: Serial):
        self.connection = connection
        connection.flushInput()
        # Discard first message
        connection.read_until(expected=CR)

    def listen(self, listener: Callable[[ujsonrpc.RPCBaseMessage], bool], timeout: Optional[float] = None):

        deadline = time() + timeout if timeout is not None else float('inf')

        while time() < deadline:
            buffer = self.connection.read_until(expected=CR)
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
