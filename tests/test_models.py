from app import DATA_PATH, SHORT_DATA_PATH
from handlers.db import init_db
from handlers.models import get_patients_score_by_location, create_patient, create_location

EXAMPLE_LOCATION = {
    "latitude": "86.7110",
    "longitude": "-83.1150"
}

EXAMPLE_PATIENT_DICT = {
    "id": "541d25c9-9500-4265-8967-240f44ecf723",
    "name": "Samir Pacocha",
    "location": {
        "latitude": "46.7110",
        "longitude": "-63.1150"
    },
    "age": 46,
    "acceptedOffers": 49,
    "canceledOffers": 92,
    "averageReplyTime": 2598
}

PATIENT_WITH_LITTLE_BEHAVIOR_DICT = {
    "id": "00000000000000000000000000000000",
    "name": "Bernard Mosciski",
    "location": {
        "latitude": "-81.0341",
        "longitude": "144.9963"
    },
    "age": 21,
    "acceptedOffers": 0,
    "canceledOffers": 0,
    "averageReplyTime": 0
}


def test_create_location():
    location = create_location(data=EXAMPLE_LOCATION)
    assert location


def test_location_valid_true():
    location = create_location(data=EXAMPLE_LOCATION)
    assert location
    assert location.is_valid()


def test_location_valid_false():
    location = create_location(data=EXAMPLE_LOCATION)
    assert location
    location.longitude = 181
    assert location.is_valid() is False


def test_location_to_tuple():
    location = create_location(data=EXAMPLE_LOCATION)
    assert location
    latitude = float(EXAMPLE_LOCATION.get('latitude'))
    longitude = float(EXAMPLE_LOCATION.get('longitude'))
    assert location.to_tuple() == (latitude, longitude)


def test_create_patient():
    patient = create_patient(data=EXAMPLE_PATIENT_DICT)
    assert patient


def test_patient_repr():
    patient = create_patient(data=EXAMPLE_PATIENT_DICT)
    assert patient
    assert EXAMPLE_PATIENT_DICT.get('id') == str(patient)


def test_patient_get_distance():
    patient = create_patient(data=EXAMPLE_PATIENT_DICT)
    expected_patient_distance = 4483.06038068168
    assert patient
    location = create_location(data=EXAMPLE_LOCATION)
    assert patient.get_distance(location=location) == expected_patient_distance


def test_patient_get_score():
    patient = create_patient(data=EXAMPLE_PATIENT_DICT)
    expected_patient_score = -976.206038068168
    assert patient
    location = create_location(data=EXAMPLE_LOCATION)
    assert patient.get_score(location=location) == expected_patient_score


def test_two_patients_same_score():
    patient_1_dict = EXAMPLE_PATIENT_DICT.copy()
    patient_1 = create_patient(data=patient_1_dict)
    patient_2_dict = EXAMPLE_PATIENT_DICT.copy()
    patient_2_dict['id'] += 'F'
    patient_2 = create_patient(data=patient_2_dict)
    location = create_location(data=EXAMPLE_LOCATION)
    assert patient_1.get_score(location=location) == patient_2.get_score(location=location)


def test_two_patients_different_age_different_score():
    patient_1_dict = EXAMPLE_PATIENT_DICT.copy()
    patient_1 = create_patient(data=patient_1_dict)
    patient_2_dict = EXAMPLE_PATIENT_DICT.copy()
    patient_2_dict['id'] += 'F'
    patient_2_dict['age'] += 1
    patient_2 = create_patient(data=patient_2_dict)
    location = create_location(data=EXAMPLE_LOCATION)
    assert patient_1.get_score(location=location) != patient_2.get_score(location=location)


def test_patients_sort_by_score():
    patients = init_db(path=DATA_PATH)
    expected_sorted_patients_ids = ['25e9a7fe-7bc8-44b8-8235-f3a91a6332e8',
                                    '285c73a6-0b8f-4a49-bc43-4bed139d2dff',
                                    'bfd86a1d-4b74-4669-b8a9-32580a7546b6',
                                    '59dbc70b-276e-4c46-b2b8-d44104e11c56',
                                    'a4080fe9-dd45-4b2b-bd30-8b87023946cd',
                                    '382f7799-de58-430b-986c-e1555e8db2b0',
                                    'e3e6c7ce-d847-4e87-bc36-6103781aeb2c',
                                    'f770dd7a-f3f7-4b01-a54e-d6214aa24838',
                                    '469caf18-51a6-4284-8f9e-47d9f580d701',
                                    'c0ebff1c-ce08-4db0-97dc-2c77eca1bc0c']

    location = create_location(data=EXAMPLE_LOCATION)
    sorted_patients = get_patients_score_by_location(patients=patients, location=location)
    assert len(expected_sorted_patients_ids) == len(sorted_patients)
    assert all([a == b.patient_id for a, b in zip(expected_sorted_patients_ids, sorted_patients)])


def test_get_patients_score_by_location_no_patients_failure():
    location = create_location(data=EXAMPLE_LOCATION)
    sorted_patients = get_patients_score_by_location(patients=None, location=location)
    assert sorted_patients is None


def test_get_patients_score_by_location_no_location_failure():
    patients = init_db(path=DATA_PATH)
    sorted_patients = get_patients_score_by_location(patients=patients, location=None)
    assert sorted_patients is None


def test_patients_with_little_behavior_data():
    patients = init_db(path=SHORT_DATA_PATH)
    new_patient = create_patient(data=PATIENT_WITH_LITTLE_BEHAVIOR_DICT)
    patients.append(new_patient)
    expected_sorted_patients_ids = [PATIENT_WITH_LITTLE_BEHAVIOR_DICT.get('id'),
                                    '0f84387c-f659-44cf-894c-6b47a3dac36a',
                                    '16adefef-536a-48db-a0b6-e3e74be0bb3e',
                                    'a0f6e833-b043-48ee-828c-8ceb06ba159c',
                                    '1ba1b882-6516-4e54-a1ef-453bb3137d02',
                                    '541d25c9-9500-4265-8967-240f44ecf723',
                                    'a21a7ea6-4c4e-4d00-b492-e43e2c71c8f7',
                                    '00ad0d71-193d-458c-8a61-ba1b233cd6df',
                                    'c4dc7b5c-0899-4500-b158-19f535bda9d6',
                                    '9e728f2b-b5a4-4afa-a8e3-4e0587421149']

    location = create_location(data=EXAMPLE_LOCATION)
    sorted_patients = get_patients_score_by_location(patients=patients, location=location)
    print(sorted_patients)
    assert len(expected_sorted_patients_ids) == len(sorted_patients)
    assert all([a == b.patient_id for a, b in zip(expected_sorted_patients_ids, sorted_patients)])
