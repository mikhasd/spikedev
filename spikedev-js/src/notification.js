import { RPCNotification } from "./ujsonrpc.js"

export class Notification {
    /**
     * @type {RPCNotification}
     */
    #source

    /**
     * @param {RPCNotification} source 
     */
    constructor(source) {
        this.#source = source
    }

    /**
     * @returns {RPCNotification}
     */
    get source() {
        return this.#source
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
        return `SensorNotification {accelerometer: ${this.#accelerometer}, gyroscope: ${this.#gyroscope}, ` +
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
            notification,
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

    get #data(){
        return this.source.parameters.data
    }

    get total() {
        return this.#data['total']
    }

    get available() {
        return this.#data['available']
    }

    get pct() {
        return this.#data['pct']
    }

    get unit() {
        return this.#data['unit']
    }

    get slots() {
        return this.#data['slots']
    }

    toString(){
        return `StorageInformationNotification {total: ${this.total}, available: ${this.available}, pct: ${this.pct}, unit: ${this.unit}, slots: ${this.slots}}`
    }

    static decode(notification) {        
        return new StorageInformationNotification(
            notification
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
        return this.source.parameters[BATTERY_VOLTAGE_IDX]
    }

    get percentage() {
        return this.source.parameters[BATTERY_PERCENTAGE_IDX]
    }

    toString(){
        return `BatteryStatusNotification {voltage: ${this.voltage}, percentage: ${this.percentage}}`
    }

    static decode(notification) {        
        return new BatteryStatusNotification(notification)
    }
}

const BUTTON_BUTTON_IDX = 0
const BUTTON_STATE_IDX = 1

export class ButtonNotification extends Notification {
    static method = 3

    constructor(source) {
        super(source)
    }

    get button() {
        return this.source.parameters[BUTTON_BUTTON_IDX]
    }

    get state() {
        return this.source.parameters[BUTTON_STATE_IDX] > 0
    }

    toString(){
        return `ButtonNotification {button: ${this.button}, state: ${this.state}}`
    }

    static decode(notification) {        
        return new ButtonNotification(notification)
    }
}

export class GestureNotification extends Notification {
    static method = 4

    constructor(source) {
        super(source)
    }

    get gesture() {
        return this.source.parameters
    }

    toString(){
        return `GestureNotification {gesture: ${this.gesture}}`
    }

    static decode(notification) {        
        return new GestureNotification(notification)
    }
}

export class DisplayStatusNotification extends Notification {
    static method = 5

    constructor(source) {
        super(source)
    }

    toString(){
        return `DisplayStatusNotification {}`
    }

    static decode(notification) {        
        return new DisplayStatusNotification(notification)
    }
}

const FIRMWARE_VERSION_IDX = 0
const FIRMWARE_HASH_IDX = 1
const FIRMWARE_RUNTIME_IDX = 2

export class FirmwareNotification extends Notification {
    static method = 6

    constructor(source) {
        super(source)
    }

    get version(){
        return this.source.parameters[FIRMWARE_VERSION_IDX]
    }

    get hash(){
        return this.source.parameters[FIRMWARE_HASH_IDX]
    }

    get runtime(){
        return this.source.parameters[FIRMWARE_RUNTIME_IDX]
    }

    toString(){
        return `FirmwareNotification {version: ${this.version}, hash: ${this.hash}, runtime: ${this.runtime}}`
    }

    static decode(notification) {        
        return new FirmwareNotification(notification)
    }
}

export class StackStartNotification extends Notification {
    static method = 7

    constructor(source) {
        super(source)
    }

    get stack() {
        return this.source.parameters
    }

    toString(){
        return `StackStartNotification {stack: ${this.stack}}`
    }

    static decode(notification) {        
        return new StackStartNotification(notification)
    }
}

export class StackStopNotification extends Notification {
    static method = 8

    constructor(source) {
        super(source)
    }

    get stack() {
        return this.source.parameters
    }

    toString(){
        return `StackStopNotification {stack: ${this.stack}}`
    }

    static decode(notification) {        
        return new StackStopNotification(notification)
    }
}

export class InfoNotification extends Notification {
    static method = 9

