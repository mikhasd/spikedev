from spikectl.model.notifications import SensorNotification
from typing import List, Tuple
import spikectl
import spikectl.model
import time

def calculate_gear_ratio(first: int, axes: List[Tuple[int, int]], last: int) -> float:
    r = 1.0
    prev = first
    for (input_gear, output_gear) in axes:
        r = r * (input_gear / prev)
        prev = output_gear        
    
    r = r * (last / prev)
    return r

def main():
    spike_hub = spikectl.find_hub('mp8')    
    
    wrist_angle_motor = spike_hub.motor('D')
    wrist_angle_ratio = calculate_gear_ratio(8, [(24, 16), (16, 12), (12, 12)], 60)
    
    wrist_rotation_motor = spike_hub.motor('F')
    wrist_rotation_ratio = calculate_gear_ratio(16, [(16, 12)], 60)
    
    angle_vs_rotation_ratio = wrist_angle_ratio / wrist_rotation_ratio

    hand_motor = spike_hub.motor('B')
    

    try:
        print(spike_hub.listen_notification(SensorNotification).B)
        
        #for _ in range(12):
        degress = 180        
        hand_motor.rotate(-100, 2900)

        print(spike_hub.listen_notification(SensorNotification).B)

        hand_motor.rotate(-85, 1111)


        hand_motor.go_to(100, 0)

        print(spike_hub.listen_notification(SensorNotification).B)
        

        print(spike_hub.listen_notification(SensorNotification).B)
        
    except KeyboardInterrupt:
        wrist_rotation_motor.stop()
        wrist_angle_motor.stop()

    spike_hub.close()


main()