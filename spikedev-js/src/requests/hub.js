import { RPCRequest } from '../ujsonrpc.js'

export class GetHubInfoRequest extends RPCRequest {
    constructor(idx) {
        super('get_hub_info', {}, idx)
    }
}

export class StartWriteProgramRequest extends RPCRequest {

    constructor(projectId, projectSlot, name, projectType, size, created, modified, idx = null) {
        super('start_write_program', {
            'slotid': projectSlot,
            'size': size,
            'meta': {
                'name': name,
                'project_id': projectId,
                'type': projectType,
                'created': created,
                'modified': modified
            }
        }, idx)
    }
}

export class StartWriteResourceRequest extends RPCRequest {
    constructor(project_id, project_slot, name, project_type, size, created, modified, idx = null) {
        super('start_write_resource', {
            'slotid': project_slot,
            'size': size,
            'meta': {
                'name': name,
                'project_id': project_id,
                'type': project_type,
                'created': created,
                'modified': modified
            }
        }, idx)
    }
}

export class GetFirmwareInfoRequest extends RPCRequest {
    constructor(idx = null) {
        super('get_firmware_info', {}, idx)
    }
}

export class TriggerCurrentStateRequest extends RPCRequest {

    constructor(idx = null) {
        super('trigger_current_state', {}, idx)
    }
}

export class SetHubNameRequest extends RPCRequest {
    constructor(name, idx = null) {
        super('set_hub_name', {
            'name': Buffer.from(name, 'ascii').toString('base64')
        }, idx)
    }
}

export class WritePackageRequest extends RPCRequest {
    constructor(data, transfer_id, idx = null) {
        super('write_package', {
            'transferid': transfer_id,
            'data': data
        }, idx)
    }
}

export class ProgramTerminateRequest extends RPCRequest {
    constructor(idx = null) {
        super('program_terminate', {}, idx)
    }
}

export class ProgramExecuteRequest extends RPCRequest {

    constructor(projectSlot, idx = null) {
        super('program_execute', {
            'slotid': projectSlot
        }, idx)
    }
}

export class MoveProjectRequest extends RPCRequest {

    constructor(oldSlot, newSlot, idx = null) {
        super('move_project', {
            'old_slotid': oldSlot,
            'new_slotid': newSlot
        }, idx)
    }
}

export class SwitchModeRequest extends RPCRequest {

    /**
     * 
     * @param {'play'|'download'} mode 
     * @param {string} [idx]
     */
    constructor(mode, idx = null) {
        super('program_execute', {
            'mode': mode
        }, idx)
    }

    static play(idx = null){
        return new SwitchModeRequest('play', idx)
    }

    static download(idx = null){
        return new SwitchModeRequest('download', idx)
    }
}

export class SyncDisplayRequest extends RPCRequest {
    /**
     * @param {string} sync
     * @param {string} [idx]
     */
    constructor(sync, idx = null) {
        super('sync_display', {
            'sync': sync
        }, idx)
    }
}

export class ScratchResetYawRequest extends RPCRequest {
    constructor(idx = null) {
        super('scratch.reset_yaw', {}, idx)
    }
}

export class ResetProgramTimeRequest extends RPCRequest {
    constructor(idx = null) {
        super('reset_program_time', {}, idx)
    }
}

export class StartProgramTimeRequest extends RPCRequest {
    constructor(idx = null) {
        super('start_program_time', {}, idx)
    }
}