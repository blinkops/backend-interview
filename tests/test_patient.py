from unittest import TestCase

from patient import Patient
from location import Location


class TestPatient(TestCase):
    def setUp(self):
        self.lyon = Location(45.7597, 4.8422)
        self.paris = Location(48.8567, 2.3508)
        self.distance = 392.2172595594006
        self.patient = Patient("1", "fake", self.lyon, 10, None, None, None, 5)

    def test_get_distance_with_patient_location_as_none(self):
        self.patient.location = None
        self.assertEqual(self.patient.get_distance(self.paris), float('inf'))

    def test_get_distance(self):
        self.assertAlmostEqual(self.distance, self.patient.get_distance(self.paris))

    def test_get_by_field_with_None(self):
        self.assertEqual(self.patient.get_by_field("acceptedOffers", 100), 100)

    def test_get_by_field_with_age(self):
        self.assertEqual(self.patient.get_by_field("age", 100), 10)

    def test_get_by_field_with_location(self):
        self.assertAlmostEqual(self.patient.get_by_field("location", self.paris), self.distance)

    def test_get_by_field_with_location_with_patient_location_as_none(self):
        self.patient.location = None
        self.assertEqual(self.patient.get_by_field("location", self.paris), float("inf"))

    def test_calculate_score(self):
        self.patient.set_score(2)
        self.assertEqual(self.patient.score, self.patient.pre_score + 2)

    def test_calculate_score_with_potential_randomly_added_score(self):
        patient = Patient("1", "fake", None, 10, None, None, None, 5, 10)
        patient.set_score(2)
        self.assertGreaterEqual(patient.score, patient.pre_score + 2)
        self.assertLessEqual(patient.score, patient.pre_score + 2 + 10)



