import { RPCRequest } from '../ujsonrpc.js'


export class ScratchDisplaySetPixelRequest extends RPCRequest {

    constructor(x, y, brightness, idx = null) {
        super('scratch.display_set_pixel', {
            'x': x,
            'y': y,
            'brightness': brightness
        }, idx)
    }
}

export class ScratchDisplayClearRequest extends RPCRequest {

    constructor(idx = null) {
        super('scratch.display_clear', {}, idx)
    }
}

export class ScratchCenterButtonLightRequest extends RPCRequest {

    constructor(color, idx = null) {
        super('scratch.center_button_lights', {
            'color': color
        }, idx)
    }
}

export class ScratchDisplayTextRequest extends RPCRequest {

    constructor(text, idx = null) {
        super('scratch.display_text', {
            'text': text
        }, idx)
    }
}

export class ScratchDisplayImageRequest extends RPCRequest {

    constructor(image = '00000\n00000\n00000\n00000\n00000', idx = null) {
        super('scratch.display_image', {
            'image': image
        }, idx)
    }
}

export class ScratchDisplayImageForRequest extends RPCRequest {

    constructor(image, duration, idx = null) {
        super('scratch.display_image_for', {
            'image': image,
            'duration': duration
        }, idx)
    }
}