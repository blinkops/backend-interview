package conv

import (
	. "github.com/Haramaty/blink-backend-interview"

	"fmt"
	"strconv"
	"strings"
)

// Parse a "latitude,longitutde" string into a location
func ParseLoc(s string) (Loc, error) {
	splitted := strings.Split(s, ",")
	if len(splitted) != 2 {
		return Loc{}, fmt.Errorf("location must be two numbers separated by a comma")
	}

	lat, err := strconv.ParseFloat(splitted[0], 64)
	if err != nil {
		return Loc{}, fmt.Errorf("latitude not a number: %w", err)
	}

	long, err := strconv.ParseFloat(splitted[1], 64)
	if err != nil {
		return Loc{}, fmt.Errorf("longtitude not a number: %w", err)
	}

	return Loc{lat, long}, nil
}
