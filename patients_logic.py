import json
import math
import random
import re

DEFAULT_PATIENTS_DATA_FILE = 'sample-data\patients.json'
MIN = 0
MAX = 1
TO_KM = 1.609344
PATIENT_ID_LEN = 36

MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180


class InvalidFileError(Exception):
    def __init__(self):
        super().__init__("Invalid patients data file: file doesn't contain json serialized data.")


class InvalidAttributeError(Exception):
    def __init__(self, attr_name, attr_value):
        super().__init__(f'Invalid attribute: \'{attr_value}\' is not a valid value for the \'{attr_name}\' attribute.')


class Location():
    '''
    A class used to represent a location.

    Attributes
    ----------
    _latitude : float
        The location's latitude.

    _longitude : float
        The location's longitude.

    Methods
    -------
    __eq__(other)
        Checks whether two Location objects point to the same location.

    distance(other)
        Calculates the distance between the location and another location.
    '''
    def __init__(self, latitude, longitude):
        self._latitude = float(latitude)
        self._longitude = float(longitude)

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude

    def __eq__(self, other):
        '''
        Checks whether two Location objects point to the same location.

        Parameters
        ----------
        other : Location
            A Location object to compare the current Location object to.

        Returns
        -------
            If other is an instance of Location, returns True if both instances point to the same location.
            Otherwise, returns False.
            If other is not an instance of Location, returns NotImplemented.
        '''

        if isinstance(other, Location):            
            return (self._latitude == other.get_latitude() and
                    self._longitude == other.get_longitude())
                    
        return NotImplemented


    def distance(self, other):
        '''
        Calculates the distance between the location and another location.

        Parameters
        ----------
        other : Location
            The other location to calculate distance from.

        Returns
        -------
        float
            The distance in kilometers between the two locations.
        '''

        # If both locations are the same, the distance between them is 0.
        if (self == other):
            return 0

        # Calculate the distance between the two locations using the Spherical Law of Cosines.
        else:
            lat1, lat2, long1, long2 = self._latitude, other.get_latitude(), self._longitude, other.get_longitude()

            theta = long1 - long2
            dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515

            # Return the distance in kilometers, accurate to 2 decimal places.
            return round(miles * TO_KM, 2)


