from flask import Flask

from app import create_app, DATA_PATH
from handlers.db import init_db
from handlers.routes import configure_routes, ERROR_MSG_LATITUDE_LONGITUDE_MANDATORY, ERROR_MSG_LOCATION_MANDATORY


def test_base_route():
    app = create_app()
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Server up and running!'


def test_patients_location_route_success():
    app = create_app()
    client = app.test_client()
    lat = 46.7110
    lng = -63.1150
    url = f'/patients?location={lat},{lng}'

    expected_result = '["7277e23c-92f3-47dd-85a3-6dde34d99a6e", "16adefef-536a-48db-a0b6-e3e74be0bb3e", "9c62af0b-1c3e-49f1-96d0-b0a6b2749680", "ea702069-2438-4113-b8f9-4dd7a775e19d", "3a33c442-61c7-477d-bcc6-a0c1f9890641", "a0f6e833-b043-48ee-828c-8ceb06ba159c", "b56a2c2b-4ece-43c9-b519-514248a98a09", "0e1e688e-52c9-4f4f-845b-90107b727cd7", "08eae1b3-526b-49ba-96d2-8456679d102e", "62df6709-d811-48dd-bb44-d8a38a06bef8"]'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == expected_result
    assert response.get_data() == str.encode(expected_result)


def test_patients_location_route_location_missing():
    app = create_app()
    client = app.test_client()
    url = f'/patients'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == ERROR_MSG_LOCATION_MANDATORY


def test_patients_location_route_location_empty():
    app = create_app()
    client = app.test_client()
    url = f'/patients?location='
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == ERROR_MSG_LOCATION_MANDATORY


def test_patients_location_route_location_not_valid():
    app = create_app()
    client = app.test_client()
    lat = 46.7110
    lng = 200
    url = f'/patients?location={lat},{lng}'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == ERROR_MSG_LOCATION_MANDATORY


def test_patients_location_route_latitude_missing():
    app = create_app()
    client = app.test_client()
    lat = ''
    lng = -63.1150
    url = f'/patients?location={lat},{lng}'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == ERROR_MSG_LATITUDE_LONGITUDE_MANDATORY


def test_patients_location_route_longitude_missing():
    app = create_app()
    client = app.test_client()
    lat = 46.7110
    lng = ''
    url = f'/patients?location={lat},{lng}'
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_data(as_text=True) == ERROR_MSG_LATITUDE_LONGITUDE_MANDATORY


def test_patients_location_route_bad_parameters():
    app = create_app()
    client = app.test_client()
    lat = 46.7110
    lng = None
    url = f'/patients?location={lat},{lng}'
    response = client.get(url)
    assert response.status_code == 500
