EARTH_RADIUS = 6371
EARTH_CIRCUIT = 40075

# Path to the patients json file
PATIENTS_FILE_PATH = 'sample-data/patients.json'
# Default range of top rated patients
TOP_PATIENT_RANGE = 10

AGE_WEIGHT_PERCENT = 10
ACCEPTED_OFFERS_WEIGHT_PERCENT = 30
CANCELED_OFFERS_WEIGHT_PERCENT = 30
MAX_REPLY_TIME_WEIGHT_PERCENT = 20
DISTANCE_WEIGHT_PERCENT = 10
# Which patients are defined with little behavior data - this is a percentage of the average behavior data
BEHAVIOR_PERCENT = 5
# Maximum age of human life
MAX_AGE = 150

# Precalculated percents
MAX_AGE_PERCENT = MAX_AGE / AGE_WEIGHT_PERCENT
PERCENT_MIN_BEHAVIOR = BEHAVIOR_PERCENT/100
