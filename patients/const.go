package patients

import "math"

const (
	earthRadius  = 6371
	earthCircuit = 40075

	// Path to the patients json file
	filePath = "sample-data/patients.json"

	// TopPatientRange defined default range of top rated patients
	TopPatientRange = 10

	ageWeightPercent            = 10
	acceptedOffersWeightPercent = 30
	canceledOffersWeightPercent = 30
	maxReplyTimeWeightPercent   = 20
	distanceWeightPercent       = 10

	// Maximum age of human life
	maxAge = 150

	// Pre-calculated percents
	maxAgePercent = maxAge / ageWeightPercent
	// Which patients are defined with little behavior data - this is a percentage of the average behavior data
	percentMinBehavior = 0.05
	degreesToRadians   = math.Pi / 180
)
