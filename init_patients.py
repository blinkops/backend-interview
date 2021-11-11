from typing import List, Dict, Any, Optional

from patient import Patient
from location import Location


def init_patient_location_object_from_json(location: Optional[Dict[str, str]]) -> Optional[Location]:
    """
    Initialize location object from json

    :param location: from json
    :return: Location object if location is not None and valid, else None
    """

    if location is None:
        return None
    try:
        return Location(float(location["latitude"]), float(location["longitude"]))
    except TypeError:
        return None


def init_patient_object_form_json(patient: Dict[str, Any]) -> Patient:
    """
    Initialize patient object from json
    *assumes that every field is present in json file and that for every value the type is valid or None*
    :param patient: from json
    :return: Patient object
    """

    location = init_patient_location_object_from_json(patient["location"])
    return Patient(patient["id"], patient["name"], location, patient["age"],
                   patient["acceptedOffers"], patient["canceledOffers"],
                   patient["averageReplyTime"])


def init_patients_objects(patients: List[Dict[str, Any]]) -> List[Patient]:
    """
    Initialize patients objects

    :param patients: from json file
    :return: list of Patient objects
    """

    patients_objects_list = []
    for patient in patients:
        patients_objects_list.append(init_patient_object_form_json(patient))
    return patients_objects_list
