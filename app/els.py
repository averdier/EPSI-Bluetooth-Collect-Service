# -*- coding: utf-8 -*-

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Text, Integer, Double, InnerObjectWrapper, Nested


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


class Sensor(MyDocType):
    pos_x = Integer()
    pos_y = Integer()
    radius = Integer()
    mqtt_token = Text()
    key = Text()

    class Meta:
        index = 'bluetooth'


class SensorData(InnerObjectWrapper):
    """
    Inner object
    """

    def __eq__(self, other):
        return self.device_id == other.device_id \
               and self.rssi == other.rssi \
               and self.start_timestamp == other.start_timestamp \
               and self.end_timestamp == other.end_timestamp


class DeviceLog(MyDocType):
    """
    Sensor
    """
    start_timestamp = Double()
    end_timestamp = Double()
    mac_address = Text()
    sensors_data = Nested(
        doc_class=SensorData,
        properties={
            'device_id': Text(),
            'rssi': Integer(),
            'start_timestamp': Double(),
            'end_timestamp': Double()
        }
    )

    class Meta:
        index = 'bluetooth'

    def set_sensors_data(self, data):
        """
        Set device sensors values
        :param data:
        :type data: list
        """

        if len(data) > 0:
            min_ts = data[0]['start_timestamp']
            max_ts = data[0]['end_timestamp']

            for i in range(1, len(data)):
                min_ts = min(min_ts, data[i]['start_timestamp'])
                max_ts = min(max_ts, data[i]['end_timestamp'])

                self.sensors_data.append({
                    'device_id': data[i]['device_id'],
                    'rssi': data[i]['rssi'],
                    'start_timestamp': data[i]['start_timestamp'],
                    'end_timestamp': data[i]['end_timestamp']
                })

            self.start_timestamp = min_ts
            self.end_timestamp = max_ts
