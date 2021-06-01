package blink

import (
	"encoding/json"
	"math"
	"time"
)

// A Patient, with any demographic and behavioural information about them
type Patient struct {
	Id           string   `json:"id"`
	Name         string   `json:"name"`
	Age          uint     `json:"age"`
	Loc          Loc      `json:"location"`
	Accepted     uint     `json:"acceptedOffers"`
	Canceled     uint     `json:"canceledOffers"`
	AvgReplyTime Duration `json:"averageReplyTime"`
}

// Patient location
type Loc struct {
	Lat  float64 `json:"latitude,string"`
	Long float64 `jdon:"longitude,string"`
}

func (l Loc) Distance(o Loc) float64 {
	return math.Sqrt(math.Pow(l.Lat-o.Lat, 2) + math.Pow(l.Long-o.Long, 2))
}

// A wrapper around time.Duration represented as (whole) seconds in JSON
type Duration struct {
	time.Duration
}

func (d Duration) MarshalJSON() ([]byte, error) {
	return json.Marshal(int(math.RoundToEven(d.Seconds())))
}

func (d *Duration) UnmarshalJSON(b []byte) error {
	var n int
	err := json.Unmarshal(b, &n)
	if err != nil {
		return err
	}

	d.Duration = time.Duration(n)
	return nil
}
