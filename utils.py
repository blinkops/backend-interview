from math import radians, cos, sin, asin, sqrt
from random import randint
from constants import *

def calculate_patients_score(patients,lat,lon):
    """ Gets a list of preproccessed patients list and returns the final score after taking distance into consideration.
    Args: 
        patients (list): The list of patients. Each patient has a 'scoreWithoutDistance' property.
    Returns:
        Nothing, adds the total score as a property to each dict in the list. 
    """
    for patient in patients:
        try:
            patient_lat = float(patient['location']['latitude'])
            patient_lon = float(patient['location']['longitude'])
            distance = haversine(lat, lon, patient_lat, patient_lon)
            distance_score = max(min(DISTANCE_WEIGHT - distance * DISTANCE_WEIGHT / MAX_DISTANCE, DISTANCE_WEIGHT),0)
        except:
            distance_score = randint(0, DISTANCE_WEIGHT)
        patient.update({'totalScore': patient['scoreWithoutDistance'] + distance_score })        

def calculate_patients_score_without_distance(patients):
    """ Gets a list of patients and adds their score without taking location into account.
    Args: 
        patients (list): The list of patients.
    Returns:
        Nothing, adds the score as a property to each dict in the list.
    """
    for patient in patients:
        score_without_distance = calculate_patient_score_without_distance(patient)
        patient.update({'scoreWithoutDistance': score_without_distance })
    
def calculate_patient_score_without_distance(patient):
    """ Gets a patient and calculates the patient's score without taking location into account.
    Args: 
        patient (dict): The patient to be computed.
    Returns:
        score (number): The patient's score.
    """
    try:
        cancelled_offers = int(patient['canceledOffers'])
        if (cancelled_offers < 0):
            raise Exception
        cancelled_offers_score = max(min(CANCELLED_OFFERS_WEIGHT - (cancelled_offers * CANCELLED_OFFERS_WEIGHT) / MAX_CANCELLED_OFFERS, CANCELLED_OFFERS_WEIGHT),0)
    except:
        cancelled_offers_score = randint(0, CANCELLED_OFFERS_WEIGHT)
    try:
        accepted_offers = int(patient['acceptedOffers'])
        if (accepted_offers < 0):
            raise Exception
        accepted_offers_score = min(accepted_offers * ACCEPTED_OFFERS_WEIGHT / MAX_ACCEPTED_OFFERS, ACCEPTED_OFFERS_WEIGHT)
    except:
        accepted_offers_score = randint(0, ACCEPTED_OFFERS_WEIGHT)
    try:
        reply_time = int(patient['averageReplyTime'])
        if (reply_time < 0):
            raise Exception
        reply_time_score = max(min(REPLY_TIME_WEIGHT - reply_time * REPLY_TIME_WEIGHT / MAX_REPLY_TIME, REPLY_TIME_WEIGHT),0)
    except:
        reply_time_score = randint(0, REPLY_TIME_WEIGHT)
    try:
        age = int(patient['age'])
        if (age < 0):
            raise Exception
        age_score = min(age * AGE_WEIGHT / MAX_AGE, AGE_WEIGHT)
    except:
        age_score = randint(0, AGE_WEIGHT)
    return cancelled_offers_score + accepted_offers_score + reply_time_score + age_score

def haversine(lat1, lon1, lat2, lon2):
    """ Gets 2 coordinates and returns the distance between them.
    Args: 
        lat1, lon1, lat2, lon2 (float): The latitude/longitude coordinates.
    Returns:
        km (number): The distance in kilometers.
    """
    R = 6372.8      # Earth's radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    km = R * c
    return km