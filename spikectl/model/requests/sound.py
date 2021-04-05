from ujsonrpc import RPCRequest


class ScratchSoundBeepForTimeRequest(RPCRequest):

    def __init__(self, idx: str, duration: int, note: int, volume: int):
        super().__init__(idx, 'scratch.sound_beep_for_time', {
            'duration': duration,
            'note': note,
            'volume': volume,
        })