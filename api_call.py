import requests
import json

BASE = 'http://127.0.0.1:5000/'

def api_request(location):
    '''
    Sends a get request to the API to get the top patients list, and prints it.
    If an error occurred and the server returned a response with a 404 status code,
    the error will be printed.

    Parameters
    ----------
    location : str
        The facility's location, latitude and longitude separated by a comma.
    '''
    response = requests.get(BASE + f'patients?location={location}')

    if response.status_code == 200:    
        print(json.dumps(json.loads(response.json()), indent=4))
    else:
        print(response.json())


def main():
    location = input('Enter location (lat,long): ')
    api_request(location)

if __name__ == '__main__':
    main()