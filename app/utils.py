# -*- coding: utf-8 -*-


def group_data_with_match_intervals(updated_sensor, sensors, threshold=5):
    result = {}

    for mac_address in updated_sensor['data']:
        result[mac_address] = [{
            'device_id': updated_sensor['sensor'].meta.id,
            'start_timestamp': updated_sensor['data'][mac_address]['start_timestamp'],
            'end_timestamp': updated_sensor['data'][mac_address]['end_timestamp'],
            'rssi': updated_sensor['data'][mac_address]['rssi']
        }]
        for sensor in sensors:
            if sensor != updated_sensor:
                if mac_address in sensor['data']:
                    if (sensor['data'][mac_address]['end_timestamp'] + threshold >= updated_sensor['data'][mac_address]['start_timestamp']) or (sensor['data'][mac_address]['start_timestamp'] - threshold <= updated_sensor['data'][mac_address]['end_timestamp']):
                        result[mac_address].append({
                            'device_id': sensor['sensor'].meta.id,
                            'start_timestamp': sensor['data'][mac_address]['start_timestamp'],
                            'end_timestamp': sensor['data'][mac_address]['end_timestamp'],
                            'rssi': sensor['data'][mac_address]['rssi']
                        })

    return result

