from ujsonrpc import RPCRequest

class ScratchDisplayClearRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'scratch.display_clear', {})


class ScratchDisplaySetPixelRequest(RPCRequest):

    def __init__(self, idx: str, x: int, y: int, brightness: int):
        super().__init__(idx, 'scratch.display_set_pixel', {
            'x': x,
            'y': y,
            'brightness': brightness
        })


class ScratchDisplayImageRequest(RPCRequest):

    def __init__(self, idx: str, image: str):
        super().__init__(idx, 'scratch.display_image', {
            'image': image
        })


class ScratchDisplayImageForRequest(RPCRequest):

    def __init__(self, idx: str, image: str, duration: int):
        super().__init__(idx, 'scratch.display_image_for', {
            'image': image,
            'duration': duration
        })


class ScratchDisplayClearRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'scratch.display_clear', {})


class ScratchCenterButtonLightRequest(RPCRequest):

    def __init__(self, idx: str, color: int):
        super().__init__(idx, 'scratch.center_button_lights', {
            'color': color
        })

class ScratchDisplayTextRequest(RPCRequest):

    def __init__(self, idx: str, text: str):
        super().__init__(idx, 'scratch.display_text', {
            'text': text
        })

class ScratchDisplayImageRequest(RPCRequest):

    def __init__(self, idx: str, image: str = '00000\n00000\n00000\n00000\n00000'):
        super().__init__(idx, 'scratch.display_image', {
            'image': image
        })


class ScratchDisplayImageForRequest(RPCRequest):

    def __init__(self, idx: str, image: str, duration: int):
        super().__init__(idx, 'scratch.display_image_for', {
            'image': image,
            'duration': duration
        })


class ScratchDisplayClearRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'scratch.display_clear', {})


class ScratchDisplaySetPixelRequest(RPCRequest):

    def __init__(self, idx: str, x: int, y: int, brightness: int):
        super().__init__(idx, 'scratch.display_set_pixel', {
            'x': x,
            'y': y,
            'brightness': brightness
        })