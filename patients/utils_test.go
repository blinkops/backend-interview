package patients

import (
	"fmt"
	"testing"
)

func TestLoadPatientListFromFile(t *testing.T)  {
	// Get data from origin file
	if len(loadPatientListFromFile("../" + filePath)) != 1000 {
		t.Errorf("Load JSON data from file failed")
	}

	// Get data from incorrect JSON file
	if len(loadPatientListFromFile("../sample-data/incorrect_patient_json_data_for_test_purpose.json")) != 0 {
		t.Errorf("Load JSON data from file failed")
	}

	// Get data from non-existent file
	if len(loadPatientListFromFile("not-existent-file.json")) != 0 {
		t.Errorf("Load JSON data from not existent file failed")
	}
}


func TestDistanceCalculation(t *testing.T) {
	lat1 := 32.109333
	lng1 := 34.855499
	lat2 := 43.21667
	lng2 := 27.91667

	if fmt.Sprintf("%.2f", distanceCalculation(lat1, lng1, lat2, lng2)) != "1376.61" {
		t.Errorf("Distance calculation error")
	}
}
