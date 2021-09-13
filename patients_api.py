import patients_logic
from flask import Flask, request, abort
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Patients(Resource):
    def get(self):
        try:
            location = parse_location(request.args.get('location', str))
        except ValueError:
            abort(404, description='Error: invalid location.')
        
        try:
            patients_logic.get_top_list(location)
        except Exception as e:
            abort(404, description=e.__str__())


api.add_resource(Patients, '/patients')


def parse_location(location):
    '''
    Parses a location string where latitude and longitude are separated by a comma,
    and creates a Location object from it.

    Parameters
    ----------
    location : str
        String containing a location where latitude and longitude are separated by a comma.

    Raises
    ------
    ValueError
        If the location is invalid, a ValueError is raised.

    Returns
    -------
    Location
        Location object containing the given latitude and longitude.
    '''

    if ',' not in location:
        raise ValueError

    try:
        lat, long = map(float, location.split(','))
    except:
        raise

    if lat < patients_logic.MIN_LATITUDE or lat > patients_logic.MAX_LATITUDE or long < patients_logic.MIN_LONGITUDE or long > patients_logic.MAX_LONGITUDE:
        raise ValueError

    return patients_logic.Location(lat, long)

if __name__ == '__main__':
    app.run()