class Patient():
    '''
    A class used to represent a patient.

    Attributes
    ----------
    _id : str
        The patient's id.
    
    _name : str
        The patient's name.
    
    _age : int
        The patient's age.

    _location : Location
        The patient's location (latitude and longitude).

    _distance : float
        The patient's distance from the given location.

    _accepted_offers : int
        The number of offers the patient has accepted in the past.

    _cancelled_offers : int
        The number of offers the patient has cancelled in the past.

    _average_reply_time : int
        The patient's average reply time, in seconds.

    Methods
    -------
    __eq__(other)
        Checks whether two Patient objects point to the same patient.

    all_attributes_valid()
        Checks whether the patient has data for all their attributes.

    calculate_score(comparison_values)
        Calculates the patient's score based on their attributes and the comparison values.
    '''
    def __init__(self, id, name, age, location, distance, accepted_offers=None, cancelled_offers=None, average_reply_time=None):
        self._id = id
        self._name = name
        self._age = age
        self._location = location
        self._distance = distance
        self._accepted_offers = accepted_offers
        self._cancelled_offers = cancelled_offers
        self._average_reply_time = average_reply_time

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_location(self):
        return self._location

    def get_distance(self):
        return self._distance

    def get_accepted_offers(self):
        return self._accepted_offers

    def get_cancelled_offers(self):
        return self._cancelled_offers

    def get_average_reply_time(self):
        return self._average_reply_time

    def __eq__(self, other):
        '''
        Checks whether two Patient objects point to the same patient.

        Parameters
        ----------
        other : Patient
            A Patient object to compare the current Patient object to.

        Returns
        -------
            If other is an instance of Patient, returns True if both instances point to the same patient.
            Otherwise, returns False.
            If other is not an instance of Patient, returns NotImplemented.
        '''

        if isinstance(other, Patient):            
            return (self._id == other.get_id() and
                    self._name == other.get_name() and
                    self._age == other.get_age() and
                    self._location == other.get_location() and
                    self._accepted_offers == other.get_accepted_offers() and
                    self._cancelled_offers == other.get_cancelled_offers() and
                    self._average_reply_time == other.get_average_reply_time())

        return NotImplemented


    def all_attributes_valid(self):
        '''
        Checks whether the patient has data for all their behavior attributes.

        Returns
        -------
        bool
            True if patient has data for all the behavior attributes, False otherwise.
        '''

        if self._accepted_offers is None or self._cancelled_offers is None or self._average_reply_time is None:
            return False
        return True


    def calculate_score(self, comparison_values):
        '''
        Calculates the patient's score (1-10) based on their attributes and the comparison values.
        Age - weighted 10%.
        Distance - weighted 10%.
        Accepted offers - weighted 30%.
        Cancelled offers - weighted 30%.
        Average reply time - weighted 20%.

        Parameters
        ----------
        comparison_values : dict
            A dictionary containing all the maximum and minimum values
            of the different fields, used to calculate the score of
            the patient.

        Returns
        -------
        int
            The patient's score based on their attributes and the comparison values.
            If the score can't be calculated, returns None.
        '''

        # If the patient doesn't have data for all the attributes, their score can't be
        # calculated, therefore None is returned.
        if not self.all_attributes_valid():
            return None

        score = 0

        score += scale(comparison_values['age'], (0, 1), self._age)
        score += scale(comparison_values['distance'], (0, 1), self._distance, True)
        score += scale(comparison_values['accepted_offers'], (0, 3), self._accepted_offers)
        score += scale(comparison_values['cancelled_offers'], (0, 3), self._cancelled_offers, True)
        score += scale(comparison_values['average_reply_time'], (0, 2), self._average_reply_time, True)

        # Scaling from 0-10 to 1-10, since the minimum valid score is 1.
        score = scale((0, 10), (1, 10), score)

        return score

# Global variable containing the facility's location.
location = Location(0, 0)

def check_behavior_data(value, attr_name):
    '''
    Checks whether a behavior attribute is valid.

    Parameters
    ----------
    value : Any
        The value of a certain behavior attribute.

    attr_name : str
        The name of the behavior attribute.
    
    Raises
    ------
    InvalidAttributeError
        If the value is invalid, a InvalidAttributeError will be raised.
    '''

    if value is not None:
        try:
            accepted_offers = int(value)
            if accepted_offers < 0:
                raise InvalidAttributeError(attr_name, value)
        except ValueError:
            raise InvalidAttributeError(attr_name, value)


