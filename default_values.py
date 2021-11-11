# location values
MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180

# scores values
RELEVANT_FIELDS = ["age", "acceptedOffers", "canceledOffers", "averageReplyTime"]
HIGHER_IS_BETTER = \
    {"age": True, "acceptedOffers": True, "canceledOffers": False, "averageReplyTime": False, "location": False}
FIELD_TO_MAX_SCORE = {"age": 1, "acceptedOffers": 3, "canceledOffers": 3, "averageReplyTime": 2, "location": 1}

# files values
PATH = "sample-data\patients.json"

# server values
NUMBER_OF_PATIENTS_TO_RETURN = 10
