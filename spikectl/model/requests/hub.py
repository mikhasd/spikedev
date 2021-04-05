from base64 import b64encode
from ujsonrpc import RPCRequest


class GetHubInfoRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'get_hub_info', {})


class StartWriteProgramRequest(RPCRequest):

    def __init__(self, idx: str, project_id: str, project_slot: int, name: str, project_type: str, size: str,
                 created: int, modified: int):
        super().__init__(idx, 'start_write_program', {
            'slotid': project_slot,
            'size': size,
            'meta': {
                'name': name,
                'project_id': project_id,
                'type': project_type,
                'created': created,
                'modified': modified
            }
        })


class StartWriteResourceRequest(RPCRequest):

    def __init__(self, idx: str, project_id: str, project_slot: int, name: str, project_type: str, size: str,
                 created: int, modified: int):
        super().__init__(idx, 'start_write_resource', {
            'slotid': project_slot,
            'size': size,
            'meta': {
                'name': name,
                'project_id': project_id,
                'type': project_type,
                'created': created,
                'modified': modified
            }
        })


class GetFirmwareInfoRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'get_firmware_info', {})


class TriggerCurrentStateRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'trigger_current_state', {})


class SetHubNameRequest(RPCRequest):

    def __init__(self, idx: str, name: str):
        super().__init__(idx, 'set_hub_name', {
            'name': b64encode(name)
        })


class WritePackageRequest(RPCRequest):

    def __init__(self, idx: str, data: str, transfer_id: int):
        super().__init__(idx, 'write_package', {
            'transferid': transfer_id,
            'data': data
        })


class ProgramTerminateRequest(RPCRequest):

    def __init__(self, idx: str):
        super().__init__(idx, 'program_terminate', {})


class ProgramExecuteRequest(RPCRequest):

    def __init__(self, idx: str, project_slot: int):
        super().__init__(idx, 'program_execute', {
            'slotid': project_slot
        })


class MoveProjectRequest(RPCRequest):

    def __init__(self, idx: str, old_slot: int, new_slot: int):
        super().__init__(idx, 'move_project', {
            'old_slotid': old_slot,
            'new_slotid': new_slot
        })


class SwitchModeRequest(RPCRequest):

    def __init__(self, idx: str, mode: str):
        """

        :param idx:
        :param mode: 'play' or 'download'
        """

        super().__init__(idx, 'program_modechange', {
            'mode': mode
        })

    @classmethod
    def play(idx: str) -> SwitchModeRequest:
        return SwitchModeRequest(idx, 'play')

    @classmethod
    def download(idx: str) -> SwitchModeRequest:
        return SwitchModeRequest(idx, 'download')


class SyncDisplayRequest(RPCRequest):

    def __init__(self, idx: str, sync: str):
        super().__init__(idx, 'sync_display', {
            'sync': sync
        })


class ScratchResetYawRequest(RPCRequest):

    def __init__(self, idx: str, sync: str):
        super().__init__(idx, 'scratch.reset_yaw', {})

        
class ResetProgramTimeRequest(RPCRequest):

    def __init__(self, idx: str, sync: str):
        super().__init__(idx, 'reset_program_time', {})

class StartProgramTimeRequest(RPCRequest):

    def __init__(self, idx: str, sync: str):
        super().__init__(idx, 'start_program_time', {})