import heapq
import logging

from patients.constants import PERCENT_MIN_BEHAVIOR, MAX_AGE_PERCENT, ACCEPTED_OFFERS_WEIGHT_PERCENT, \
    CANCELED_OFFERS_WEIGHT_PERCENT, TOP_PATIENT_RANGE, MAX_REPLY_TIME_WEIGHT_PERCENT, AGE_WEIGHT_PERCENT, \
    EARTH_CIRCUIT, DISTANCE_WEIGHT_PERCENT
from patients.utils import load_patients_list, distance_calculation


class Patients:

    def __init__(self, load_patients_from_file=True):
        self.patients_list = list()
        self.max_accepted_offers = 1
        self.max_canceled_offers = 1
        self.max_reply_time = 1
        self.max_behavior_index = 1

        if load_patients_from_file:
            self.preprocess_patient_list(load_patients_list())
            self.preprocess_patient_priority()

    @staticmethod
    def validate_and_convert_patient_input_data(patient: dict) -> (dict, None):
        """
        Validate a single patient data and convert it into usable data type
        Additional information - depending on the project, this function can be divided into validator and converter
        :param patient: Single patient data
        :type patient: dict
        :return: Patient data or None if there is a data issue
        :rtype: dict | None
        """
        patient_data = {
            'acceptedOffers': 0,
            'canceledOffers': 0,
            'averageReplyTime': 0,
            'name': '',
            'id': '',
            'age': 0,
            'latitude': 0,
            'longitude': 0,
            'priority': None
        }

        try:
            if 'id' not in patient:
                raise Exception(f'ID not found in the patient data: {patient}')
            elif not patient['id']:
                raise Exception(f'The patient ID is empty: {patient}')
            patient_data['id'] = patient['id']

            if 'name' in patient:
                patient_data['name'] = patient['name']

            for int_data in ['acceptedOffers', 'canceledOffers', 'averageReplyTime', 'age']:
                if int_data not in patient:
                    raise Exception(f'{int_data} not found in the patient data: {patient}')
                patient_data[int_data] = int(patient[int_data])

            if 'location' not in patient:
                raise Exception(f'Location not found in the patient data {patient}')

            if 'latitude' not in patient['location']:
                raise Exception(f'Latitude not found in the patient data {patient}')
            elif not patient['location']['latitude']:
                raise Exception(f'Latitude is empty: {patient}')

            if 'longitude' not in patient['location']:
                raise Exception(f'Longitude not found in the patient data {patient}')
            elif not patient['location']['longitude']:
                raise Exception(f'Longitude is empty: {patient}')

            patient_data['latitude'] = float(patient['location']['latitude'])
            patient_data['longitude'] = float(patient['location']['longitude'])
        except Exception as e:
            logging.warning(f'Cannot process the patient. Exception {e}')
            return None

        return patient_data

    def preprocess_patient_priority(self):
        """
        Preprocess the patient priority with existing data
        """
        for patient in self.patients_list:
            if (
                    (patient['acceptedOffers'] + patient['canceledOffers'])
                    / self.max_behavior_index) <= PERCENT_MIN_BEHAVIOR:
                accepted_offers_index = ACCEPTED_OFFERS_WEIGHT_PERCENT
                canceled_offers_index = CANCELED_OFFERS_WEIGHT_PERCENT
                average_reply_time_index = MAX_REPLY_TIME_WEIGHT_PERCENT
                age_index = AGE_WEIGHT_PERCENT
            else:
                accepted_offers_index = \
                    (patient['acceptedOffers'] / self.max_accepted_offers) * ACCEPTED_OFFERS_WEIGHT_PERCENT

                canceled_offers_index = \
                    (1 - (patient['canceledOffers'] / self.max_canceled_offers)) * CANCELED_OFFERS_WEIGHT_PERCENT

                average_reply_time_index = \
                    (1 - (patient['averageReplyTime'] / self.max_reply_time)) * MAX_REPLY_TIME_WEIGHT_PERCENT

                age_index = patient['age'] / MAX_AGE_PERCENT

            patient['priority'] = age_index + accepted_offers_index + canceled_offers_index + average_reply_time_index

    def preprocess_patient_list(self, raw_patients_list: list) -> None:
        """
        Patient list pre-processing and calculate maximum of acceptedOffers, canceledOffers, averageReplyTime
        Also calculate the max_behavior_index used to define patients with little data about their behavior
        :param raw_patients_list: pre-processing list patient list
        :type raw_patients_list: list
        :return:
        :rtype: None
        """
        if len(raw_patients_list) < 1:
            return

        for patient in raw_patients_list:
            # Validate the patient input data.
            # If the data is incomplete or contains incorrect information, the patient will be excluded from the list
            patient_list = Patients.validate_and_convert_patient_input_data(patient)
            if not patient_list:
                continue

            self.patients_list.append(patient_list)

            # Calculate the maximum of acceptedOffers, canceledOffers and averageReplyTime
            if patient_list['acceptedOffers'] > self.max_accepted_offers:
                self.max_accepted_offers = patient_list['acceptedOffers']

            if patient_list['canceledOffers'] > self.max_canceled_offers:
                self.max_canceled_offers = patient_list['canceledOffers']

            if patient_list['averageReplyTime'] > self.max_reply_time:
                self.max_reply_time = patient_list['averageReplyTime']

        # Calculate max_behavior_index - it will be used for define patients with little behavior data
        self.max_behavior_index = self.max_accepted_offers + self.max_canceled_offers

    def get_top_priority_patients(self, latitude: float, longitude: float,
                                  patient_range: int = TOP_PATIENT_RANGE) -> list:
        """
        Get a final list of patients according to the coordinates of the facility
        :param latitude: facility latitude
        :type latitude: float
        :param longitude: facility longitude
        :type longitude: float
        :param patient_range: Number of top results to return
        :type patient_range: int
        :return: List with top patients
        :rtype: list
        """
        ordered_patient_list = list()

        for patient in self.patients_list:
            distance = distance_calculation(patient['latitude'], patient['longitude'], latitude, longitude)
            distance_percent = (1 - (distance / EARTH_CIRCUIT)) * DISTANCE_WEIGHT_PERCENT
            priority = float(patient['priority'] + distance_percent)
            heapq.heappush(ordered_patient_list, (priority, patient))

        return heapq.nlargest(patient_range, ordered_patient_list)
