import unittest
from utils import calculate_patients_score, calculate_patients_score_without_distance, calculate_patient_score_without_distance
from constants import *
from app import app
from random import randint

class TestScoreCalc(unittest.TestCase):
    patient_structure = {
        'id': 'mock123mock',
        'name': 'Joe Doe',
        'location': {
            'latitude': '77.5235',
            'longitude': '175.3549'
        },
        'acceptedOffers': '50',
        'canceledOffers': '50',
        'averageReplyTime': '150',
        'age': '80'
    }

    test_client = app.test_client()

    # Test util functions

    def test_patient_max_score(self):
        patient = self.patient_structure.copy()
        patient.update({'acceptedOffers' : MAX_ACCEPTED_OFFERS})
        patient.update({'canceledOffers' : 0})
        patient.update({'averageReplyTime' : 0})
        patient.update({'age' : MAX_AGE})
        score = calculate_patient_score_without_distance(patient)
        self.assertEqual(score, TOTAL_WEIGHT - DISTANCE_WEIGHT)

    def test_patient_min_score(self):
        patient = self.patient_structure.copy()
        patient.update({'acceptedOffers' : 0})
        patient.update({'canceledOffers' : MAX_CANCELLED_OFFERS})
        patient.update({'averageReplyTime' : MAX_REPLY_TIME})
        patient.update({'age' : 0})
        score = calculate_patient_score_without_distance(patient)
        self.assertEqual(score, 0)

    def test_patient_missing_behavior(self):
        patient = self.patient_structure.copy()
        del patient['acceptedOffers']
        del patient['canceledOffers']
        del patient['averageReplyTime']
        patient.update({'age' : MAX_AGE})
        score = calculate_patient_score_without_distance(patient)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score,TOTAL_WEIGHT - AGE_WEIGHT - DISTANCE_WEIGHT)

    def test_patient_no_data(self):
        patient = {}
        score = calculate_patient_score_without_distance(patient)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score,TOTAL_WEIGHT)

    def test_patient_erroneous_data(self):
        patient = {
        'location': {
            'latitude': 'fds',
            'longitude': 150
        },
        'acceptedOffers': 'asd',
        'canceledOffers': -159,
        'age': 'Eighty'
        }
        score = calculate_patient_score_without_distance(patient)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, TOTAL_WEIGHT - DISTANCE_WEIGHT)

    def test_patients(self):
        patients = []
        for i in range(10):
            patients.append(newPatient())
        calculate_patients_score_without_distance(patients)
        calculate_patients_score(patients, 77.5235,175.3549)
        for patient in patients:
            self.assertIn('totalScore',patient)
            self.assertGreaterEqual(patient['totalScore'],0)
            self.assertLessEqual(patient['totalScore'],TOTAL_WEIGHT)

    # Test API endpoints

    def test_get_patients_bad_location(self):
        code_bad_format = self.test_client.get(f'{DEFAULT_LOCAL_URL}/patients?location=10asd,49').status_code
        code_no_comma = self.test_client.get(f'{DEFAULT_LOCAL_URL}/patients?location=772334').status_code
        code_blank_location = self.test_client.get(f'{DEFAULT_LOCAL_URL}/patients?location=').status_code
        code_blank_query = self.test_client.get(f'{DEFAULT_LOCAL_URL}/patients?').status_code
        code_no_query = self.test_client.get(f'{DEFAULT_LOCAL_URL}/patients').status_code
        self.assertEqual(code_no_comma, 400)
        self.assertEqual(code_bad_format, 400)
        self.assertEqual(code_blank_location, 400)
        self.assertEqual(code_blank_query, 400)
        self.assertEqual(code_no_query, 400)


    def test_get_patients_good_location(self):
        code_correct = self.test_client.get(f'{DEFAULT_LOCAL_URL}/patients?location=77.5235,175.3549').status_code
        self.assertEqual(code_correct, 200)

    def test_get_homepage(self):
        res_code = self.test_client.get(f'{DEFAULT_LOCAL_URL}/').status_code
        self.assertEqual(res_code, 200)

def newPatient():
    return {
        'id': 'mock123mock',
        'name': 'Joe Doe',
        'location': {
            'latitude': randint(-90,90),
            'longitude': randint(-180,180)
        },
        'acceptedOffers': randint(0,100),
        'canceledOffers': randint(0,100),
        'averageReplyTime': randint(0,3600),
        'age': randint(0,150)
    }
