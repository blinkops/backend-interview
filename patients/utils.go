package patients

import (
	"encoding/json"
	"log"
	"math"
	"os"
)

func loadPatientListFromFile(patientFilePath string) []Patient {
	if patientFilePath != "" {
		if _, err := os.Stat(patientFilePath); err == nil {
			patientFileHandler, err := os.Open(patientFilePath)

			defer func() {
				fileCloseError := patientFileHandler.Close()
				if err == nil {
					err = fileCloseError
				}
			}()

			if err != nil {
				log.Println("Cannot open file {file} due to {err}", "file", patientFilePath, "err", err)

				return []Patient{}
			}
			var patients []Patient
			if err = json.NewDecoder(patientFileHandler).Decode(&patients); err != nil {
				log.Println("Cannot parse file {file} due to JSONDecodeError {err}", patientFilePath, err)
				return []Patient{}
			}
			return patients
		}
	}
	return []Patient{}
}

func distanceCalculation(lat1 float64, lng1 float64, lat2 float64, lng2 float64) float64 {
	radLat := (lat2 - lat1) * degreesToRadians
	radLong := (lng2 - lng1) * degreesToRadians
	radLag1 := lat1 * degreesToRadians
	radLag2 := lat2 * degreesToRadians
	a := math.Pow(math.Sin(radLat/2), 2) + math.Pow(math.Sin(radLong/2), 2)*math.Cos(radLag1)*math.Cos(radLag2)
	c := 2 * math.Asin(math.Sqrt(a))
	return earthRadius * c
}

// Functions for ordering patients by their priority
func (patient patientByPriority) Len() int           { return len(patient) }
func (patient patientByPriority) Less(i, j int) bool { return patient[i].Priority > patient[j].Priority }
func (patient patientByPriority) Swap(i, j int)      { patient[i], patient[j] = patient[j], patient[i] }
