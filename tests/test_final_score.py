from unittest import TestCase

from pre_score import set_pre_score
from location import Location
from default_values import RELEVANT_FIELDS, HIGHER_IS_BETTER, FIELD_TO_MAX_SCORE, NUMBER_OF_PATIENTS_TO_RETURN
from final_score import set_score, get_top_list

from .utils import patients_objects_list, _test_list_of_patients_is_sorted

set_pre_score(patients_objects_list, RELEVANT_FIELDS, HIGHER_IS_BETTER, FIELD_TO_MAX_SCORE)


class TestSetScore(TestCase):
    def test_set_score(self):
        location = Location(0, 0)
        set_score(patients_objects_list, location, 1)
        for patient in patients_objects_list:
            if patient.potential_randomly_added_score != 0:
                self.assertGreater(patient.score, patient.pre_score)
            else:
                self.assertGreaterEqual(patient.score, patient.pre_score)


class TestGetTopList(TestCase):
    def test_get_top_list(self):
        location = Location(0, 0)
        set_score(patients_objects_list, location, 1)
        top_list = get_top_list(patients_objects_list, NUMBER_OF_PATIENTS_TO_RETURN)
        self.assertEqual(len(top_list), NUMBER_OF_PATIENTS_TO_RETURN)
        _test_list_of_patients_is_sorted(self, top_list, 'score', 0, True)

