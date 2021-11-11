from unittest import TestCase

from patient import Patient
from location import Location
from init_patients import init_patient_location_object_from_json, init_patient_object_form_json, init_patients_objects

from .utils import patients


class TestInitPatientLocationObjectFromJson(TestCase):
    def test_init_patient_location_object_from_json_with_valid_data(self):
        location = init_patient_location_object_from_json(patients[0]["location"])
        self.assertIsInstance(location, Location)
        self.assertEqual(location.latitude, float(patients[0]["location"]["latitude"]))
        self.assertEqual(location.longitude, float(patients[0]["location"]["longitude"]))

    def test_init_patient_location_object_from_json_with_null(self):
        location = init_patient_location_object_from_json(None)
        self.assertIsNone(location)


class TestInitPatientObjectFormJson(TestCase):
    def test_init_patient_object_form_json_with_patients(self):
        patient = init_patient_object_form_json(patients[0])
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.id, patients[0]["id"])


class TestInitPatientsObjects(TestCase):
    def test_init_patients_objects(self):
        """
        Test that the init_patients_objects function returns a list of
        Patient objects.
        """

        patients_objects_list = init_patients_objects(patients)
        self.assertIsInstance(patients_objects_list, list)
        self.assertIsInstance(patients_objects_list[0], Patient)
