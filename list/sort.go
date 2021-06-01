package list

import (
	. "github.com/Haramaty/blink-backend-interview"

	"sort"
    "math/rand"
)

const (
    UNKNOWN_RATIO = 0.25
    SCORE_FACTOR = 3
)

func (p *PatientList) SortedIndex(facility Loc) Index {
	index := newIndex(p, facility)
	sort.Stable(sort.Reverse(&index))
	return index
}

// A sorted index of a patient list
// Besides the sorted patient list, the index also saves score calculations
type Index struct {
	list    *PatientList
	scores  []int
	indices []int
}

func newIndex(list *PatientList, facility Loc) Index {
	var (
		scores      = make([]int, len(list.patients))
		indices     = make([]int, len(list.patients))
		maxDistance float64
	)

	for i := range list.patients {
		if distance := list.patients[i].Loc.Distance(facility); distance > maxDistance {
			maxDistance = distance
		}
	}

	for i := range list.patients {
		scores[i] = finalScore(list.partialScores[i], list.patients[i].Loc.Distance(facility), maxDistance)
        if float64(list.patients[i].Accepted) < UNKNOWN_RATIO * float64(list.max.Accepted) {
            scores[i] += int(SCORE_FACTOR * rand.Float64())
        }
		indices[i] = i
	}

	return Index{list, scores, indices}
}

func (m *Index) Patients() []*Patient {
	patients := make([]*Patient, len(m.scores))

	for i := range patients {
		patients[i] = &m.list.patients[m.indices[i]]
	}

	return patients
}

func (m *Index) Scores() []int {
    return m.scores
}

func (m *Index) Len() int {
	return len(m.scores)
}

func (m *Index) Less(i, j int) bool {
	return m.scores[i] < m.scores[j]
}

func (m *Index) Swap(i, j int) {
	m.scores[i], m.scores[j] = m.scores[j], m.scores[i]
	m.indices[i], m.indices[j] = m.indices[j], m.indices[i]
}
