import json
import logging
import math
import os
from json import JSONDecodeError

from patients.constants import PATIENTS_FILE_PATH, EARTH_RADIUS


def load_patients_list(patient_file_path: str = PATIENTS_FILE_PATH) -> list:
    """
    Load patient list from file
    :return: List with patients
    :rtype: list
    """
    if os.path.exists(patient_file_path):
        with open(patient_file_path) as json_file:
            try:
                data = json.load(json_file)
            except JSONDecodeError:
                logging.error(f"Cannot parse file {PATIENTS_FILE_PATH} due to JSONDecodeError")
                return []
            return data
    logging.error(f"The file {PATIENTS_FILE_PATH} does not exists")
    return []


def distance_calculation(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    The distance calculator using the Haversine formula
    :param lat1: First point latitude
    :type lat1: float
    :param lon1: First point longitude
    :type lon1: float
    :param lat2: Second point latitude
    :type lat2: float
    :param lon2: Second point longitude
    :type lon2: float
    :return: Distance in kilometers
    :rtype: float
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    d_lat = (lat2 - lat1)
    d_lon = (lon2 - lon1)
    a = (pow(math.sin(d_lat / 2), 2) + pow(math.sin(d_lon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS * c
