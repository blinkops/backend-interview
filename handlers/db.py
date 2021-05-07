import json

from handlers.models import create_patient


def init_db(path):
    """
    Initialize in-memory database

    :param path: location of the json format file with patients data
    :return: list of patients
    """
    try:
        patients = list()
        with open(path) as f:
            lines = json.load(f)
            print(f'{len(lines)} lines loaded from {path=}')
            for line in lines:
                patients.append(create_patient(data=line))
            return patients
    except Exception as error:
        err_msg = f'Failed to load data from {path=}, {error=}'
        print(err_msg)
        raise err_msg
