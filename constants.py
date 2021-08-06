AGE_WEIGHT = 1
DISTANCE_WEIGHT = 1
ACCEPTED_OFFERS_WEIGHT = 3
CANCELLED_OFFERS_WEIGHT = 3
REPLY_TIME_WEIGHT = 2
TOTAL_WEIGHT = AGE_WEIGHT + DISTANCE_WEIGHT + ACCEPTED_OFFERS_WEIGHT + CANCELLED_OFFERS_WEIGHT + REPLY_TIME_WEIGHT

"""
These are the maximum values for each category. 
The scores will increase / decrease linearly between 0 and the max value.
Any number above the specified max will grant the patient the maximum score for this category.
For example: Age 0 grants 0 score. Age 80 grants the max score (AGE_WEIGHT). Age 150 also grants the max score.
0 reply time will grant max score. 1200 seconds reply time will grant 0 score. 3500 reply time will also grant 0 score.
"""
MAX_ACCEPTED_OFFERS = 100
MAX_CANCELLED_OFFERS = 100
MAX_AGE = 80
MAX_REPLY_TIME = 1200
MAX_DISTANCE = 1500

DEFAULT_LOCAL_URL = 'http://localhost:5000'