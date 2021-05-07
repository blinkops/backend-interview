import random
from typing import Iterable

import geopy.distance

AGE_SCORE = 0.1
DISTANCE_SCORE = -0.1
ACCEPTED_OFFERS_SCORE = 0.3
CANCELED_OFFERS_SCORE = -0.3
AVERAGE_REPLY_TIME_SCORE = -0.2


class Location(object):
    """
    Provide location structure object for latitude and longitude
    """

    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def is_valid(self):
        """
        Check valid latitude and longitude in Location class object
        :return:
        """
        if 90 >= self.latitude >= -90 and 180 >= self.longitude >= -180:
            return True
        return False

    def to_tuple(self):
        """
        Return the location in tuple format (for distance measurement)
        :return:
        """
        return self.latitude, self.longitude


def create_location(data: dict):
    """
    Returns Location by given dictionary input {'latitude': '', 'longitude': ''}
    :param data:
    :return:
    """
    return Location(latitude=data.get('latitude'), longitude=data.get('longitude'))


class Patient(object):
    """
    Provide patient structure object that hold the patient historical data
    """

    def __init__(self, patient_id: str, name: str, location: dict, age: int, accepted_offers: int, canceled_offers: int,
                 average_reply_time: int):
        self.patient_id = patient_id
        self.name = name
        self.location = create_location(data=location)
        self.age = age
        self.accepted_offers = accepted_offers
        self.canceled_offers = canceled_offers
        self.average_reply_time = average_reply_time
        self.distance = 0
        self.score = 0

    def __repr__(self):
        return f'{self.patient_id}'

    def get_distance(self, location: Location):
        """
        Return the distance of the patient location from the given doctor facility's location
        :param location: facility's location
        :return:
        """
        self.distance = geopy.distance.distance(self.location.to_tuple(), location.to_tuple()).km
        return self.distance

    def get_score(self, location: Location):
        """
        Returns the patient score considering the demographic data and historical behavior

        :param location: facility's location
        :return:
        """
        age = self.age * AGE_SCORE
        distance = self.get_distance(location=location) * DISTANCE_SCORE
        accepted_offers = self.accepted_offers * ACCEPTED_OFFERS_SCORE
        canceled_offers = self.canceled_offers * CANCELED_OFFERS_SCORE
        average_reply_time = self.average_reply_time * AVERAGE_REPLY_TIME_SCORE
        self.score = age + distance + accepted_offers + canceled_offers + average_reply_time
        return self.score


def create_patient(data: dict):
    return Patient(
        patient_id=data.get('id'),
        name=data.get('name'),
        location=data.get('location'),
        age=data.get('age'),
        accepted_offers=data.get('acceptedOffers'),
        canceled_offers=data.get('canceledOffers'),
        average_reply_time=data.get('averageReplyTime')
    )


def get_patients_score_by_location(patients: Iterable[Patient],
                                   location: Location,
                                   limit: int = 10,
                                   add_new_patients: bool = True):
    """
    Return the top list of patients by patient score

    :param patients: list of patients
    :param location: facility's location
    :param limit: size of top list
    :param add_new_patients: True if to give new patients a chance to be selected
    :return:
    """
    if not patients or not location:
        print('Providing patients and location is mandatory')
        return

    result = set()
    new_patients = set()
    for patient in patients:
        score = patient.get_score(location=location)
        if len(result) < limit:
            result.add(patient)
        else:
            # Find the patient with minimum score is list
            result = sorted(result, key=lambda x: x.score, reverse=False)
            min_score = result[0].score
            if score > min_score:
                # Replace patient
                result[0] = patient

        if patient.accepted_offers == 0 and patient.canceled_offers == 0:
            # New patient (patients who have little behavior data)
            new_patients.add(patient)

    # Sort the list by score
    result = sorted(result, key=lambda x: x.score, reverse=True)

    # give new patients a chance to be selected
    if add_new_patients:
        # Randomize new patients list
        random.shuffle(list(new_patients))
        for new_patient in new_patients:
            if new_patient not in result:
                result.insert(0, new_patient)
                result.pop(limit)
                break

    return result
