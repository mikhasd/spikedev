//import * as SerialPort from 'serialport'
import { SpikeHub }  from './hub.js'

async function main(){
    const hub = await SpikeHub.find()
    console.info(hub)
}

main()