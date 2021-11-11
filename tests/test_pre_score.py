from unittest import TestCase
from typing import Any

from pre_score import create_sorted_list_by_field, calculate_score_by_field, set_pre_score_by_field
from default_values import RELEVANT_FIELDS, HIGHER_IS_BETTER, FIELD_TO_MAX_SCORE
from location import Location

from .utils import patients_objects_list, _test_list_is_sorted, _test_list_of_patients_is_sorted


class TestCreateSortedListByField(TestCase):

    def _test_create_sorted_list_by_field(self, field: str, default: Any, reverse: bool):
        sorted_list = create_sorted_list_by_field(patients_objects_list, field, default, reverse)
        self.assertIsInstance(sorted_list, list)
        _test_list_of_patients_is_sorted(self, sorted_list, field, default, reverse)

    def test_create_sorted_list_by_field_with_relevant_fields(self):
        for field in RELEVANT_FIELDS:
            default = -1 if HIGHER_IS_BETTER[field] else float('inf')
            self._test_create_sorted_list_by_field(field, default, not HIGHER_IS_BETTER[field])

    def test_create_sorted_list_by_field_with_location(self):
        self._test_create_sorted_list_by_field("location", Location(0, 0), not HIGHER_IS_BETTER["location"])


class TestCalculateScoreByField(TestCase):
    def test_calculate_score_by_field(self):
        for field in RELEVANT_FIELDS:
            default = -1 if HIGHER_IS_BETTER[field] else float('inf')
            scores, patients_sorted_by_field = \
                calculate_score_by_field(patients_objects_list, field, default, not HIGHER_IS_BETTER[field],
                                         FIELD_TO_MAX_SCORE[field])

            self.assertIsInstance(scores, list)
            self.assertIsInstance(patients_sorted_by_field, list)
            _test_list_of_patients_is_sorted(self, patients_sorted_by_field, field, default,
                                             not HIGHER_IS_BETTER[field])
            _test_list_is_sorted(self, scores, False)

            # Test update for potential_randomly_added_score when score == 0
            for i, patient in enumerate(patients_sorted_by_field):
                if scores[i] == 0:
                    self.assertGreaterEqual(patient.potential_randomly_added_score, FIELD_TO_MAX_SCORE[field])


class TestSetPreScoreByField(TestCase):

    def test_set_pre_score_by_field(self):
        for field in RELEVANT_FIELDS:
            default = -1 if HIGHER_IS_BETTER[field] else float('inf')
            set_pre_score_by_field(patients_objects_list, field, default, not HIGHER_IS_BETTER[field],
                                   FIELD_TO_MAX_SCORE[field])
            self.assertGreater(patients_objects_list[0].pre_score, 0)
            self.assertGreater(patients_objects_list[5].potential_randomly_added_score, 0)
