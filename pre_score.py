from typing import List, Any, Tuple, Dict


def create_sorted_list_by_field(patients_objects_list: List['Patient'], field: str, default: Any, reverse: bool) \
        -> List['Patient']:
    """
    Creates a sorted list of patients by the given field.
    :param patients_objects_list: list of patients objects
    :param field: the field to sort by
    :param default: the default value for the field
    :param reverse: True if the list should be sorted in reverse order
    :return: list of sorted patients
    """

    return sorted(patients_objects_list, key=lambda patient: patient.get_by_field(field, default), reverse=reverse)


def calculate_score_by_field(patients_objects_list: List['Patient'], field: str, default: Any, reverse: bool,
                             max_score: int) -> Tuple[List[float], List['Patient']]:
    """
    Calculates the score of a given field for each patient based on the field and the max_score by
     sorting the list against the patient.get(field).

    function magic:
     create a sorted list of patients by the given field with 'function create_sorted_list_by_field',
     i =  index of the patient in sorted_list, score = (i / len(patients_sorted_list) - 1) * max_score.
     If some patients have the same value they will get the same score. If patient.field is null the score
     will be 0, but it will add the max_score to the potential_randomly_added_score field to enable patients
     with little behavior data still have a chance to be selected.

    :param patients_objects_list: list of patients objects
    :param field: the field to calculate the score for (the list of patients is sorted by this field)
    :param default: the default value for the field
    :param reverse: True if the list should be sorted in reverse order
    :param max_score: the maximum score for the given field (based on 'Weighting Categories')
    :return: (list of scores, list of patients sorted by the given field)
    """

    patients_sorted_list = create_sorted_list_by_field(patients_objects_list, field, default, reverse)
    last_value = None
    last_index = None
    scores = []
    for i, patient in enumerate(patients_sorted_list):
        # score is 0 if the patient.field is null, but it will add the max_score to the 'potential_randomly_added_score'
        if patient.__getattribute__(field) is None:
            patient.potential_randomly_added_score += max_score
            score = 0.0

        # score will be the same as the last patient
        elif last_value is not None and last_index is not None and patient.get_by_field(field, default) == last_value:
            score = (last_index / (len(patients_sorted_list) - 1)) * max_score

        else:
            score = (i / (len(patients_sorted_list) - 1)) * max_score
            last_index = i
            last_value = patient.get_by_field(field, default)

        scores.append(round(score, 10))

    return scores, patients_sorted_list


def set_pre_score_by_field(patients_objects_list: List['Patient'], field: str, default: Any, reverse: bool,
                           max_score: int) -> None:
    """
    Update the pre_score to the patients_objects by a given field. Uses the calculate_score_by_field function.

    :param patients_objects_list: list of patients objects
    :param field: the field to calculate the score for (the list of patients is sorted by this field)
    :param default: the default value for the field
    :param reverse: True if the list should be sorted in reverse order
    :param max_score: the maximum score for the given field (based on 'Weighting Categories')
    :return: None
    """

    scores, patients_sorted_list = calculate_score_by_field(patients_objects_list, field, default, reverse, max_score)

    for i, patient in enumerate(patients_sorted_list):
        if patient.get_by_field(field, default) != default:
            patient.pre_score += scores[i]


def set_pre_score(patients_objects_list: List['Patient'], relevant_fields: List[str],
                  higher_is_better: Dict[str, bool], field_to_max_score: Dict[str, bool]) -> None:
    """
    Update the pre_score to the patients_objects by the relevant_fields. Uses the set_pre_score_by_field function.
    :param patients_objects_list: list of patients objects
    :param relevant_fields: ["age", "acceptedOffers", "canceledOffers", "averageReplyTime"]
    :param higher_is_better: {"age": True, "acceptedOffers": True, "canceledOffers": False, "averageReplyTime": False}
    :param field_to_max_score: {"age": 1, "acceptedOffers": 3, "canceledOffers": 3, "averageReplyTime": 2, "location": 1}
    :return: None
    """

    for i, field in enumerate(relevant_fields):
        default = -1 if higher_is_better[field] else float('inf')
        set_pre_score_by_field(patients_objects_list, field, default, not higher_is_better[field],
                               field_to_max_score[field])
