import json
from flask import request

from handlers.models import get_patients_score_by_location, Location, create_location

ERROR_MSG_LOCATION_MANDATORY = 'Failed to process request, valid location is mandatory'
ERROR_MSG_LATITUDE_LONGITUDE_MANDATORY = 'Failed to process request, valid latitude and longitude are mandatory'


def configure_routes(app):
    @app.route('/')
    def index():
        return 'Server up and running!'

    @app.route('/patients', methods=['GET'])
    def get_patients():
        """
        Get top 10 patients, patients most likely to accept the offer off the wait list
        by given mandatory argument `location` with `latitude,longitude` values

        :return:
        """
        try:
            location = request.args.get('location')

            if not location or ',' not in location:
                print(ERROR_MSG_LOCATION_MANDATORY)
                return ERROR_MSG_LOCATION_MANDATORY, 400

            lat, lng = location.split(',')
            if not lat or not lng:
                print(ERROR_MSG_LATITUDE_LONGITUDE_MANDATORY)
                return ERROR_MSG_LATITUDE_LONGITUDE_MANDATORY, 400

            location = create_location(data={"latitude": lat, "longitude": lng})
            if not location.is_valid():
                print(ERROR_MSG_LOCATION_MANDATORY)
                return ERROR_MSG_LOCATION_MANDATORY, 400

            patients = get_patients_score_by_location(
                patients=app.db,
                location=location)
            return json.dumps([p.patient_id for p in patients]), 200

        except Exception as error:
            err_msg = f'Failed to process request, {error=}'
            print(err_msg)
            return err_msg, 500
