from base64 import b64encode


class BaseRequest:

    def __init__(self, idx: str, method: str, parameters: any):
        self.idx = idx
        self.method = method
        self.parameters = parameters


class StartWriteProgramRequest(BaseRequest):

    def __init__(self, idx: str, project_id: str, project_slot: int, name: str, project_type: str, size: str,
                 created: int, modified: int):
        super(BaseRequest, self).__init__(idx, 'start_write_program', {
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


class StartWriteResourceRequest(BaseRequest):

    def __init__(self, idx: str, project_id: str, project_slot: int, name: str, project_type: str, size: str,
                 created: int, modified: int):
        super(BaseRequest, self).__init__(idx, 'start_write_resource', {
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


class GetFirmwareInfoRequest(BaseRequest):

    def __init__(self, idx: str):
        super(BaseRequest, self).__init__(idx, 'get_firmware_info', {})


class TriggerCurrentStateRequest(BaseRequest):

    def __init__(self, idx: str):
        super(BaseRequest, self).__init__(idx, 'trigger_current_state', {})


class SetHubNameRequest(BaseRequest):

    def __init__(self, idx: str, name: str):
        super(BaseRequest, self).__init__(idx, 'set_hub_name', {
            'name': b64encode(name)
        })


class WritePackageRequest(BaseRequest):

    def __init__(self, idx: str, data: str, transfer_id: int):
        super(BaseRequest, self).__init__(idx, 'write_package', {
            'transferid': transfer_id,
            'data': data
        })


class ProgramTerminateRequest(BaseRequest):

    def __init__(self, idx: str):
        super(BaseRequest, self).__init__(idx, 'program_terminate', {})


class ProgramExecuteRequest(BaseRequest):

    def __init__(self, idx: str, project_slot: int):
        super(BaseRequest, self).__init__(idx, 'program_execute', {
            'slotid': project_slot
        })


class MoveProjectRequest(BaseRequest):

    def __init__(self, idx: str, old_slot: int, new_slot: int):
        super(BaseRequest, self).__init__(idx, 'move_project', {
            'old_slotid': old_slot,
            'new_slotid': new_slot
        })


class SwitchModeRequest(BaseRequest):

    def __init__(self, idx: str, mode: str):
        """

        :param idx:
        :param mode: 'play' or 'download'
        """

        super(BaseRequest, self).__init__(idx, 'program_modechange', {
            'mode': mode
        })


class SyncDisplayRequest(BaseRequest):

    def __init__(self, idx: str, sync: str):
        super(BaseRequest, self).__init__(idx, 'sync_display', {
            'sync': sync
        })


class ScratchDisplayClearRequest(BaseRequest):

    def __init__(self, idx: str):
        super(BaseRequest, self).__init__(idx, 'scratch.display_clear', {})


class ScratchDisplaySetPixelRequest(BaseRequest):

    def __init__(self, idx: str, x: int, y: int, brightness: int):
        super(BaseRequest, self).__init__(idx, 'scratch.display_set_pixel', {
            'x': x,
            'y': y,
            'brightness': brightness
        })


class ScratchDisplayImageRequest(BaseRequest):

    def __init__(self, idx: str, image: str):
        super(BaseRequest, self).__init__(idx, 'scratch.display_image', {
            'image': image
        })


class ScratchDisplayImageForRequest(BaseRequest):

    def __init__(self, idx: str, image: str, duration: int):
        super(BaseRequest, self).__init__(idx, 'scratch.display_image_for', {
            'image': image,
            'duration': duration
        })


class ScratchCenterButtonLightRequest(BaseRequest):

    def __init__(self, idx: str, color: int):
        super(BaseRequest, self).__init__(idx, 'scratch.center_button_lights', {
            'color': color
        })
