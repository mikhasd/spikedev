from ujsonrpc import RPCRequest

class ScratchCenterButtonLightRequest(RPCRequest):

    def __init__(self, idx: str, color: int):
        super().__init__(idx, 'scratch.center_button_lights', {
            'color': color
        })
