from spikectl.model.notifications import MotorSensorData, SensorNotification
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
    tower_motor = spike_hub.motor('E')
    
    motors = [wrist_angle_motor, wrist_rotation_motor, hand_motor]

    try:
        
        spike_hub.wait(*[ motor.go_to(100, 0) for motor in motors])
        spike_hub.wait(*[ motor.set_current_position(0) for motor in motors])

        angle = 210
        
        spike_hub.wait(
            hand_motor.rotate(100, 360)
        )
        spike_hub.wait(            
            hand_motor.rotate(-100, 360)
        )

        spike_hub.wait(
            hand_motor.rotate((-100/wrist_angle_ratio) * 1.666666, 150),
            wrist_angle_motor.rotate(100, 90 * wrist_angle_ratio)
        )

        spike_hub.wait(
            hand_motor.rotate((100/wrist_angle_ratio) * 1.666666, 150),
            wrist_angle_motor.rotate(-100, 90 * wrist_angle_ratio)
        )
        
        spike_hub.wait(
            wrist_angle_motor.rotate(100 * (angle_vs_rotation_ratio / wrist_rotation_ratio), angle * angle_vs_rotation_ratio * 0.5),
            wrist_rotation_motor.rotate(100, angle * wrist_rotation_ratio * 0.5),
            hand_motor.rotate(-100 * (1 / wrist_rotation_ratio), angle* 0.5)
        )
        
        spike_hub.wait(
            wrist_angle_motor.rotate(-100 * float(angle_vs_rotation_ratio / wrist_rotation_ratio), angle * angle_vs_rotation_ratio),
            wrist_rotation_motor.rotate(-100, angle * wrist_rotation_ratio),
            hand_motor.rotate(100 * (1 / wrist_rotation_ratio), angle)            
        )

        spike_hub.wait(
            wrist_angle_motor.rotate(100 * (angle_vs_rotation_ratio / wrist_rotation_ratio), angle * angle_vs_rotation_ratio * 0.5),
            wrist_rotation_motor.rotate(100, angle * wrist_rotation_ratio * 0.5),
            hand_motor.rotate(-100 * (1 / wrist_rotation_ratio), angle* 0.5)
        )        
        
    except KeyboardInterrupt as err:
        print(err)

    spike_hub.wait(*[ task.stop() for task in motors])
    
    spike_hub.close()


main()