def check_values(patient):
    '''
    Checks whether all patient attributes have valid values.

    Parameters
    ----------
    patient : dict
        A dict containing a patient's data.
    
    Raises
    ------
    InvalidAttributeError
        If a value is invalid, a InvalidAttributeError will be raised.
    '''

    # Check if ID is valid. Regex explanation:
    # ^[a-z0-9]{8}- - ID starts with a sequence of 8 lowercase letters and digits followed by a hyphen.
    # ([a-z0-9]{4}-){3} - 3 sequences of 4 lowercase letters and digits, each followed by a hyphen.
    # [a-z0-9]{12}$ - ID ends with a sequence of 12 lowercase letters and digits.
    if len(patient['id']) != PATIENT_ID_LEN or not re.match('^[a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}$', patient['id']):
        raise InvalidAttributeError('id', patient['id'])

    # Check if the name is valid. Regex explanation:
    # ^[A-Z]\'? - Name starts with capital letter followed by an optional apostrophe (for example: D'angelo).
    # [a-z]+\.? - One or more lowercase letters followed by an optional period (for example: Dr. Adam).
    # \s - Whitespace.
    # [A-Z]\'? - Capital letter followed by an optional apostrophe (for example: O'brien).
    # [A-Za-z]+-?\s? - One or more uppercase or lowercase letters followed by an optional hyphen or whitespace (for example: Anna-Marie, O'Reilly).
    # ([A-Z]\'?[A-Za-z]*-?\s?)*? - Zero or more optional names, starting with a capital letter and an optional apostrophe,
    #                              followed by zero or more uppercase or lowercase letters (for example: Chester Yost II),
    #                              an optional hyphen and an optional whitespace.
    # [A-Za-z]$ - Name ends with an uppercase or lowercase letter and an optional period (for example: Benny Mann Sr.).
    if not re.match('^[A-Z]\'?[a-z]+\.?\s[A-Z]\'?[A-Za-z]+-?\s?([A-Z]\'?[A-Za-z]*-?\s?)*?[A-Za-z]\.?$', patient['name']):
        raise InvalidAttributeError('name', patient['name'])

    # Check if age is valid (integer between 0-120).
    try:
        age = int(patient['age'])
        if age < 0 or age > 120:
            raise InvalidAttributeError('age', patient['age'])
    except (ValueError, TypeError):
        raise InvalidAttributeError('age', patient['age'])

    # Check if latitude is valid (float between -90-90).
    try:
        lat = float(patient['location']['latitude'])
        if lat < MIN_LATITUDE or lat > MAX_LATITUDE:
            raise InvalidAttributeError('latitude', patient['location']['latitude'])
    except (ValueError, TypeError):
        raise InvalidAttributeError('latitude', patient['location']['latitude'])
    
    # Check if longitude is valid (float between -180-180).
    try:
        long = float(patient['location']['longitude'])
        if long < MIN_LONGITUDE or long > MAX_LONGITUDE:
            raise InvalidAttributeError('longitude', patient['location']['longitude'])
    except (ValueError, TypeError):
        raise InvalidAttributeError('longitude', patient['location']['longitude'])

    # Check if all behavioral attributes are valid (integers 0 and above).
    check_behavior_data(patient['acceptedOffers'], 'accepted offers')
    check_behavior_data(patient['canceledOffers'], 'cancelled offers')
    check_behavior_data(patient['averageReplyTime'], 'average reply time')

        
def patient_decoder(item):
    '''
    Parses a dictionary containing a single patient's data and creates
    a Patient object according to the given data.

    Parameters
    ----------
    item : dict
        A dict containing a patient's data.

    Returns
    -------
    Patient
        A patient object with the given data.
    '''
    if 'id' in item:
        # Check whether all attributes have valid values. If a value is invalid, a InvalidAttributeError will be raised.
        check_values(item)

        # Save the patient's location in order to use it in calculating the distance.
        patient_location = Location(item['location']['latitude'], item['location']['longitude'])

        # Calculate the patient's distance from the given location.
        distance = location.distance(patient_location)

        # Create and return the patient object.
        # If some behavior attributes are null, Python automatically converts them to None.
        return Patient(item['id'], item['name'], item['age'], patient_location, distance, item['acceptedOffers'], item['canceledOffers'], item['averageReplyTime'])
    return item


def is_valid_file(patients_data_file_path):
    '''
    Checks whether the data file contains valid json serialized data.

    Parameters
    ----------
    patients_data_file_path : str
        A string containing the path to the patients data file. 

    Returns
    -------
    bool
        True if the file contains valid json, False otherwise.
    '''
    
    with open(patients_data_file_path, 'r') as file:
        data = file.read()

    try:
        json.loads(data)
    except json.decoder.JSONDecodeError:
        return False
    return True


def parse_patients_data(patients_data_file_path):
    '''
    Reads data from the patients data file, parses it and returns a list of Patient objects.

    Parameters
    ----------
    patients_data_file_path : str
        A string containing the path to the patients json data file. 

    Returns
    -------
    list
        A list of Patient objects.
    '''

    # Read patients data from file.
    with open(patients_data_file_path, 'r') as patients_file:
        patients_data = patients_file.read()

    # Decode the json data.
    patients_data = json.loads(patients_data, object_hook=patient_decoder)

    return patients_data


