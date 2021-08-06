import { Channel } from './channel.js'
import * as ujsonrpc from './ujsonrpc.js'
import { default as enumerate } from './enumerate.js'
import { decode as decodeNotification } from './notification.js'
import * as requests from './requests.js'

const MAX_PARALLEL_REQUESTS = 12

function isInRange(low, value, high) {
    return value >= low || value <= high
}

export class SpikeHub {
    /**
     * @type {Channel}
     */
    #channel

    /**
     * @typedef FutureRequest
     * @type {object}
     * @property {ujsonrpc.RPCRequest} request
     * @property {(err?: Error)=>void} callback
     */

    /**
     * @type {FutureRequest[]}
     */
    #queue = []

    #notificationListeners = new Set()

    /**
     * @type {Map<string, (err?: Error)=>void>}
     */
    #responseListener = new Map()

    /**
     * 
     * @param {Channel} channel 
     */
    constructor(channel) {
        this.#channel = channel
        channel.setListener(msg => {
            this.#onMessage(msg)
        })
    }

    /**
     * 
     * @param {ujsonrpc.RPCMessage} message 
     */
    #onMessage(message) {
        if (message.isNotification()) {
            // @ts-ignore
            this.#onNotification(message)
        } else if (message.isResponse()) {
            // @ts-ignore
            this.#onResponse(message)
        } else if (message.isError()) {
            console.warn('Unexpected message received', message)
        } else {
            console.warn('unexpected message', message)
        }
    }

    /**
     * @param {ujsonrpc.RPCNotification} rpcNotification
     */
    #onNotification(rpcNotification) {
        const notification = decodeNotification(rpcNotification)
        for (const listener of this.#notificationListeners) {
            listener(notification)
        }
    }

    /**
     * 
     * @param {ujsonrpc.RPCResponse} rpcResponse 
     */
    #onResponse(rpcResponse) {
        const idx = rpcResponse.idx
        const callback = this.#responseListener.get(idx)
        if (callback) {
            callback()
        } else {
            console.warn('unhandled response', idx)
        }
    }


    listen(listener) {
        this.#notificationListeners.add(listener)
        const hub = this
        return function removeListener() {
            hub.#notificationListeners.delete(listener)
        }
    }

    async #awaitResponse(idx) {
        return new Promise((resolve, reject) => {
            /*
            const timeout = setTimeout(() => {
                if (this.#responseListener.delete(idx)) {
                    reject(new Error('timeout'))
                }
            }, 100)
            */

            this.#responseListener.set(idx, err => {
                this.#responseListener.delete(idx)
                if (err) {
                    reject(err)
                } else {
                    resolve()
                }
                //clearTimeout(timeout)
            })

        })

    }

    /**
     * @param {ujsonrpc.RPCRequest} request 
     */
    async #doInvoke(request, callback) {        
        try{
            const response = this.#awaitResponse(request.idx)
            await this.#channel.send(request)
            await response
            callback()
        } catch(err) {
            callback(err)
        }
    }

    async #consumeQueue(){
        while (this.#queue.length) {
            const {request, callback} = this.#queue.shift()            
            await this.#doInvoke(request, callback)
        }
    }

    async #enqueueInvokation(request, callback) {
        if (this.#responseListener.size <= MAX_PARALLEL_REQUESTS) {
            await this.#doInvoke(request, callback)
            await this.#consumeQueue()
        } else {
            this.#queue.push({
                request,
                callback
            })
        }
    }

    async invoke(request) {
        return new Promise((resolve, reject) => {
            this.#enqueueInvokation(request, err => {
                if (err) {
                    reject(err)
                } else {
                    resolve()
                }
            })
        })
    }

    async setButtonColor(color = 0){
        if(!isInRange(0, color, 10)){
            throw new Error(`color=${color} must be between 0 and 10`)
        }
        const request = new requests.ScratchCenterButtonLightRequest(color)
        await this.invoke(request)
    }

    display() {
        return new Display(this)
    }

    async close() {
        return await this.#channel.close()
    }

    /**
     * Creates an SpikeHub for a given serial `port`.
     * 
     * If a `port` is not provided, this function will search for an available hub.
     * 
     * If more than one hub is available, this function will fail.
     * 
     * @param {string} [port] serial port where the hub is located.
     */
    static async create(port) {
        if (!port) {
            const devices = await enumerate()
            if (devices.length < 1) {
                throw new Error('No SpikeHub device found')
            } else if (devices.length > 1) {
                throw new Error(`${devices.length} SpikeHub devices found. Try using 'enumerate()'`)
            }
            port = devices[0].path
        }

        const channel = await Channel.open(port)
        return new SpikeHub(channel)
    }
}

function isPixelInRange(pixel) {
    return pixel >= 0 && pixel <= 4
}

export class Display {
    /**
     * @type {SpikeHub}
     */
    #hub

    /**
     * @param {SpikeHub} hub
     */
    constructor(hub) {
        this.#hub = hub
    }

    async clear() {
        const request = new requests.ScratchDisplayClearRequest()
        await this.#hub.invoke(request)
    }

    async setPixel(x, y, brightness) {
        if (!isPixelInRange(x) || !isPixelInRange(y)) {
            throw new Error(`x=${x} and y=${y} must be between 0 and 4`)
        }
        const request = new requests.ScratchDisplaySetPixelRequest(x, y, brightness)
        await this.#hub.invoke(request)
    }

    /**
     * @param {string} image 
     * @param {number} [duration]
     */
    async displayImage(image, duration = 0){
        if(!image.match(/^\d{5}\s\d{5}\s\d{5}\s\d{5}\s\d{5}/))
            throw new Error(`invalid image provided: ${image}`)
        
        let request
        if(duration){
            request = new requests.ScratchDisplayImageForRequest(image, duration)
        } else {
            request = new requests.ScratchDisplayImageRequest(image)
        }        
        await this.#hub.invoke(request)
    }

    async displayText(text){        
        const request = new requests.ScratchDisplayTextRequest(text)
        await this.#hub.invoke(request)
    }
}