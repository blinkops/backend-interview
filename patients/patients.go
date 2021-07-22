/*
	Package patients provides functionality to load patients from file data and calculating their priorities.
*/

package patients

import (
	"sort"
)

// NewManagePatients create a new Patient structure object
func NewManagePatients(loadPatientsFromFile bool) *ManagePatients {
	patients := new(ManagePatients)
	patients.MaxAcceptedOffers = 1
	patients.MaxCanceledOffers = 1
	patients.MaxBehaviorIndex = 1
	patients.MaxReplyTime = 1
	if loadPatientsFromFile {
		patients.PatientsList = loadPatientListFromFile(filePath)
		patients.preProcessPatients()
		patients.preProcessPatientsPriority()
	}
	return patients
}

// Patient list pre-processing and calculate maximum of acceptedOffers, canceledOffers, averageReplyTime
// Also calculate the max_behavior_index used to define patients with little data about their behavior
func (patients *ManagePatients) preProcessPatients() {
	for i := range patients.PatientsList {
		currentPatient := &patients.PatientsList[i]

		if currentPatient.AcceptedOffers > patients.MaxAcceptedOffers {
			patients.MaxAcceptedOffers = currentPatient.AcceptedOffers
		}

		if currentPatient.CanceledOffers > patients.MaxCanceledOffers {
			patients.MaxCanceledOffers = currentPatient.CanceledOffers
		}

		if currentPatient.AverageReplyTime > patients.MaxReplyTime {
			patients.MaxReplyTime = currentPatient.AverageReplyTime
		}
	}
	patients.MaxBehaviorIndex = patients.MaxAcceptedOffers + patients.MaxCanceledOffers
}

// Preprocess the Patient priority with existing data
func (patients *ManagePatients) preProcessPatientsPriority() {
	for i := range patients.PatientsList {
		currentPatient := &patients.PatientsList[i]
		var (
			acceptedOffersIndex   float64
			canceledOffersIndex   float64
			averageReplyTimeIndex float64
			ageIndex              float64
		)

		if ((currentPatient.AcceptedOffers + currentPatient.CanceledOffers) / patients.MaxBehaviorIndex) <= percentMinBehavior {
			acceptedOffersIndex = acceptedOffersWeightPercent
			canceledOffersIndex = canceledOffersWeightPercent
			averageReplyTimeIndex = maxReplyTimeWeightPercent
			ageIndex = ageWeightPercent
		} else {
			acceptedOffersIndex = currentPatient.AcceptedOffers / patients.MaxAcceptedOffers * acceptedOffersWeightPercent
			canceledOffersIndex = (1 - (currentPatient.CanceledOffers / patients.MaxCanceledOffers)) * canceledOffersWeightPercent
			averageReplyTimeIndex = (1 - (currentPatient.AverageReplyTime / patients.MaxReplyTime)) * maxReplyTimeWeightPercent
			ageIndex = currentPatient.Age / maxAgePercent

		}
		currentPatient.Priority = ageIndex + acceptedOffersIndex + canceledOffersIndex + averageReplyTimeIndex
	}
}

// GetTopPriorityPatients gets a final list of patients according to the coordinates of the facility
func (patients *ManagePatients) GetTopPriorityPatients(latitude float64, longitude float64, patientRange int) []Patient {
	var orderedPatients []Patient

	if patientRange < 1 {
		patientRange = TopPatientRange
	}

	for i := range patients.PatientsList {
		currentPatient := patients.PatientsList[i]
		distance := distanceCalculation(currentPatient.Location.Latitude, currentPatient.Location.Longitude, latitude, longitude)
		distancePercent := (1 - (distance / earthCircuit)) * distanceWeightPercent

		currentPatient.Priority = currentPatient.Priority + distancePercent
		orderedPatients = append(orderedPatients, currentPatient)
	}
	sort.Sort(patientByPriority(orderedPatients))
	if len(orderedPatients) > patientRange {
		return orderedPatients[:patientRange]
	}
	return orderedPatients
}
