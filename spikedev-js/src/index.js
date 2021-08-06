//import * as SerialPort from 'serialport'
import { SpikeHub } from './hub.js'
import { RuntimeErrorNorification } from './notification.js'

async function wait(time){
    return new Promise(resolve => {
        setTimeout(resolve, time)
    })
}

async function main() {
    const hub = await SpikeHub.create()
    const display = hub.display()
    const tasks = []
    let start = 0

    hub.listen(not => {
        if (not instanceof RuntimeErrorNorification) {
            console.warn(not.stackTrace)
        }
    })
    display.clear()
    for (let y = start; y < 5; y++) {
        for (let x = start; x < 5; x++) {
            tasks.push(display.setPixel(x, y, x + y + 1))

        }
    }
    console.info('requests sent')
    try {
        await Promise.allSettled(tasks)
    } catch (err) {
        console.warn(err)
    }
    console.info('requewts done')

    await display.displayImage('09090\n98989\n98789\n09890\n00900')
    console.info('das')

    await wait(2000)

    for(let color=0; color <= 10; color ++){
        console.info('color', color)
        await hub.setButtonColor(color)
        await wait(100)
    }

    setTimeout(async () => {
        console.info('cleaning display')
        await hub.display().clear()
        console.info('display clean')
        await hub.close()
    }, 2500)
}

main()