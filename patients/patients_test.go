package patients

import (
	"github.com/google/uuid"
	"testing"
)

var patientData = Patient{
	ID:               uuid.UUID{},
	Name:             "Patient Name",
	AcceptedOffers:   123,
	CanceledOffers:   123,
	AverageReplyTime: 123,
	Age:              50,
	Location:         location{32.109333, 34.855499},
	Priority:         0,
}

func TestPreProcessPatients(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.AcceptedOffers = 500
	patient1.AverageReplyTime = 3000

	patient2.CanceledOffers = 1000

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()

	if managePatients.MaxAcceptedOffers != 500 {
		t.Errorf("MaxAcceptedOffers is incorrectly calculated. Must be %f, %f received",
			patient1.AcceptedOffers, managePatients.MaxAcceptedOffers)
	}

	if managePatients.MaxCanceledOffers != 1000 {
		t.Errorf("MaxCanceledOffers is incorrectly calculated. Must be %f, %f received",
			patient2.CanceledOffers, managePatients.MaxCanceledOffers)
	}

	if managePatients.MaxReplyTime != 3000 {
		t.Errorf("MaxReplyTime is incorrectly calculated. Must be %f, %f received",
			patient1.AverageReplyTime, managePatients.MaxReplyTime)
	}

	if managePatients.MaxBehaviorIndex != 1500 {
		t.Errorf("MaxBehaviorIndex is incorrectly calculated. Must be %f, %f received",
			1500.0, managePatients.MaxReplyTime)
	}
}

func TestPreProcessPatientsPriority(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.Name = "Patient 1"
	patient1.Age = 30

	patient2.Name = "Patient 2"
	patient2.Age = 60

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()
	managePatients.preProcessPatientsPriority()

	if managePatients.PatientsList[0].Priority != 32 {
		t.Errorf("Patient priority is incorrectly calculated.")
	}

	if managePatients.PatientsList[1].Priority != 34 {
		t.Errorf("Patient priority is incorrectly calculated.")
	}
}

func TestGetTopPriorityPatientsDifferentAge(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.Name = "Patient 1"
	patient1.Age = 30

	patient2.Name = "Patient 2"
	patient2.Age = 60

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()
	managePatients.preProcessPatientsPriority()
	orderedList := managePatients.GetTopPriorityPatients(32.109333, 34.855499, 10)

	if orderedList[0].Name != patient2.Name {
		t.Errorf("Patient priority by age is incorrectly calculated.")
	}
	if orderedList[1].Name != patient1.Name {
		t.Errorf("Patient priority by age is incorrectly calculated.")
	}
}

func TestGetTopPriorityPatientsDifferentAcceptedOffers(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.Name = "Patient 1"
	patient1.AcceptedOffers = 100

	patient2.AcceptedOffers = 10
	patient2.Name = "Patient 2"

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()
	managePatients.preProcessPatientsPriority()
	orderedList := managePatients.GetTopPriorityPatients(32.109333, 34.855499, 10)

	if orderedList[0].Name != patient1.Name {
		t.Errorf("Patient priority by accepted offers is incorrectly calculated.")
	}
	if orderedList[1].Name != patient2.Name {
		t.Errorf("Patient priority by accepted offers is incorrectly calculated.")
	}
}

func TestGetTopPriorityPatientsDifferentCanceledOffers(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.Name = "Patient 1"
	patient1.CanceledOffers = 100

	patient2.Name = "Patient 2"
	patient2.CanceledOffers = 10

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()
	managePatients.preProcessPatientsPriority()
	orderedList := managePatients.GetTopPriorityPatients(32.109333, 34.855499, 10)

	if orderedList[0].Name != patient2.Name {
		t.Errorf("Patient priority by canceled offers is incorrectly calculated.")
	}
	if orderedList[1].Name != patient1.Name {
		t.Errorf("Patient priority by canceled offers is incorrectly calculated.")
	}
}

func TestGetTopPriorityPatientsLittleBehaviorData(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.Name = "Patient 1"
	patient1.AcceptedOffers = 1000
	patient1.CanceledOffers = 1000

	patient2.Name = "Patient 2"
	patient2.AcceptedOffers = 1
	patient2.CanceledOffers = 1

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()
	managePatients.preProcessPatientsPriority()
	orderedList := managePatients.GetTopPriorityPatients(32.109333, 34.855499, 10)

	if orderedList[0].Name != patient2.Name {
		t.Errorf("Patient priority by little behavior data is incorrectly calculated.")
	}
	if orderedList[1].Name != patient1.Name {
		t.Errorf("Patient priority by little behavior data is incorrectly calculated.")
	}
}

func TestGetTopPriorityPatientsDifferentLocations(t *testing.T) {
	patient1 := patientData
	patient2 := patientData

	patient1.Name = "Patient 1"
	patient1.Location.Latitude = 32.078651
	patient1.Location.Longitude = 34.778852

	patient2.Name = "Patient 2"
	patient2.Location.Latitude = 32.323354
	patient2.Location.Longitude = 34.856745

	managePatients := NewManagePatients(false)
	managePatients.PatientsList = append(managePatients.PatientsList, patient1)
	managePatients.PatientsList = append(managePatients.PatientsList, patient2)
	managePatients.preProcessPatients()
	managePatients.preProcessPatientsPriority()
	orderedList := managePatients.GetTopPriorityPatients(32.109333, 34.855499, 10)

	if orderedList[0].Name != patient1.Name {
		t.Errorf("Patient priority by location is incorrectly calculated.")
	}
	if orderedList[1].Name != patient2.Name {
		t.Errorf("Patient priority by location is incorrectly calculated.")
	}
}
