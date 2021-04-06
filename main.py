import spikectl
import time

spike_hub = spikectl.find_hub('mp8')

spike_hub.display_clear()

count = 10
def handler(n):    
    global count
    count = count - 1
    print(n.percentage)
    return count >= 0

spike_hub.trigger_current_state()
spike_hub.listen_notifications(handler, spikectl.model.BatteryStatusNotification)

spike_hub.close()