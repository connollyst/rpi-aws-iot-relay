import json
import time
from uuid import uuid4

from Logger import get_logger
from aws.AwsIotCore import AwsIotCore
from gpio.Relay import Relay
from rpi.Host import Host


class App:
    LOGGER = get_logger(__name__)

    AWS_ENDPOINT = 'a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com'
    AWS_IOT_MQTT_TOPIC = 'iot/devices/readings'
    AWS_CLIENT_ID = "iot-relay-" + str(uuid4())

    def __init__(self, pin, duration, frequency):
        self._pin = pin
        self._duration = duration
        self._frequency = frequency
        self._host = Host()

    def start(self):
        while True:
            self._run()
            time.sleep(self._frequency)

    def _run(self):
        relay = Relay(pin=self._pin, initial=Relay.State.OFF, host=self._host, logger=self.LOGGER)
        writer = AwsIotCore(self.AWS_ENDPOINT, logger=self.LOGGER)
        writer.connect(self.AWS_CLIENT_ID)
        relay.on()
        writer.write(self.AWS_IOT_MQTT_TOPIC, json.dumps(relay.to_json(), indent=4, default=str))
        time.sleep(self._duration)
        relay.off()
        writer.write(self.AWS_IOT_MQTT_TOPIC, json.dumps(relay.to_json(), indent=4, default=str))
        writer.disconnect()
