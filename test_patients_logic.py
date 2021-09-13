import unittest
import patients_logic
import requests
import json

BASE = 'http://127.0.0.1:5000/'

class TestHelperFunctions(unittest.TestCase):
    def test_distance(self):
        loc1 = patients_logic.Location(-63.52345, -27.27481)
        loc2 = patients_logic.Location(85.32072, 85.53304)

        self.assertEqual(loc1.distance(loc2), 17233.24)
        self.assertEqual(loc1.distance(loc1), 0)

    def test_scale(self):
        # Test whether the function raises a ValueError when the value provided is outside of the old range.
        with self.assertRaises(ValueError):
            patients_logic.scale((0, 10), (20, 30), 20)

        self.assertEqual(patients_logic.scale((0, 10), (1, 10), 3), 3.7)
        self.assertEqual(patients_logic.scale((1, 10), (1, 500), 1), 1.0)
        self.assertEqual(patients_logic.scale((5, 10), (5, 15), 10, True), 5)

    def test_api_call(self):
        self.assertEqual(requests.get(BASE + 'patients?location=-45.789,98.234').status_code, 200)
        self.assertEqual(requests.get(BASE + 'patients?location=abc').status_code, 404)
        self.assertEqual(requests.get(BASE + 'patients?location=-98.546, 120.678').status_code, 404)


