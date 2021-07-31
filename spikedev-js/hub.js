import SerialPort from 'serialport'
import {default as enumerate} from './enumerate.js'

export class SpikeHub {
    
    /**
     * Creates a new SpikeHub
     * @param {import('./enumerate.js').DeviceId} deviceId 
     */
    constructor(deviceId){
        this.serialDevice = new SerialPort(deviceId.path)
    }

    static async find(){
        const devices = await enumerate()
        if(devices.length < 1) {
            throw new Error('No SpikeHub device found')
        } else if(devices.length > 1) {
            throw new Error(`${devices.length} SpikeHub devices found. Try unsing 'enumerate()'`)
        }
        return new SpikeHub(devices[0])
    }
}