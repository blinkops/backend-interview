package patients

import (
	"github.com/google/uuid"
)

// Patient represent single patient structure
type Patient struct {
	ID               uuid.UUID `json:"id"`
	Name             string    `json:"name"`
	Age              float64   `json:"age"`
	AcceptedOffers   float64   `json:"acceptedOffers"`
	CanceledOffers   float64   `json:"canceledOffers"`
	AverageReplyTime float64   `json:"averageReplyTime"`
	Location         location  `json:"location"`
	Priority         float64
}

// Patient location structure
type location struct {
	Latitude  float64 `json:"latitude,string"`
	Longitude float64 `json:"longitude,string"`
}

// ManagePatients contains the object properties
type ManagePatients struct {
	PatientsList      []Patient
	MaxAcceptedOffers float64
	MaxCanceledOffers float64
	MaxReplyTime      float64
	MaxBehaviorIndex  float64
}

type patientByPriority []Patient
