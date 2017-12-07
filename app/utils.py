# -*- coding: utf-8 -*-


def mac_in_sensor_data_list(mac_address, data_list):
    found = False
    for data in data_list:
        if data['mac'] == mac_address:
            found = True
            break

    return found


def find_in_sensor_data_list_from_mac_address(mac_address, data_list):
    target = None

    for data in data_list:
        if data['mac'] == mac_address:
            target = data
            break

    return target


def find_match_in_sensors(sensor_data_list, sensor_dict, threshold=5):
    mac_addresses = {}

    for sensor_name in sensor_dict:
        for data in sensor_dict[sensor_name]:

            target_data = find_in_sensor_data_list_from_mac_address(data['mac'], sensor_data_list)

            if target_data is not None:
                if (data['start_timestamp'] - threshold <= target_data['end_timestamp']) \
                        or (data['end_timestamp'] + threshold >= target_data['start_timestamp']):

                    if data['mac'] not in mac_addresses:
                        mac_addresses[data['mac']] = [data]

                    elif data not in mac_addresses[data['mac']]:
                        mac_addresses[data['mac']].append(data)


def get_mac_with_sensors(sensors):
    """
    Get mac address with sensors data

    :param sensors: List of sensors

    :return: Dict of mac address with sensors data
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
            if (data['start_timestamp'] - threshold <= target['end_timestamp']) or (
                            data['end_timestamp'] + threshold >= target['start_timestamp']):
                group.append(data)

    return group
