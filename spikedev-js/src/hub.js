import { Channel } from './channel.js'
import { RPCMessage } from './ujsonrpc.js'
import { default as enumerate } from './enumerate.js'
import {decode as decodeNotification} from './notification.js'

export class SpikeHub {
    /**
     * @type {Channel}
     */
    #channel

    #notificationListeners = []

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
     * @param {RPCMessage} message 
     */
    #onMessage(message){
        if(message.isNotification()){
            const notification = decodeNotification(message)
            for (const listener of this.#notificationListeners) {
                listener(notification)
            }
        } else {
            console.info('got message', message)
        }
    }


    listen(listener){
        this.#notificationListeners.push(listener)
    }

    async close(){
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