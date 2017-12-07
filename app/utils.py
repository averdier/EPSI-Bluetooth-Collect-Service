# -*- coding: utf-8 -*-


def get_devices_with_sensors(sensors):
    """
    Get devices with sensors data

    :param sensors: List of sensors

    :return: Dict of devices with sensors data
    {
        mac: [SensorData]
    }
    """
    devices = {}

    for sensor_name in sensors:
        for data in sensors[sensor_name]:

            if data['mac'] not in devices:
                devices[data['mac']] = [data]

            elif data not in devices[data['mac']]:
                devices[data['mac']].append(data)

    return devices


def get_match_intervals(target, sensors_data, threshold=5):
    """
    Return data where interval match with target

    :param target:
    :param sensors_data:
    :param threshold:

    :return: List of sensors data
    :rtype: list
    """
    group = [target]

    for data in sensors_data:
        if data != target:
            if (data['start_timestamp'] - threshold <= target['end_timestamp']) or (data['end_timestamp'] + threshold >= target['start_timestamp']):
                group.append(data)

    return group
