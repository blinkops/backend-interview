package blink

import (
	"reflect"
	"testing"
)

func TestLoc_Distance(t *testing.T) {
	tests := []struct {
		name   string
		l1, l2 Loc
		want   float64
	}{
		{
			name: "zero",
			l1:   Loc{},
			l2:   Loc{},
			want: 0,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.l1.Distance(tt.l2); got != tt.want {
				t.Errorf("Loc.Distance() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestDuration_MarshalJSON(t *testing.T) {
	tests := []struct {
		name    string
		d       Duration
		want    []byte
		wantErr bool
	}{
		{
			name:    "zero",
			d:       Duration{},
			want:    []byte("0"),
			wantErr: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := tt.d.MarshalJSON()
			if (err != nil) != tt.wantErr {
				t.Errorf("Duration.MarshalJSON() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Duration.MarshalJSON() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestDuration_UnmarshalJSON(t *testing.T) {
	tests := []struct {
		name       string
		serialized []byte
		want       Duration
		wantErr    bool
	}{
		{
			name:       "zero",
			serialized: []byte("0"),
			want:       Duration{},
			wantErr:    false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var got Duration
			err := got.UnmarshalJSON(tt.serialized)
			if (err != nil) != tt.wantErr {
				t.Errorf("Duration.UnmarshalJSON() error = %v, wantErr %v", err, tt.wantErr)
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("Duration.UnmarshalJSON() = %v, want %v", got, tt.want)
			}
		})
	}
}