def is_sortable(value):
    '''
    Checks whether the given value is sortable (has the methods used for sorting).

    Parameters
    ----------
    value : Any
        The value to check whether it is sortable.

    Returns
    -------
    bool
        True if the value is sortable, false otherwise.
    '''

    cls = value.__class__
    return cls.__lt__ != object.__lt__ or cls.__gt__ != object.__gt__


def get_min_max(gen):
    '''
    Returns the minimum and maximum value in a generator.

    Parameters
    ----------
    gen : generator
        A generator containing different comparable values.

    Raises
    ------
    StopIteration
        If the generator is empty, a StopIteration is raised.
    TypeError
        If the values in the generator are not comparable, a TypeError is raised.

    Returns
    -------
    tuple
        A tuple where the first element is the minimum value in the generator,
        and the second element is the maximum value in the generator.
    '''

    try:
        first = next(gen)
    except StopIteration:
        raise

    if not is_sortable(first):
        raise TypeError

    # Initialize minimum and maximum.
    max = first
    min = first

    for value in gen:
        if value > max:
            max = value
        elif value < min:
            min = value
    
    return (min, max)


def get_comparison_values(patients_data):
    '''
    Gets the minimum and maximum values for age, distance, accepted offers,
    cancelled offers and average reply time, and stores them in a dictionary.

    Parameters
    ----------
    patients_data : list
        A list of Patient objects.

    Returns
    -------
    dictionary
        A dictionary containing maximum and minimum values of the different attributes.
    '''

    comparison_values = {}

    # Get comparison values while ignoring None values, which belong to patients that have no data for a certain attribute.
    comparison_values['age'] = get_min_max(patient.get_age() for patient in patients_data)
    comparison_values['distance'] = get_min_max(patient.get_distance() for patient in patients_data)
    comparison_values['accepted_offers'] = get_min_max(patient.get_accepted_offers() for patient in patients_data)
    comparison_values['cancelled_offers'] = get_min_max(patient.get_cancelled_offers() for patient in patients_data)
    comparison_values['average_reply_time'] = get_min_max(patient.get_average_reply_time() for patient in patients_data)

    return comparison_values


def scale(old_range, new_range, value, reverse = False):
        '''
        Scales a value in the old range to a value in the new range using linear conversion.

        Parameters
        ----------
        old_range : tuple
            A tuple representing the old range, where the minimum is the first element and the maximum is the second element.

        new_range : tuple
            A tuple representing the new range, where the minimum is the first element and the maximum is the second element.

        value : float
            The value to scale from the old range to the new range.

        reverse : bool, default False
            A boolean indicating whether to reverse the old range. Used in cases where the lowest value gets the highest priority.
        
        Raises
        ------
        ValueError
            If the value is not within the original range, a ValueError is raised.

        Returns
        -------
        float
            A value representing the old value in the new range.
        '''

        # If the value is not within the old range, raise a ValueError.
        if value < old_range[MIN] or value > old_range[MAX]:
            raise ValueError

        # If the minimum and maximum in the old range are the same, the new value will be equal to the new maximum.
        if old_range[MAX] == old_range[MIN]:
            return new_range[MAX]

        if reverse:
            old_range = (old_range[MAX], old_range[MIN])

        return (new_range[MAX]-new_range[MIN])/(old_range[MAX]-old_range[MIN]) * (value-old_range[MIN]) + new_range[MIN]


def serialize_patients_list(patients_list):
    '''
    Serializes a list of Patient objects to json.

    Parameters
    ----------
    patients_list : list
        A list of Patient objects.

    Returns
    string
        A string containing the json serialized patient data.
    '''

    patients_json = []

    for patient in patients_list:
        patients_json.append({
            'id': patient.get_id(),
            'name': patient.get_name(),
            'location': {
                'latitude': str(format(patient.get_location().get_latitude(), '.4f')),
                'longitude': str(format(patient.get_location().get_longitude(), '.4f'))
            },
            'age': patient.get_age(),
            'acceptedOffers': patient.get_accepted_offers(),
            'canceledOffers': patient.get_cancelled_offers(),
            'averageReplyTime': patient.get_average_reply_time()
        })

    return json.dumps(patients_json)


