# -*- coding: utf-8 -*-

import json
from elasticsearch_dsl.connections import connections
import paho.mqtt.client as mqtt
from config import config
from .models import Device, BluetoothLog
from .utils import group_data_with_match_intervals


class App:
    def __init__(self, config_name='default'):
        self._mqtt = mqtt.Client()
        self._config = config[config_name]
        self._sensors = {}

    def on_sensor_update(self, sensor_id):
        grouped_data = group_data_with_match_intervals(
            self._sensors[sensor_id],
            list(self._sensors.values())
        )

        for mac_address in grouped_data:
            log = BluetoothLog(mac=mac_address)
            log.set_sensors_data(grouped_data[mac_address])
            log.save()

    def on_message(self, userdata, msg):
        print('Got message from: ' + msg.topic)

        parts = msg.topic.split('/')
        if len(parts) == 4 and parts[3] == 'from_device':
            data = json.loads(msg.payload.decode('utf-8'))

            if self._sensors.get(data['id']):
                self._sensors[data['id']]['data'] = {}
                for device in data['devices']:
                    self._sensors[data['id']]['data'][device['mac']] = {
                        'start_timestamp': data['start_timestamp'],
                        'end_timestamp': data['end_timestamp'],
                        'rssi': device['rssi']
                    }

                self.on_sensor_update(data['id'])

    def on_connect(self, userdata, flags, rc):
        if rc == 4:
            raise Exception('Invalid username or password')

        if rc != 0:
            raise Exception('Unable to connect to mqtt service')

        print('MQTT connected')

        self._mqtt.subscribe('bluetooth/sensor/+/from_device')

    def start(self):
        connections.create_connection(hosts=[self._config.ELASTICSEARCH_HOST], timeout=20)
        BluetoothLog.init()

        sensors_search = Device.search().query('term', device_type='sensor').execute()
        self._sensors = {sensor.meta.id: {'sensor': sensor, 'data': {}} for sensor in sensors_search}

        def on_mqtt_message(client, userdata, msg):
            nonlocal self
            self.on_message(userdata, msg)

        def on_mqtt_connect(client, userdata, flags, rc):
            nonlocal self
            self.on_connect(userdata, flags, rc)

        self._mqtt.username_pw_set(self._config.MQTT_USERNAME, self._config.MQTT_TOKEN)
        self._mqtt.on_message = on_mqtt_message
        self._mqtt.on_connect = on_mqtt_connect
        self._mqtt.connect(self._config.MQTT_SERVER, self._config.MQTT_PORT, self._config.MQTT_KEEP_ALIVE)

    def stop(self):
        self._mqtt.disconnect()

    def loop(self):
        self._mqtt.loop()
