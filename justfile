build:
  @go build ./...

test +modules="./...":
  @go test {{ modules }}

run:
  @go run ./cmd/blink

patients lat long:
  curl -i http://localhost:8080/patients?location={{lat}},{{long}}
