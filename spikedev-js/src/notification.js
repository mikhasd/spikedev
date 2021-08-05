import { RPCNotification } from "./ujsonrpc.js"

export class Notification {
    #timestamp = new Date()
    /**
     * @type {Object.<string, any>}
     */
    #source

    /**
     * @param {Object.<string, any>} source 
     */
    constructor(source) {
        this.#source = source
    }

    get source() {
        return this.#source
    }

    get timestamp() {
        return this.#timestamp
    }
}

export class UnknownNotification extends Notification {
    constructor(source){
        super(source)
    }
}

class ExternalSensorData {
    /**
     * @type {SensorType}
     */
    #type
    #data

    constructor(type, data){
        this.#type = type
        this.#data = data
    }
}

class MotorSensorData {
    #position

    #absolute_position

    constructor(position, absolute_position){
        this.#position = position
        this.#absolute_position = absolute_position
    }

    static decode(data){
        return new MotorSensorData(
            data[1],
            data[2]
        )
    }
}

const SensorData = {
    PortA: 0,
    PortB: 1,
    PortC: 2,
    PortD: 3,
    PortE: 4,
    PortF: 5,
    Accelerometer: 6,
    Gyroscope: 7,
    Position: 8,
    Display: 9,
    Time: 10,
}

function identity(arg0) {
    return arg0
}

class SensorType {
    /**
     * @type {number}
     */
    #idx
    /**
     * @type {number[]}
     */
    #modes
    /**
     * @type {(arg0: any) => any}
     */
    #decoder

    constructor(idx, modes = [0], decoder = identity) {
        this.#idx = idx
        this.#modes = modes
        this.#decoder = decoder
    }

    get idx(){
        return this.#idx
    }

    decode(data) {
        return this.#decoder(data)
    }
}

const LPF2_FLIPPER_MOTOR_SMALL = new SensorType(65, [1, 2, 3, 0], MotorSensorData.decode)
const LPF2_FLIPPER_MOTOR_MEDIUM = new SensorType(48, [1, 2, 3, 0], MotorSensorData.decode)
const LPF2_FLIPPER_MOTOR_LARGE = new SensorType(49, [1, 2, 3, 0], MotorSensorData.decode)
const LPF2_FLIPPER_COLOR = new SensorType(61, [1, 0])
const LPF2_FLIPPER_DISTANCE = new SensorType(62)
const LPF2_FLIPPER_FORCE = new SensorType(63, [0, 1, 4])
const LPF2_ACCELERATION = new SensorType(57)
const LPF2_GYRO = new SensorType(58)
const LPF2_ORIENTATION = new SensorType(59)
const LPF2_STONE_GREY_MOTOR_MEDIUM = new SensorType(75, [1, 2, 3, 0])
const LPF2_STONE_GREY_MOTOR_LARGE = new SensorType(76, [1, 2, 3, 0])

/**
 * @type {Map<number, SensorType>}
 */
const SensorTypes = (map => {
    [
        LPF2_FLIPPER_MOTOR_SMALL,
        LPF2_FLIPPER_MOTOR_MEDIUM,
        LPF2_FLIPPER_MOTOR_LARGE,
        LPF2_FLIPPER_COLOR,
        LPF2_FLIPPER_DISTANCE,
        LPF2_FLIPPER_FORCE,
        LPF2_ACCELERATION,
        LPF2_GYRO,
        LPF2_ORIENTATION,
        LPF2_STONE_GREY_MOTOR_MEDIUM,
        LPF2_STONE_GREY_MOTOR_LARGE
    ].forEach(type => map.set(type.idx, type))
    return map
})(new Map())

function formatExternalSensor(data, idx){
    const [typeIdx, values] = data[idx]
    const type = SensorTypes.get(typeIdx)
    if (!type)
        return null

    return new ExternalSensorData(
        type,
        type.decode(values)
    )
}

export class SensorNotification extends Notification {
    static method = 0
    #accelerometer
    #gyroscope
    #position
    #time
    #leds
    #a
    #b
    #c
    #d
    #e
    #f    

