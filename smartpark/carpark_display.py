from windowed_display import WindowedDisplay
import threading
import time
import paho.mqtt.client as paho
from config_parser import parse_config
class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # Determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.window = WindowedDisplay(
            'Moondalup', CarParkDisplay.fields)
        print("Initialised.") # Used to test if its working
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()


    def on_message(self, client, userdata, message):
        # Function invoked when a new MQTT message has been received
        data = message.payload.decode()
        split_data = data.split(',')
        for item in split_data:
            key, value = item.split(": ")
            if key.strip() == 'SPACES':
                self.spaces = int(value)
            if key.strip() == 'TIME':
                self.time = value
            if key.strip() == 'TEMPC':
                self.temp = float(value)
        # Updates the fields in the UI
        field_values = {
            'Available bays': self.spaces,
            'Temperature': f'{self.temp}℃',
            'At': self.time
        }
        self.window.update(field_values)

    def check_updates(self):
        # Placeholder until update has been received
        self.spaces = ""
        self.temp = ""
        self.time = ""

        while True:
            field_values = {
                'Available bays': self.spaces,
                'Temperature': f'{self.temp}℃',
                'At': self.time
            }
            # Creating an MQTT client and subscribing to display1
            config = parse_config("config2.json")
            self.client = paho.Client(config['name'])
            self.client.connect(config["broker"], config["port"])
            self.client.on_message = self.on_message
            self.client.loop_start()
            self.client.subscribe('display1')
            # Update every 5 seconds
            time.sleep(5)
            self.client.loop_stop()


if __name__ == '__main__':
    CarParkDisplay()