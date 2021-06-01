package main

import (
	. "github.com/Haramaty/blink-backend-interview"
	. "github.com/Haramaty/blink-backend-interview/conv"
	. "github.com/Haramaty/blink-backend-interview/list"

	"encoding/json"
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
)

const PATH = "sample-data/patients.json"

func main() {
	file, err := os.Open(PATH)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var (
		patients []Patient
		decoder  = json.NewDecoder(file)
	)
	err = decoder.Decode(&patients)
	if err != nil {
		panic(err)
	}

	var (
		service = Service{NewList(patients)}
		server  = gin.Default()
	)

	server.GET("/patients", service.PatientList)
	server.Run(":8080")
}

type Service struct {
	patients PatientList
}

func (s *Service) PatientList(c *gin.Context) {
	loc, err := ParseLoc(c.Query("location"))
	if err != nil {
		c.AbortWithError(http.StatusBadRequest, err)
		return
	}

	var (
		index    = s.patients.SortedIndex(loc)
		patients = index.Patients()[:10]
		scores   = index.Scores()[:10]
	)
	// names := make([]string, len(patients))
	// for i, p := range patients {
	// 	names[i] = p.Name
	// }
	data := make([]struct {
		Name  string
		Score int
	}, len(patients))
	for i, p := range patients {
		data[i] = struct {
			Name  string
			Score int
		}{Name: p.Name, Score: scores[i]}
	}
	c.JSON(http.StatusOK, data)
}
