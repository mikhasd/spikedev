from spikectl.ujsonrpc import RPCRequest

class ScratchDisplayClearRequest(RPCRequest):

    def __init__(self, idx: str = None):
        super().__init__('scratch.display_clear', {}, idx=idx)


class ScratchDisplaySetPixelRequest(RPCRequest):

    def __init__(self, x: int, y: int, brightness: int, idx: str = None):
        super().__init__('scratch.display_set_pixel', {
            'x': x,
            'y': y,
            'brightness': brightness
        }, idx=idx)


class ScratchDisplayImageRequest(RPCRequest):

    def __init__(self, image: str, idx: str = None):
        super().__init__('scratch.display_image', {
            'image': image
        }, idx=idx)


class ScratchDisplayImageForRequest(RPCRequest):

    def __init__(self, image: str, duration: int, idx: str = None):
        super().__init__('scratch.display_image_for', {
            'image': image,
            'duration': duration
        }, idx=idx)


class ScratchDisplayClearRequest(RPCRequest):

    def __init__(self, idx: str = None):
        super().__init__('scratch.display_clear', {}, idx=idx)


class ScratchCenterButtonLightRequest(RPCRequest):

    def __init__(self, color: int, idx: str = None):
        super().__init__('scratch.center_button_lights', {
            'color': color
        }, idx=idx)

class ScratchDisplayTextRequest(RPCRequest):

    def __init__(self, text: str, idx: str = None):
        super().__init__('scratch.display_text', {
            'text': text
        }, idx=idx)

class ScratchDisplayImageRequest(RPCRequest):

    def __init__(self, image: str = '00000\n00000\n00000\n00000\n00000', idx: str = None):
        super().__init__('scratch.display_image', {
            'image': image
        }, idx=idx)


class ScratchDisplayImageForRequest(RPCRequest):

    def __init__(self, image: str, duration: int, idx: str = None):
        super().__init__('scratch.display_image_for', {
            'image': image,
            'duration': duration
        }, idx=idx)


class ScratchDisplayClearRequest(RPCRequest):

    def __init__(self, idx: str = None):
        super().__init__('scratch.display_clear', {}, idx=idx)


class ScratchDisplaySetPixelRequest(RPCRequest):

    def __init__(self, x: int, y: int, brightness: int, idx: str = None):
        super().__init__('scratch.display_set_pixel', {
            'x': x,
            'y': y,
            'brightness': brightness
        }, idx=idx)


