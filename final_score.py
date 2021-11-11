from typing import List, Dict, Any

from pre_score import calculate_score_by_field
from default_values import HIGHER_IS_BETTER


def set_score(patients_objects_list: List['Patient'], location: 'Location', max_score: int) -> None:
    """
    Set score for each patient, uses the calculate_score_by_field function inorder
     to get the score of the distance. And use Patient().set_score inorder to set patient score.

    :param patients_objects_list: list of patients
    :param location: location object
    :param max_score: the maximum score for distance (based on 'Weighting Categories')
    :return: None
    """

    scores, patients_sorted_by_distance = \
        calculate_score_by_field(patients_objects_list, "location", location, not HIGHER_IS_BETTER["location"], max_score)

    for i, patient in enumerate(patients_sorted_by_distance):
        patient.set_score(scores[i])


def get_top_list(patients_objects_list: List['Patient'], top_n: int) -> List['Patient']:
    """
    Get the top n patients by score.

    n = numbers of patients
    runtime: O(nlogn)
    space: O(n)
    (can be done with runtime = O(n * top_n) and space = O(top_n),
     but I believe it is more elegant and maintainability solution)

    :param patients_objects_list: list of patients
    :param top_n: number of patients to get
    :return: list sorted by score (length = top_n) of patients with the highest score
    """

    patients_sorted_by_score = sorted(patients_objects_list, key=lambda patient: patient.score, reverse=True)
    return patients_sorted_by_score[:top_n]
