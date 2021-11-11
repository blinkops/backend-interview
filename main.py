# create patients_objects_list and set pre score

import json
from default_values import PATH, RELEVANT_FIELDS, HIGHER_IS_BETTER, FIELD_TO_MAX_SCORE
from init_patients import init_patients_objects
from pre_score import set_pre_score


with open(PATH, 'r') as f:
    patients = json.load(f)

patients_objects_list = init_patients_objects(patients)
set_pre_score(patients_objects_list, RELEVANT_FIELDS, HIGHER_IS_BETTER, FIELD_TO_MAX_SCORE)
