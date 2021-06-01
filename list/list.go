package list

import (
	. "github.com/Haramaty/blink-backend-interview"

	"math"
)

type PatientList struct {
	patients []Patient
	max      Patient
	// Incomplete score, not taking distance into account
	partialScores []float64
}

func NewList(patients []Patient) PatientList {
	var (
		max           = computeMax(patients)
		partialScores = make([]float64, len(patients))
	)

	for i := range patients {
		partialScores[i] = partialScore(&patients[i], &max)
	}

	return PatientList{patients, max, partialScores}
}

func computeMax(patients []Patient) (max Patient) {
	for i := range patients {
		p := &patients[i]

		if age := p.Age; age > max.Age {
			max.Age = age
		}

		if accepted := p.Accepted; accepted > max.Accepted {
			max.Accepted = accepted
		}

		if canceled := p.Canceled; canceled > max.Canceled {
			max.Canceled = canceled
		}

		if avgReplyTime := p.AvgReplyTime; avgReplyTime.Seconds() > max.AvgReplyTime.Seconds() {
			max.AvgReplyTime = avgReplyTime
		}
	}

	return max
}

func partialScore(p *Patient, max *Patient) float64 {
	var (
		age          = float64(p.Age) / float64(max.Age)
		accepted     = float64(p.Accepted) / float64(max.Accepted)
		canceled     = (1 - float64(p.Canceled)/float64(max.Canceled))
		avgReplyTime = (1 - float64(p.AvgReplyTime.Seconds())/float64(max.AvgReplyTime.Seconds()))
	)

	partial := 1*age + 3*accepted + 3*canceled + 2*avgReplyTime
	return partial
}

func finalScore(partial, distance, max float64) int {
	distance = (1 - distance/max)
	return int(math.RoundToEven(partial + 1*distance))
}
