from typing import Dict, Union
from base64 import b64decode
import json
import random
import string

RPC_KEY_ID = 'i'
RPC_KEY_METHOD = 'm'
RPC_KEY_RESULT = 'r'
RPC_KEY_ERROR = 'e'
RPC_KEY_PARAMETERS = 'p'

CR = '\r'


class RPCBaseMessage(object):
    def is_error(self): False

    def is_response(self): False

    def is_request(self): False

    def is_notification(self): False


class RPCNotification(RPCBaseMessage):

    __slots__ = ['method', 'parameters']

    def __init__(self, method: Union[str, int], parameters: any):
        self.method = method
        self.parameters = parameters

    def is_notification(self):
        return True

    def __str__(self):
        return 'RPCNotification [method: {}, parameters: {}]'.format(
            self.method,
            self.parameters
        )


class RPCError(RPCBaseMessage):

    __slots__ = ['id', 'exception']

    def __init__(self, idx: str, exception_data: str):
        self.id = idx
        decoded_exception_data = b64decode(exception_data)
        self.exception = str(decoded_exception_data, 'utf-8')

    def is_error(self):
        return True

    def __str__(self):
        return 'RPCError [id: {}, exception: {}]'.format(
            self.id,
            self.exception
        )


class RPCResponse(RPCBaseMessage):

    __slots__ = ['id', 'result']

    def __init__(self, idx: str, result: any):
        self.id = idx
        self.result = result

    def is_response(self):
        return True

    def __str__(self):
        return f'RPCResponse [id: {self.id}, result: {self.result}]'


def gen_idx() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))


class RPCRequest(RPCBaseMessage):

    __slots__ = ['id', 'method', 'parameters']

    def __init__(self, method: str, parameters: any, idx: str):
        self.id = idx if idx else gen_idx()        
        self.method = method
        self.parameters = parameters

    def is_request(self):
        return True


def is_request(msg: any) -> bool:
    return RPC_KEY_ID in msg and RPC_KEY_METHOD in msg and RPC_KEY_PARAMETERS in msg


def is_response(msg) -> bool:
    return RPC_KEY_ID in msg and RPC_KEY_RESULT in msg


def is_error(msg) -> bool:
    return RPC_KEY_ID in msg and RPC_KEY_ERROR in msg


def is_notification(msg) -> bool:
    return RPC_KEY_METHOD in msg and RPC_KEY_PARAMETERS in msg and RPC_KEY_ID not in msg


def _to_json(obj: any) -> str:
    return json.dumps(obj, separators=(',', ':')) + CR


def encode_request(idx: str, method: str, parameters: any) -> str:
    return _to_json({
        RPC_KEY_ID: idx,
        RPC_KEY_METHOD: method,
        RPC_KEY_PARAMETERS: parameters
    })


def encode_response(idx: str, response: any) -> str:
    return _to_json({
        RPC_KEY_ID: idx,
        RPC_KEY_RESULT: response
    })


def encode_notification(method: str, parameters: any) -> str:
    return _to_json({
        RPC_KEY_METHOD: method,
        RPC_KEY_PARAMETERS: parameters
    })


def decode(msg: Dict[str, any]) -> RPCBaseMessage:
    if is_notification(msg):  # Check notifications first as those are more frequent
        return RPCNotification(msg[RPC_KEY_METHOD], msg[RPC_KEY_PARAMETERS])
    elif is_response(msg):
        return RPCResponse(msg[RPC_KEY_ID], msg[RPC_KEY_RESULT])
    elif is_error(msg):
        return RPCError(msg[RPC_KEY_ID], msg[RPC_KEY_ERROR])
    elif is_request(msg):
        return RPCRequest(msg[RPC_KEY_ID], msg[RPC_KEY_METHOD], msg[RPC_KEY_PARAMETERS])

def encode(msg: Union[RPCBaseMessage]) -> str:
    if isinstance(msg, RPCBaseMessage):
        if msg.is_request():
            request: RPCRequest = msg
            return encode_request(
                request.id,
                request.method,
                request.parameters
            )

    raise Exception(f'Unexcpected message type {type(msg)}')


__all__ = [
    'encode',
    'decode',
    'RPCBaseMessage',
    'RPCNotification',
    'RPCError',
    'RPCRequest',
    'RPCResponse'
]