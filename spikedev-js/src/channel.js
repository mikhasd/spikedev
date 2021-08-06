import SerialPort from 'serialport'
import {default as ReadLine} from '@serialport/parser-readline'
import * as ujsonrpc from './ujsonrpc.js'

const CR = '\r'

export class Channel {    
    /**
     * @type {SerialPort}
     */
    #serialPort = null
    /**
     * @callback RPCMessageListener
     * @param {ujsonrpc.RPCMessage} message
     * @returns {void}
     * 
     * @type {RPCMessageListener}
     */
    #listener = _ => null

    /**
     * Creates a new SpikeHub
     * @param {SerialPort} serialPort
     */
    constructor(serialPort){
        this.#serialPort = serialPort
        this.#installListener()
    }

    #installListener(){
        const me = this
        this.#serialPort.pipe(new ReadLine({
            delimiter: CR,
            encoding: 'utf8'
        }))        
        .on('data', data => {
            me.#onMessage(data)
        })
    }

    /**
     * React to an RPC message
     * @param {string} rawMessage
     */
    #onMessage(rawMessage){
        if(rawMessage[0] !== '{')
            return
        const jsonMessage = JSON.parse(rawMessage)
        const message = ujsonrpc.decode(jsonMessage)
        this.#listener(message)
    }

    /**
     * @param {ujsonrpc.RPCRequest} request
     * @returns {Promise<void>}
     */
    async send(request) {
        const encoded = request.encode()
        const message = encoded + CR
        return new Promise((resolve, reject)=>{
            this.#serialPort.write(message, err => {
                if(err){
                    reject(err)
                }else{
                    resolve()
                }
            })
        })
    }

    /**
     * 
     * @param {RPCMessageListener} listener 
     */
    setListener(listener) {
        if(listener){
            this.#listener = listener
        } else {
            throw new Error('listener must not be null')
        }
    }

    /**
     * Closes the connection with the SpikeHub.
     * 
     * @returns {Promise<Void>}
     */
    async close(){
        const me = this
        return new Promise((resolve, reject) => {
            me.#serialPort.close(err => {
                if(err){
                    reject(err)
                } else {
                    resolve()
                }
            })
        })        
    }

    /**
     * Opens an RPC channel for a given `path`
     * 
     * @param {string} path
     * @returns {Promise<Channel>}
     */
    static async open(path){
        let serialPort = new SerialPort(path, {
            autoOpen: false,
            baudRate: 115200,            
        })

        return new Promise((resolve, reject) => {
            serialPort.open(err => {
                if (err){
                    reject(err)
                } else {
                    resolve(new Channel(serialPort))
                }
            })
        })
    }
}