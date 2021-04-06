# spikedev

Tools and libraries for LEGO® SPIKE® developers.

## About

This is a personal project in which I'm exploring ways to interact with LEGO® SPIKE® Hub directly, without the SPIKE® App.

Methods and messages here were discovered by sniffing the communication between my desktop and the SPIKE® Hub.

Feel free to submit a PR and joing the project!

## Usage

```python
import spikectl

# Find Spike hub by name
hub = spikectl.find_hub('my-hub')

# change center button color
red = 10
hub.set_button_color(red)

# rotate motor
motor_port = 'A'
power_percentage = 100
degrees = 360
hub.motor_run_for_degrees(motor_port, power_percentage, degress)

# listen sensor data
count = 10
def notification_listener(notification):
    global count
    count = count - 1
    print(notification)
    return count >= 0

hub.listen_notifications(notification_listener)

# Finish communication
hub.close()

```