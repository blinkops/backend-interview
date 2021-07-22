package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	httpSwagger "github.com/swaggo/http-swagger"
	_ "backend-interview/docs"
	"backend-interview/patients"
	"log"
	"net/http"
	"regexp"
	"strconv"
	"strings"
)

// @title Blink backend interview REST API
// @version 0.0.1
// @description This is a very simple project to ordering a list of patients according to certain criteria
// @termsOfService http://swagger.io/terms/
// @contact.name Atanas Mavrov
// @license.name GPL3
// @license.url https://www.gnu.org/licenses/gpl-3.0.html
// @host localhost:8000

// Response is a helper structure for API responses without patient data
type Response struct {
	Response string
}

var managePatients = patients.NewManagePatients(true)
var helpResponse = "Please use http://localhost:8000/patients?location=latitude,longitude;" +
	" Example: http://localhost:8000/patients?location=32.109333,34.855499"

func main() {
	app := mux.NewRouter()
	app.PathPrefix("/docs/").Handler(httpSwagger.Handler(
		httpSwagger.URL("http://localhost:8000/docs/doc.json"), //The url pointing to API definition
		httpSwagger.DeepLinking(true),
		httpSwagger.DocExpansion("none"),
		httpSwagger.DomID("#swagger-ui"),
	))
	app.HandleFunc("/", getDefaultHandler)
	app.HandleFunc("/patients", getPatients).Methods("get")

	log.Println("Listening 8000")
	log.Fatal(http.ListenAndServe(":8000", app))
}

// GetOrders godoc
// @Summary Get root URL
// @Description Return help data
// @Tags /
// @Accept  plain
// @Produce  json
// @Success 200
// @Router / [get]
func getDefaultHandler(response http.ResponseWriter, request *http.Request) {
	setResponse(response, http.StatusOK, Response{Response: helpResponse})
}

// GetOrders godoc
// @Summary Top rated patients
// @Description Get the patients with the highest rating by geographical coordinates
// @Tags /patients
// @Accept plain
// @Produce  json
// @Param location query string true "latitude,longitude" default(32.109333,34.855499)
// @Success 200 {array} patients.Patient
// @Router /patients [get]
func getPatients(response http.ResponseWriter, request *http.Request) {

	location := request.URL.Query().Get("location")
	if location == "" {
		setResponse(response, http.StatusBadRequest,
			Response{
				Response: fmt.Sprintf("The coordinates cannot be found in the correct format. %s", helpResponse),
			})
		return
	}
	match, _ :=
		regexp.MatchString(
			"^(-?([0-8]?[0-9](.\\d+)?|90(.[0]+)?)\\s?[,]\\s?)+(-?([1]?[0-7]?[0-9](.\\d+)?|180((.[0]+)?)))$",
			location)

	if ! match {
		setResponse(response, http.StatusBadRequest,
			Response{
				Response: fmt.Sprintf("The coordinates cannot be processed correctly. %s", helpResponse),
			})
		return
	}
	splitLocations := strings.Split(location, ",")
	var lat, lng float64
	if s, err := strconv.ParseFloat(splitLocations[0], 64); err == nil {
		lat = s
	} else {
		setResponse(response, http.StatusBadRequest,
			Response{
				Response: fmt.Sprintf("The latitude coordinate cannot be processed correctly. %s", helpResponse),
			})
		return
	}
	if s, err := strconv.ParseFloat(splitLocations[1], 64); err == nil {
		lng = s
	} else {
		setResponse(response, http.StatusBadRequest,
			Response{
				Response: fmt.Sprintf("The longitude coordinate cannot be processed correctly. %s", helpResponse),
			})
		return
	}

	returnData := managePatients.GetTopPriorityPatients(lat, lng, patients.TopPatientRange)
	setResponse(response, http.StatusOK, returnData)
}

func setResponse(response http.ResponseWriter, responseStatus int, dataForConvert interface{}) {
	jsonResponse, jsonError := json.Marshal(dataForConvert)
	var responseData []byte

	if jsonError != nil {
		response.Header().Set("Content-Type", "text/plain")
		response.WriteHeader(http.StatusInternalServerError)
		responseData = []byte(fmt.Sprintf("The response cannot be processed correctrly. %s", helpResponse))
	} else {
		response.Header().Set("Content-Type", "application/json")
		response.WriteHeader(responseStatus)
		responseData = jsonResponse
	}

	if _, err := response.Write(responseData); err != nil {
		log.Println("Cannot process the response: ", err)
	}
}
