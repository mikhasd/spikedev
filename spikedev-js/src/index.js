//import * as SerialPort from 'serialport'
import { SpikeHub }  from './hub.js'
import { BatteryStatusNotification } from './notification.js'

async function main(){
    const hub = await SpikeHub.create()
    hub.listen(not => {
        if(not instanceof BatteryStatusNotification)
            console.info('notification', not.toString())
    })

    setTimeout(() => {
        hub.close()
    }, 5000)
}

main()