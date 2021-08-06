import { RPCRequest } from '../ujsonrpc.js'

export class ScratchSoundBeepForTimeRequest extends RPCRequest {

    constructor(duration, note, volume, idx = null){
        super('scratch.sound_beep_for_time', {
            'duration': duration,
            'note': note,
            'volume': volume,
        }, idx)
    }
}