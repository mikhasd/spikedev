import spikectl
import spikectl.model
import time

spike_hub = spikectl.find_hub('mp8')

spike_hub.display.clear()

#battery_status = spike_hub.listen_notification(spikectl.model.BatteryStatusNotification)
#print(battery_status.percentage)

#spike_hub.display.display_text('')

#spike_hub.motor('F').run_timed(600, 100)
#spike_hub.motor('F').run_timed(600, -100)

#spike_hub.motor('F').go_to(65, 0, 'shortest')

spike_hub.motor('F').rotate(100, 30, True, 1)



spike_hub.close()