def insert_no_score_patients(top_list, no_score_patients):
    '''
    Inserts a random number of patients who have no score to the top list
    of patients.

    Parameters
    ----------
    top_list : list
        A list of Patient objects, containing up to 10 patients with the highest scores.

    no_score_patients : list
        A list of Patient objects, containing all the patients who have little behavior data,
        meaning their score can't be computed.

    Returns
    list
        A list containing up to 10 patients, who have the highest scores or no score.
    '''

    # If there aren't any patients in the top list and only patients with no score,
    # shuffle the list of patients with no score and return the top list.
    if len(top_list) == 0:
        random.shuffle(no_score_patients)

        if len(no_score_patients) >= 10:
            return no_score_patients[:10]
        return no_score_patients[:len(no_score_patients)]

    # Add at most 5 patients with no score, as to still keep at least half of the patients with the highest score.
    range_max = 5
    
    if len(no_score_patients) < 5:
        range_max = len(no_score_patients)        
    
    # Pick a random number from 1-range_max (5 or less, based on the number of patients with no score).
    num = random.randint(1, range_max)

    # Remove the lowest scoring patients from the top list to make space for the no score patients.
    if len(top_list) < 10:
        if len(top_list) + num > 10:
            num_to_remove = len(top_list) + num - 10
            top_list = top_list[:len(top_list) - num_to_remove]
        # If there are less than 10 patients in the top list, add as many patients with no score as possible.
        else:
            num = 10 - len(top_list)

            if num > len(no_score_patients):
                num = len(no_score_patients)
    else:         
        top_list = top_list[:(10-num)]

    # Shuffle the list of no score patients as to select them randomly.
    random.shuffle(no_score_patients)

    # Insert the same number of patients with no score into the top list.
    for i in range(num):
        index = random.randint(0, len(top_list))
        right = top_list[:index]
        left = top_list[index:]
        top_list = right + [no_score_patients[i]] + left

    return top_list


def get_top_list(location_data, patients_data_file_path = DEFAULT_PATIENTS_DATA_FILE):
    '''
    Creates a list of the top 10 patients with the highest score,
    who are the most likely to accept the appointment offer.
    If there are patients who have little behavior data, they will be randomly
    inserted into the top 10 list as to give them a chance to be selected.

    Parameters
    ----------
    location_data : Location
        Location object containing the facility's location.

    patients_data_file_path : str, default DEFAULT_PATIENTS_DATA_FILE
        A string containing the path to the patients json data file.

    Raises
    ------


    Returns
    -------
    str
        A string containing the json serialized data of the top 10 patients.
    '''
    global location
    location = location_data
    no_score_patients, top_list = [], []

    if not is_valid_file(patients_data_file_path):
        raise InvalidFileError

    # Parse the list of patients.
    try:
        patients_data = parse_patients_data(patients_data_file_path)
    except InvalidAttributeError as e:
        raise e

    # Create a list containing patients who have little behavior data, meaning their score can't be
    # computed, and remove them from the original list.
    for i in range(len(patients_data) - 1, -1, -1):
        if not patients_data[i].all_attributes_valid():
            no_score_patients.append(patients_data[i])
            del patients_data[i]

    # If there are patients whose score can be calculated.
    if len(patients_data) > 0:
        # Get the dictionary of comparison values.
        comparison_values = get_comparison_values(patients_data)

        # Sort the list of patients based on their score.
        patients_data.sort(key=lambda patient: patient.calculate_score(comparison_values), reverse=True)

        # Get the top patients list.
        if len(patients_data) >= 10:
            top_list = patients_data[:10]
        else:
            top_list = patients_data

    # If there are patients who have little behavior data, they will be randomly
    # inserted into the top 10 list as to give them a chance to be selected.
    if len(no_score_patients) > 0:
        top_list = insert_no_score_patients(top_list, no_score_patients)

    # Serialize the top list to json.
    top_list_json = serialize_patients_list(top_list)

    return top_list_json