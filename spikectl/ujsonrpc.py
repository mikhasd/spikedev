from typing import Dict, Union
from base64 import b64decode
import json

RPC_KEY_ID = 'i'
RPC_KEY_METHOD = 'm'
RPC_KEY_RESULT = 'r'
RPC_KEY_ERROR = 'e'
RPC_KEY_PARAMETERS = 'p'

CR = '\r'


class RPCMessage:
    def is_error(self):
        return False

    def is_response(self):
        return False

    def is_request(self):
        return False

    def is_notification(self):
        return False


class RPCNotification(RPCMessage):
    def __init__(self, method: Union[str, int], parameters: any):
        self.method = method
        self.parameters = parameters

    def is_notification(self):
        return True

    def __str__(self):
        return 'RPCNotification [method: {method}, parameters: {parameters}]'.format(self)


class RPCError(RPCMessage):
    def __init__(self, id: str, exception_data: str):
        self.id = id
        decoded_exception_data = b64decode(exception_data)
        self.exception = str(decoded_exception_data, 'utf-8')

    def is_error(self):
        return True

    def __str__(self):
        return 'RPCError [id: {id}, exception: {exception}]'.format(self)


class RPCResponse(RPCMessage):
    def __init__(self, id: str, result: any):
        self.id = id
        self.result = result

    def is_response(self):
        return True


class RPCRequest(RPCMessage):
    def __init__(self, id: str, method: str, parameters: any):
        self.id = id
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


def to_json(obj: any) -> str:
    return json.dumps(obj, separators=(',', ':')) + CR


def request(id: str, method: str, parameters: any) -> str:
    return to_json({
        RPC_KEY_ID: id,
        RPC_KEY_METHOD: method,
        RPC_KEY_PARAMETERS: parameters
    })


def response(id: str, response: any) -> str:
    return to_json({
        RPC_KEY_ID: id,
        RPC_KEY_RESULT: response
    })


def notification(method: str, parameters: any) -> str:
    return to_json({
        RPC_KEY_METHOD: method,
        RPC_KEY_PARAMETERS: parameters
    })


def decode(msg: Dict[str, any]) -> RPCMessage:
    if is_notification(msg):  # Check notifications first as those are more frequent
        return RPCNotification(msg[RPC_KEY_METHOD], msg[RPC_KEY_PARAMETERS])
    elif is_response(msg):
        return RPCResponse(msg[RPC_KEY_ID], msg[RPC_KEY_RESULT])
    elif is_error(msg):
        return RPCError(msg[RPC_KEY_ID], msg[RPC_KEY_ERROR])
    elif is_request(msg):
        return RPCRequest(msg[RPC_KEY_ID], msg[RPC_KEY_METHOD], msg[RPC_KEY_PARAMETERS])