    #name

    constructor(source, name){
        super(source)
        this.#name = name
    }

    get name(){
        return this.#name
    }

    toString(){
        return `InfoNotification {name: ${this.name}}`
    }

    static decode(notification){
        const [encodedName] = notification.parameters
        const name = Buffer.from(encodedName, 'base64')
        return new InfoNotification(notification, name)
    }
}

const ERROR_TYPE_IDX = 0
const ERROR_MESSAGE_IDX = 1

export class ErrorNotification extends Notification {
    static method = 10

    constructor(source) {
        super(source)
    }

    get type() {
        return this.source.parameters[ERROR_TYPE_IDX]
    }

    get message() {
        return this.source.parameters[ERROR_MESSAGE_IDX]
    }

    toString(){
        return `ErrorNotification {type: ${this.type}, message: ${this.message}}`
    }

    static decode(notification) {        
        return new ErrorNotification(notification)
    }
}

const VM_STATE_TARGET_IDX = 0
const VM_STATE_VARIABLES_IDX = 1
const VM_STATE_LIST_IDX = 2
const VM_STATE_STORE_IDX = 3

export class VMStateNotification extends Notification {
    static method = 11

    constructor(source) {
        super(source)
    }

    get target() {
        return this.source.parameters[VM_STATE_TARGET_IDX]
    }

    get variables() {
        return this.source.parameters[VM_STATE_VARIABLES_IDX]
    }

    get list() {
        return this.source.parameters[VM_STATE_LIST_IDX]
    }

    get store() {
        return this.source.parameters[VM_STATE_STORE_IDX]
    }    

    toString(){
        return `VMStateNotification {target: ${this.target}, variables: ${this.variables}, list: ${this.list}, store: ${this.store}}`
    }

    static decode(notification) {        
        return new VMStateNotification(notification)
    }
}

const PROGRAM_PROJECT_IDX = 0
const PROGRAM_RUNNING_IDX = 1

export class ProgramRunningNotification extends Notification {
    static method = 12

    constructor(source) {
        super(source)
    }

    get project() {
        return this.source.parameters[PROGRAM_PROJECT_IDX]
    }

    get running() {
        return this.source.parameters[PROGRAM_RUNNING_IDX]
    }

    toString(){
        return `ProgramRunningNotification {project: ${this.project}, running: ${this.running}}`
    }

    static decode(notification) {        
        return new ProgramRunningNotification(notification)
    }
}

export class UserProgramPrintNotification extends Notification {
    static method = 'userProgram.print'

    constructor(source) {
        super(source)
    }

    toString(){
        return `UserProgramPrintNotification {source: ${this.source}}`
    }

    static decode(notification) {        
        return new UserProgramPrintNotification(notification)
    }
}

const RUNTIME_ERROR_STACKTRACE_IDX = 3

export class RuntimeErrorNorification extends Notification {
    static method = 'runtime_error'

    #stacktrace

    constructor(source, stacktrace) {
        super(source)
        this.#stacktrace = stacktrace
    }

    get stackTrace(){
        return this.#stacktrace
    }

    toString(){
        return `RuntimeErrorNorification {source: ${this.source}}`
    }

    static decode(notification) {
        const encodedStackTrace = notification.parameters[RUNTIME_ERROR_STACKTRACE_IDX]
        const stacktrace = Buffer.from(encodedStackTrace, 'base64').toString()
        return new RuntimeErrorNorification(notification, stacktrace)
    }
}

/**
 * @typedef {string|number} MethodKey
 * 
 * @typedef {(arg0: RPCNotification)=>Notification} NotificationDecoder
 * /
 * 
 /**
 * @type {Map<MethodKey, NotificationDecoder>}
 */
const decoders = new Map(
    [
        SensorNotification,
        StorageInformationNotification,
        BatteryStatusNotification,
        ButtonNotification,
        GestureNotification,
        DisplayStatusNotification,
        FirmwareNotification,
        StackStartNotification,
        StackStopNotification,
        InfoNotification,
        ErrorNotification,
        VMStateNotification,
        ProgramRunningNotification,
        RuntimeErrorNorification,
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
