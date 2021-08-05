import { Transform } from 'stream'

const RPC_KEY_ID = 'i'
const RPC_KEY_METHOD = 'm'
const RPC_KEY_RESULT = 'r'
const RPC_KEY_ERROR = 'e'
const RPC_KEY_PARAMETERS = 'p'

export class RPCMessage {
    /**
     * @returns {boolean}
     */
    isError() {
        return false
    }
    /**
     * @returns {boolean}
     */
    isResponse() {
        return false
    }
    /**
     * @returns {boolean}
     */
    isRequest() {
        return false
    }
    /**
     * @returns {boolean}
     */
    isNotification() {
        return false
    }
}

export class RPCNotification extends RPCMessage {
    /**
     * 
         * @param {number|string} method 
         * @param {any} parameters 
         */
    constructor(method, parameters) {
        super()
        this.method = method
        this.parameters = parameters
    }

    isNotification() {
        return true
    }
}

export class RPCError extends RPCMessage {
    /**
     * @param {string} idx 
     * @param {string} exceptionData 
     */
    constructor(idx, exceptionData) {
        super()
        this.idx = idx
        let decoded = Buffer.from(exceptionData)
        this.exceptionData = decoded.toString('utf8')
    }

    isError() {
        return true
    }
}

export class RPCResponse extends RPCMessage {
    /**
     * @param {string} idx 
     * @param {any} result 
     */
    constructor(idx, result) {
        super()
        this.idx = idx
        this.result = result
    }

    isResponse() {
        return true
    }
}

/**
 * @returns {string}
 */
function genIdx() {
    return Math.random().toString(36).substring(2, 6)
}

export class RPCRequest extends RPCMessage {
    /**
     * 
     * @param {string} method 
     * @param {any} parameters 
     * @param {string?} idx 
     */
    constructor(method, parameters, idx = genIdx()) {
        super()
        this.idx = idx
        this.method = method
        this.parameters = parameters
    }

    isRequest() {
        return true
    }

    encode() {
        return JSON.stringify({
            RPC_KEY_ID: this.idx,
            RPC_KEY_METHOD: this.method,
            RPC_KEY_PARAMETERS: this.parameters
        })
    }
}

/**
 * 
 * @param {Object.<string, any>} msg
 * @returns {boolean}
 */
function isRequest(msg) {
    return RPC_KEY_ID in msg && RPC_KEY_METHOD in msg && RPC_KEY_PARAMETERS in msg
}

/**
 * 
 * @param {Object.<string, any>} msg
 * @returns {boolean}
 */
function isResponse(msg) {
    return RPC_KEY_ID in msg && RPC_KEY_RESULT in msg
}

/**
 * 
 * @param {Object.<string, any>} msg
 * @returns {boolean}
 */
function isError(msg) {
    return RPC_KEY_ID in msg && RPC_KEY_ERROR in msg
}

/**
 * 
 * @param {Object.<string, any>} msg
 * @returns {boolean}
 */
function isNotification(msg) {
    return RPC_KEY_METHOD in msg && RPC_KEY_PARAMETERS in msg && !(RPC_KEY_ID in msg)
}

/**
 * 
 * @param {Object.<string, any>} msg
 * @returns {RPCMessage}
 */
export function decode(msg) {
    if (isNotification(msg)) {
        const method = msg[RPC_KEY_METHOD]
        const parameters = msg[RPC_KEY_PARAMETERS]
        return new RPCNotification(method, parameters)
    } else if (isResponse(msg)) {
        const idx = msg[RPC_KEY_ID]
        const result = msg[RPC_KEY_RESULT]
        return new RPCResponse(idx, result)
    } else if (isError(msg)) {
        const idx = msg[RPC_KEY_ID]
        const error = msg[RPC_KEY_ERROR]
        return new RPCError(idx, error)
    } else if (isRequest(msg)) {
        const idx = msg[RPC_KEY_ID]
        const method = msg[RPC_KEY_METHOD]
        const parameters = msg[RPC_KEY_PARAMETERS]
        return new RPCRequest(idx, method, parameters)
    }
    throw new Error(`Unexcpected message type: ${msg}`)
}