    constructor(source, accelerometer, gyroscope, position, time, leds, a, b, c, d, e, f) {
        super(source)
        this.#accelerometer = accelerometer
        this.#gyroscope = gyroscope
        this.#position = position
        this.#time = time
        this.#leds = leds
        this.#a = a
        this.#b= b
        this.#c = c
        this.#d = d
        this.#e = e
        this.#f = f
    }

    toString(){
        return `SensorNotification {timestamp: ${this.timestamp}, accelerometer: ${this.#accelerometer}, gyroscope: ${this.#gyroscope}, ` +
            `position: ${this.#position}, time: ${this.#time}, leds: ${this.#leds}, A: ${this.#a}, B: ${this.#b}, ` +
            `C: ${this.#c}, D: ${this.#d}, E: ${this.#e}, F: ${this.#f}}`
    }

    static decode(notification) {
        const data = notification.parameters
        const accelerometer = data[SensorData.Accelerometer]
        const gyroscope = data[SensorData.Gyroscope]
        const position = data[SensorData.Position]
        const time = data[SensorData.Time]
        const leds = data[SensorData.Display]
        const a = formatExternalSensor(data, SensorData.PortA)
        const b = formatExternalSensor(data, SensorData.PortB)
        const c = formatExternalSensor(data, SensorData.PortC)
        const d = formatExternalSensor(data, SensorData.PortD)
        const e = formatExternalSensor(data, SensorData.PortE)
        const f = formatExternalSensor(data, SensorData.PortF)
        return new SensorNotification(
            notification.parameters,
            accelerometer,
            gyroscope,
            position,
            time,
            leds,
            a,
            b,
            c,
            d,
            e,
            f
        )
    }
}

/**
 * StorageInformation
 * 
 * @typedef StorageInformation
 * @type {object}
 * 
 * Storage slot information
 * 
 * @typedef SlotInformation
 * @type {object}
 * @property {string} name
 * @property {string} id
 * @property {string} project_id
 * @property {number} modified
 * @property {string} type
 * @property {number} created
 * @property {number} size
 */

export class StorageInformationNotification extends Notification {

    static method = 1

    constructor(source) {
        super(source)
    }

    get total() {
        return this.source['total']
    }

    get available() {
        return this.source['available']
    }

    get pct() {
        return this.source['pct']
    }

    get unit() {
        return this.source['unit']
    }

    get slots() {
        return this.source['slots']
    }

    toString(){
        return `StorageInformationNotification {total: ${this.total}, available: ${this.available}, pct: ${this.pct}, unit: ${this.unit}, slots: ${this.slots}}`
    }

    static decode(notification) {
        const data = notification.parameters
        const storage = data['storage']
        return new StorageInformationNotification(
            storage
        )
    }
}

const BATTERY_VOLTAGE_IDX = 0
const BATTERY_PERCENTAGE_IDX = 1

export class BatteryStatusNotification extends Notification {
    static method = 2

    constructor(source) {
        super(source)
    }

    get voltage() {
        return this.source[BATTERY_VOLTAGE_IDX]
    }

    get percentage() {
        return this.source[BATTERY_PERCENTAGE_IDX]
    }

    toString(){
        return `BatteryStatusNotification {voltage: ${this.voltage}, percentage: ${this.percentage}}`
    }

    static decode(notification) {        
        return new BatteryStatusNotification(notification.parameters)
    }
}


/**
 * @typedef {string|number} MethodKey
 * 
 * @typedef {(arg0: RPCNotification)=>any} NotificationDecoder
 * /
 * 
 /**
 * @type {Map<MethodKey, NotificationDecoder>}
 */
const decoders = new Map(
    [
        SensorNotification,
        StorageInformationNotification,
        BatteryStatusNotification
    ].map(type => [type.method, type.decode])
)

/**
 * 
 * @param {RPCNotification} rpcNotification
 * @returns {Notification}
 */
export function decode(rpcNotification) {
    const method = rpcNotification.method
    const decoder = decoders.get(method)
    if (decoder) {
        return decoder(rpcNotification)
    } else {
        return new UnknownNotification(rpcNotification)
    }
}
