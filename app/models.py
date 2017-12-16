# -*- coding: utf-8 -*-

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, InnerObjectWrapper, Keyword, Object, Float, Nested


class MyDocType(DocType):
    created_at = Date()

    def to_dict(self, include_id=False, include_meta=False):
        base = super().to_dict(include_meta)

        if include_id and not include_meta:
            base['id'] = self.meta.id

        return base

    def save(self, **kwargs):
        self.created_at = datetime.utcnow()
        return super().save(**kwargs)


class MQTTAccount(InnerObjectWrapper):
    """
    MQTT Account wrapper
    """


class Device(MyDocType):
    device_type = Keyword()
    pos_x = Integer()
    pos_y = Integer()
    radius = Integer()
    key = Keyword()
    mqtt_account = Object(
        doc_class=MQTTAccount,
        properties={
            'username': Keyword(),
            'password': Keyword(),
            'server': Keyword(),
            'port': Integer(),
            'keep_alive': Keyword(),
            'clients_topic': Keyword(),
            'response_topic': Keyword()
        }
    )

    class Meta:
        index = 'bluetooth'


class SensorData(InnerObjectWrapper):
    """
    Inner object
    """


class BluetoothLog(MyDocType):
    start_timestamp = Float()
    end_timestamp = Float()
    mac = Keyword()
    sensors_data = Nested(
        doc_class=SensorData,
        properties={
            'device_id': Keyword(),
            'rssi': Integer(),
            'start_timestamp': Float(),
            'end_timestamp': Float()
        }
    )

    class Meta:
        index = 'bluetooth'

    def set_sensors_data(self, args):
        if len(args) > 0:
            min_ts = args[0]['start_timestamp']
            max_ts = args[0]['end_timestamp']

            for i in range(1, len(args)):
                min_ts = min(min_ts, args[i]['start_timestamp'])
                max_ts = min(max_ts, args[i]['end_timestamp'])

                self.sensors_data.append({
                    'device_id': args[i]['device_id'],
                    'rssi': args[i]['rssi'],
                    'start_timestamp': args[i]['start_timestamp'],
                    'end_timestamp': args[i]['end_timestamp']
                })

            self.start_timestamp = min_ts
            self.end_timestamp = max_ts
