package conv

import (
	"reflect"
	"testing"

	. "github.com/Haramaty/blink-backend-interview"
)

func TestParseLoc(t *testing.T) {
	tests := []struct {
		name    string
		s       string
		want    Loc
		wantErr bool
	}{
		{
			name:    "zero",
			s:       "0,0",
			want:    Loc{},
			wantErr: false,
		}, {
			name:    "empty",
			s:       "",
			want:    Loc{}, // doesn't matter
			wantErr: true,
		}, {
			name:    "simple",
			s:       "5,22",
			want:    Loc{5, 22},
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseLoc(tt.s)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParseLoc() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("ParseLoc() = %v, want %v", got, tt.want)
			}
		})
	}
}
