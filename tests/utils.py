from typing import List, Any
import json

from init_patients import init_patients_objects


with open('sample-data\patients_test.json', 'r') as f:
    patients = json.load(f)

patients_objects_list = init_patients_objects(patients)


def _test_list_of_patients_is_sorted(self, lst: List['Patient'], field: str, default: Any, reverse: bool):
    for i in range(len(lst) - 1):
        if reverse:
            self.assertGreaterEqual(lst[i].get_by_field(field, default), lst[i + 1].get_by_field(field, default))
        else:
            self.assertLessEqual(lst[i].get_by_field(field, default), lst[i + 1].get_by_field(field, default))


def _test_list_is_sorted(self, lst: List[Any], reverse: bool):
    for i in range(len(lst) - 1):
        if reverse:
            self.assertGreaterEqual(lst[i], lst[i + 1])
        else:
            self.assertLessEqual(lst[i], lst[i + 1])
