import { default as bindings }  from '@serialport/bindings';

/**
 * A Serial device Id.
 * 
 * @typedef DeviceId
 * @type {object}
 * @property {string} manufacturer
 * @property {string} serialNumber
 * @property {string} pnpId
 * @property {string} locationId
 * @property {string} vendorId
 * @property {string} productId
 * @property {string} path
 */

const LEGO_SPIKEHUB_VENDOR_ID = '0694'
const LEGO_SPIKEHUB_PRODUCT_ID = '0009'

/**
 * Checks if provided device Id is a Lego Spike Hub device.
 * 
 * @param {DeviceId} device 
 * @returns {boolean}
 */
function isLegoDevice(device){
    return device.productId === LEGO_SPIKEHUB_PRODUCT_ID && device.vendorId === LEGO_SPIKEHUB_VENDOR_ID
}

/**
 * 
 * @returns {Promise<DeviceId[]>} 
 */
export default async function enumerate(){
    /**
     * @type {DeviceId[]}
     */
    const devices = await bindings.list()
    return devices.filter(isLegoDevice)
}