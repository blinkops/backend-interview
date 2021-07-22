import copy
import unittest

from patients.patients import Patients


class TestPatients(unittest.TestCase):
    raw_patient_structure = {
        'id': 'test_id',
        'name': 'Test Name',
        'acceptedOffers': '123',
        'canceledOffers': '123',
        'averageReplyTime': '123',
        'age': '55',
        'location': {
            'latitude': '32.109333',
            'longitude': '34.855499'
        }
    }

    patient_structure_processed = {
        'id': 'test_id',
        'name': 'Test Name',
        'acceptedOffers': 123,
        'canceledOffers': 123,
        'averageReplyTime': 123,
        'age': 55,
        'latitude': 32.109333,
        'longitude': 34.855499,
        'priority': None
    }

    def test_validate_patient_input_data_proper_validation(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertDictEqual(validation_data, self.patient_structure_processed)

    def test_validate_patient_input_data_missing_id(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        del raw_patient_structure['id']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_id(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        raw_patient_structure['id'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_accepted_offers(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        del raw_patient_structure['acceptedOffers']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_accepted_offers(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        raw_patient_structure['acceptedOffers'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_canceled_offers(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        del raw_patient_structure['canceledOffers']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_canceled_offers(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        raw_patient_structure['canceledOffers'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_average_reply_time(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        del raw_patient_structure['averageReplyTime']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_average_reply_time(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        raw_patient_structure['averageReplyTime'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_age(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        del raw_patient_structure['age']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_age(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        raw_patient_structure['age'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_location(self):
        patients = Patients()
        raw_patient_structure = self.raw_patient_structure.copy()
        del raw_patient_structure['location']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_latitude(self):
        patients = Patients()
        raw_patient_structure = copy.deepcopy(self.raw_patient_structure)
        del raw_patient_structure['location']['latitude']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_latitude(self):
        patients = Patients()
        raw_patient_structure = copy.deepcopy(self.raw_patient_structure)
        raw_patient_structure['location']['latitude'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_missing_longitude(self):
        patients = Patients()
        raw_patient_structure = copy.deepcopy(self.raw_patient_structure)
        del raw_patient_structure['location']['longitude']
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_validate_patient_input_data_empty_longitude(self):
        patients = Patients()
        raw_patient_structure = copy.deepcopy(self.raw_patient_structure)
        raw_patient_structure['location']['longitude'] = ''
        validation_data = patients.validate_and_convert_patient_input_data(raw_patient_structure)

        self.assertEqual(validation_data, None)

    def test_preprocess_patient_list_max_values(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)
        patient_1['acceptedOffers'] = '500'
        patient_2['canceledOffers'] = '1000'
        patient_1['averageReplyTime'] = '3000'
        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])

        self.assertEqual(patients.max_accepted_offers, 500)
        self.assertEqual(patients.max_canceled_offers, 1000)
        self.assertEqual(patients.max_reply_time, 3000)
        self.assertEqual(patients.max_behavior_index, 1500)

    def test_preprocess_patient_list_priority(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)
        patient_1['age'] = '30'
        patient_2['age'] = '60'
        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])
        patients.preprocess_patient_priority()

        self.assertEqual(patients.patients_list[0]['priority'], 32)
        self.assertEqual(patients.patients_list[1]['priority'], 34)

    def test_get_top_priority_patients_different_age(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)

        patient_1['id'] = 'p1'
        patient_1['age'] = '30'

        patient_2['id'] = 'p2'
        patient_2['age'] = '60'

        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])
        patients.preprocess_patient_priority()
        top_patients_list = patients.get_top_priority_patients(32.109333, 34.855499)

        self.assertEqual(top_patients_list[0][1]['id'], 'p2')
        self.assertEqual(top_patients_list[1][1]['id'], 'p1')

    def test_get_top_priority_patients_different_accepted_offers(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)

        patient_1['id'] = 'p1'
        patient_1['acceptedOffers'] = '500'

        patient_2['id'] = 'p2'
        patient_2['acceptedOffers'] = '501'

        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])
        patients.preprocess_patient_priority()
        top_patients_list = patients.get_top_priority_patients(32.109333, 34.855499)

        self.assertEqual(top_patients_list[0][1]['id'], 'p2')
        self.assertEqual(top_patients_list[1][1]['id'], 'p1')

    def test_get_top_priority_patients_different_canceled_offers(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)

        patient_1['id'] = 'p1'
        patient_1['canceledOffers'] = '500'

        patient_2['id'] = 'p2'
        patient_2['canceledOffers'] = '501'

        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])
        patients.preprocess_patient_priority()
        top_patients_list = patients.get_top_priority_patients(32.109333, 34.855499)

        self.assertEqual(top_patients_list[0][1]['id'], 'p1')
        self.assertEqual(top_patients_list[1][1]['id'], 'p2')

    def test_get_top_priority_patients_little_behavior_data(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)

        patient_1['id'] = 'p1'
        patient_1['acceptedOffers'] = '10'
        patient_1['canceledOffers'] = '10'

        patient_2['id'] = 'p2'
        patient_2['acceptedOffers'] = '1000'

        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])
        patients.preprocess_patient_priority()
        top_patients_list = patients.get_top_priority_patients(32.109333, 34.855499)

        self.assertEqual(top_patients_list[0][1]['id'], 'p1')
        self.assertEqual(top_patients_list[1][1]['id'], 'p2')

    def test_get_top_priority_patients_different_locations(self):
        patient_1 = copy.deepcopy(self.raw_patient_structure)
        patient_2 = copy.deepcopy(self.raw_patient_structure)

        patient_1['id'] = 'p1'
        patient_1['location']['latitude'] = '32.078651'
        patient_1['location']['longitude'] = '34.778852'

        patient_2['id'] = 'p2'
        patient_2['location']['latitude'] = '32.323354'
        patient_2['location']['longitude'] = '34.856745'

        patients = Patients(False)
        patients.preprocess_patient_list([patient_1, patient_2])
        patients.preprocess_patient_priority()
        top_patients_list = patients.get_top_priority_patients(32.109333, 34.855499)

        self.assertEqual(top_patients_list[0][1]['id'], 'p1')
        self.assertEqual(top_patients_list[1][1]['id'], 'p2')
