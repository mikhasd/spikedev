from __future__ import annotations

from base64 import b64encode
from spikectl.ujsonrpc import RPCRequest


class GetHubInfoRequest(RPCRequest):

    def __init__(self, idx: str = None):
        super().__init__('get_hub_info', {}, idx=idx)


class StartWriteProgramRequest(RPCRequest):

    def __init__(self, project_id: str, project_slot: int, name: str, project_type: str, size: str,
                 created: int, modified: int, idx: str = None):
        super().__init__('start_write_program', {
            'slotid': project_slot,
            'size': size,
            'meta': {
                'name': name,
                'project_id': project_id,
                'type': project_type,
                'created': created,
                'modified': modified
            }
        }, idx=idx)


class StartWriteResourceRequest(RPCRequest):

    def __init__(self, project_id: str, project_slot: int, name: str, project_type: str, size: str,
                 created: int, modified: int, idx: str = None):
        super().__init__('start_write_resource', {
            'slotid': project_slot,
            'size': size,
            'meta': {
                'name': name,
                'project_id': project_id,
                'type': project_type,
                'created': created,
                'modified': modified
            }
        }, idx=idx)


class GetFirmwareInfoRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__('get_firmware_info', {}, idx=idx)


class TriggerCurrentStateRequest(RPCRequest):

    def __init__(self, idx: str=None):
        super().__init__('trigger_current_state', {}, idx=idx)


class SetHubNameRequest(RPCRequest):

    def __init__(self, name: str, idx: str = None):
        super().__init__('set_hub_name', {
            'name': b64encode(name)
        }, idx=idx)


class WritePackageRequest(RPCRequest):

    def __init__(self, data: str, transfer_id: int, idx: str = None):
        super().__init__('write_package', {
            'transferid': transfer_id,
            'data': data
        }, idx=idx)


class ProgramTerminateRequest(RPCRequest):

    def __init__(self, idx: str = None):
        super().__init__('program_terminate', {}, idx=idx)


class ProgramExecuteRequest(RPCRequest):

    def __init__(self, project_slot: int, idx: str = None):
        super().__init__('program_execute', {
            'slotid': project_slot
        }, idx=idx)


class MoveProjectRequest(RPCRequest):

    def __init__(self, old_slot: int, new_slot: int, idx: str = None):
        super().__init__('move_project', {
            'old_slotid': old_slot,
            'new_slotid': new_slot
        }, idx=idx)


class SwitchModeRequest(RPCRequest):

    def __init__(self, mode: str, idx: str = None):
        """

        :param idx:
        :param mode: 'play' or 'download'
        """

        super().__init__('program_modechange', {
            'mode': mode
        }, idx=idx)

    @classmethod
    def play(idx: str = None) -> SwitchModeRequest:
        return SwitchModeRequest('play', idx=idx)

    @classmethod
    def download(idx: str = None) -> SwitchModeRequest:
        return SwitchModeRequest('download', idx=idx)


class SyncDisplayRequest(RPCRequest):

    def __init__(self, sync: str, idx: str = None):
        super().__init__('sync_display', {
            'sync': sync
        }, idx=idx)


class ScratchResetYawRequest(RPCRequest):

    def __init__(self, sync: str, idx: str = None):
        super().__init__('scratch.reset_yaw', {}, idx=idx)

        
class ResetProgramTimeRequest(RPCRequest):

    def __init__(self, sync: str, idx: str = None):
        super().__init__('reset_program_time', {}, idx=idx)

class StartProgramTimeRequest(RPCRequest):

    def __init__(self, sync: str, idx: str = None):
        super().__init__('start_program_time', {}, idx=idx)