class TestPatientsLogic(unittest.TestCase):
    def setUp(self):
        self.facility_location = patients_logic.Location(-63.52345, -27.27481)
        location1 = patients_logic.Location(46.7110, -63.1150)
        location2 = patients_logic.Location(-81.0341, 144.9963)
        location3 = patients_logic.Location(-35.5336, -25.2795)

        self.patient1 = patients_logic.Patient("541d25c9-9500-4265-8967-240f44ecf723", "Samir Pacocha", 46, location1, self.facility_location.distance(location1), 49, 92, 2598)
        self.patient2 = patients_logic.Patient("41fd45bc-b166-444a-a69e-9d527b4aee48", "Bernard Mosciski", 21, location2, self.facility_location.distance(location2), None, 96, 1908)
        self.patient3 = patients_logic.Patient("90592106-a0d9-4329-8159-af7ce4ba45ad", "Theo Effertz", 67, location3, self.facility_location.distance(location3), 0, 0, 2000)

        self.all_patients_list = [self.patient1, self.patient2, self.patient3]
        self.only_valid_score_patients = [self.patient1, self.patient3]

    def test_all_attributes_valid(self):   
        self.assertEqual(self.patient1.all_attributes_valid(), True)
        self.assertEqual(self.patient2.all_attributes_valid(), False)
        self.assertEqual(self.patient3.all_attributes_valid(), True)

    def test_is_sortable(self):
        self.assertEqual(patients_logic.is_sortable(1), True)
        self.assertEqual(patients_logic.is_sortable(True), True)
        self.assertEqual(patients_logic.is_sortable(self.patient1), False)

    def test_get_min_max(self):
        # Test whether function raises ValueError for a generator of non-sortable objects.
        with self.assertRaises(TypeError):
            patients_logic.get_min_max(patient for patient in self.all_patients_list)

        # Test whether function raises StopIteration for an empty generator.
        with self.assertRaises(StopIteration):
            patients_logic.get_min_max(num for num in [])

        self.assertEqual(patients_logic.get_min_max((num for num in [1, 2, 3])), (1, 3))
        self.assertEqual(patients_logic.get_min_max((num for num in [1, -1, 0])), (-1, 1))
        self.assertEqual(patients_logic.get_min_max((num for num in [0])), (0, 0))

    def test_comparison_values(self):        
        comparison_values = {'age': (46, 67), 'distance': (3115.16, 12654.77), 'accepted_offers': (0, 49), 'cancelled_offers': (0, 92), 'average_reply_time': (2000, 2598)}
        
        # The second patient is not included in the list of patients, since he has little behavior data.
        result = patients_logic.get_comparison_values(self.only_valid_score_patients)

        self.assertEqual(result, comparison_values)

    def test_calculate_score(self):
        comparison_values = patients_logic.get_comparison_values(self.only_valid_score_patients)
        
        self.assertEqual(self.patient1.calculate_score(comparison_values), 3.7)
        self.assertEqual(self.patient2.calculate_score(comparison_values), None)
        self.assertEqual(self.patient3.calculate_score(comparison_values), 7.3)
    
    def test_check_behavior_data(self):
        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_behavior_data(-3, 'test')

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_behavior_data('abc', 'test')
        
        # Test whether the function fails when given a None value.
        try:
            patients_logic.check_behavior_data(None, 'test')
        except patients_logic.InvalidAttributeError:
            self.fail('InvalidAttributeError raised for None value.')

    def test_check_values(self):
        invalid_id = {"id":"541d25c9","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":2598}
        invalid_name = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"012 345","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":2598}
        invalid_latitude = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"abc","longitude":"-63.1150"},"age":46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":2598}
        invalid_longitude = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-190.1150"},"age":46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":2598}
        invalid_age = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":-46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":2598}
        invalid_accepted_offers = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":46,"acceptedOffers":-49,"canceledOffers":92,"averageReplyTime":2598}
        invalid_cancelled_offers = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":46,"acceptedOffers":49,"canceledOffers":'test',"averageReplyTime":2598}
        invalid_average_reply_time = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":-1}
    
        
        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_id)

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_name)

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_latitude)

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_longitude)

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_age)

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_accepted_offers)

        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_cancelled_offers)
        
        with self.assertRaises(patients_logic.InvalidAttributeError):
            patients_logic.check_values(invalid_average_reply_time)

    def test_patient_decoder(self):
        patient_json1 = {"id":"541d25c9-9500-4265-8967-240f44ecf723","name":"Samir Pacocha","location":{"latitude":"46.7110","longitude":"-63.1150"},"age":46,"acceptedOffers":49,"canceledOffers":92,"averageReplyTime":2598}
        patient_json2 = {"id":"41fd45bc-b166-444a-a69e-9d527b4aee48","name":"Bernard Mosciski","location":{"latitude":"-81.0341","longitude":"144.9963"},"age":21,"acceptedOffers":None,"canceledOffers":96,"averageReplyTime":1908}
        patient_json3 = {"id":"90592106-a0d9-4329-8159-af7ce4ba45ad","name":"Theo Effertz","location":{"latitude":"-35.5336","longitude":"-25.2795"},"age":67,"acceptedOffers":0,"canceledOffers":0,"averageReplyTime":2000}
        
        self.assertEqual(patients_logic.patient_decoder(patient_json1), self.patient1)
        self.assertEqual(patients_logic.patient_decoder(patient_json2), self.patient2)
        self.assertEqual(patients_logic.patient_decoder(patient_json3), self.patient3)        

    def test_parse_patients_data(self):
        self.assertEqual(patients_logic.parse_patients_data('sample-data\patients_short.json'), self.all_patients_list)

    def test_serialize_patients_list(self):
        patients_json = ''

        with open('sample-data\patients_short.json', 'r') as file:
            patients_json = file.read()

        self.assertEqual(patients_logic.serialize_patients_list(self.all_patients_list).replace(': ', ':').replace(', ', ','), patients_json)

    def test_insert_no_score_patients(self):
        # Since the no score patients are randomly added to the list, there's no way to know exactly what the output will look like.
        self.assertIn(self.patient2, patients_logic.insert_no_score_patients(self.only_valid_score_patients, [self.patient2]))
    
    def top_list_test_case(self, file_path, expected_len=10):
        '''
        Tests the get_top_list function with the given file path.

        Parameters
        ----------
        file_path : str
            A string containing the file path of a file containing json serialized patient data.
        
        expected_len : int, default 10
            The expected length of the top list.

        Returns
        -------
        int
            The number of no score patients in the top list.
        '''

        count = 0
        no_score_patient_names = ['Bernard Mosciski', 'Demond Rosenbaum', 'Erika Cassin', 'Eve Renner', 'Emmy Douglas', 'Ford Farrell', 'Cecile Hilll']

        # Get the top list of patients.
        top_list = patients_logic.get_top_list(self.facility_location, file_path)

        # Deserialize the top list of patients.
        top_list = json.loads(top_list, object_hook=patients_logic.patient_decoder)

        # Test if the list is of the expected length (10 or less if there are less than 10 patients in the data file).
        self.assertEqual(len(top_list), expected_len)
        
        # Count how many no score patients have been added to the top list.
        for patient in top_list:
            if patient.get_name() in no_score_patient_names:
                count += 1

        return count


    def test_get_top_list(self):
        # Test if exception is raised for invalid data file.
        with self.assertRaises(patients_logic.InvalidFileError):
            patients_logic.get_top_list(self.facility_location, 'sample-data\invalid_file1.json')
        
        with self.assertRaises(patients_logic.InvalidFileError):
            patients_logic.get_top_list(self.facility_location, 'sample-data\invalid_file2.json')

        # Test whether an empty list is returned for a data file containing an empty list.
        self.assertEqual(patients_logic.get_top_list(self.facility_location, 'sample-data\empty.json'), '[]')

        # Test whether 1-5 of the no score patients have been added to the top list.
        count = self.top_list_test_case('sample-data\patients_long_with_null_values.json')
        self.assertEqual(count >= 1 and count <= 5, True)

        # Test whether more than 5 no score patients are added to the top list when there are less than 5 patients with a valid score.
        count = self.top_list_test_case('sample-data\patients_less_than_5_valid_score.json')
        self.assertEqual(count, 7)

        # Test whether all no score patients are added to the top list when there are only no score patients, and less than 10 of them.
        count = self.top_list_test_case('sample-data\patients_all_null_values.json', 7)
        self.assertEqual(count, 7)


if __name__ == '__main__':
    unittest.main()