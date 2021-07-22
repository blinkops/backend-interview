import unittest

from patients.utils import distance_calculation, load_patients_list


class UtilsTest(unittest.TestCase):

    def test_load_patients_list_existing_file(self):
        patient_list = load_patients_list()
        self.assertEqual(len(patient_list), 1000)

    def test_load_patients_list_not_existing_file(self):
        patient_list = load_patients_list('incorrect/file/path.json')
        self.assertEqual(len(patient_list), 0)

    def test_load_patients_list_wrong_json_data_file(self):
        patient_list = load_patients_list('sample-data/incorrect_patient_json_data_for_test_purpose.json')
        self.assertEqual(len(patient_list), 0)

    def test_distance_calculation(self):
        first_lat = 32.109333
        first_lng = 34.855499
        second_lat = 43.21667
        second_lng = 27.91667
        self.assertEqual(round(distance_calculation(first_lat, first_lng, second_lat, second_lng), 2), 1376.61)
