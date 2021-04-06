import spikectl
import time

spike_hub = spikectl.find_hub('mp8')

spike_hub.display_clear()

for color in range(5):
    res = spike_hub.set_button_color(color)
    print(f'color {color}: {res}')    

spike_hub.close()