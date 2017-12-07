# -*- coding: utf-8 -*-

import json
import paho.mqtt.client as mqtt_client
from .els import Sensor


class CollectApp:
    def __init__(self, config):
        self._client = None
        self._config = config
        self._sensors = {}
        pass

    def on_message(self, userdata, msg):
        """
        On mqtt message

        :param userdata:
        :param msg:
        :return:
        """
        topic_parts = msg.topic.split('/')

        if len(topic_parts) == 3 and self._sensors.get(topic_parts[1], None) is not None and topic_parts[
            2] == 'from_device':
            self._sensors[topic_parts[1]] = []
            try:
                data = msg.payload.decode('utf-8')

            except Exception:
                data = {'devices': []}

            for device in data['devices']:
                self._sensors[topic_parts[1]].append({
                    data['start_timestamp'],
                    data['end_timestamp'],
                    device['mac'],
                    device['rssi']
                })

            self.on_sensor_update(topic_parts[1])

    def on_connect(self, userdata, flags, rc):
        """
        On connect to mqtt

        :param userdata:
        :param flags:
        :param rc:
        """
        pass

    def on_sensor_update(self, sensor_id):
        pass

    def start(self):
        """
        Start app
        """

        sensors_search = Sensor.search().execute()

        self._sensors = {sensor.meta.id: [] for sensor in sensors_search}

        def on_mqtt_message(client, userdata, msg):
            nonlocal self
            self.on_message(userdata, msg)

        def on_mqtt_connect(client, userdata, flags, rc):
            nonlocal self
            self.on_connect(userdata, flags, rc)

        self._client = mqtt_client.Client()
        self._client.username_pw_set(self._config.MQTT_USERNAME, self._config.MQTT_TOKEN)

        self._client.on_connect = on_mqtt_connect
        self._client.on_message = on_mqtt_message

        self._client.connect(self._config.MQTT_SERVER, self._config.MQTT_PORT, self._config.MQTT_KEEP_ALIVE)

    def stop(self):
        """
        Stop app
        """
        self._client.disconnect()
