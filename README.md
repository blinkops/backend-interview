# Blink backend interview

* [Installation](#installation)
  * [Requirements](#requirements)
  * [Environment](#environment)
  * [Packages](#packages)
* [Run the project](#run-the-project)
* [API](#api)
	* [API documentation](#api-documentation)
	* [API requests](#api-requests)
* [Projects errors handling](#projects-errors-handling)
* [Coding style](#coding-style)
* [Running tests](#running-tests)


## Installation

### Requirements

The project works with Go 1.4 or higher version 

### Environment

If you don't use the default GoLang directory you must set the `GOPATH` environment variable
```shell script
export GOPATH=/PATH_TO_GO_LANG_DIRECOTRY
```

### Packages

You can install required packages by the following command
```shell script
go get
```

## Run the project

**Start the web services:**
```shell
  go run main.go
```

## API

### API documentation

You can view the API documentation and do test by opening the browser and loading the local project URL - http://localhost:8000/docs/index.html 

### API requests

You can use the REST API by opening local project URL in the following format - http://localhost:8000/patients?location=latitude,longitude

## Projects errors handling

Exceptions during the processing of the file with patients do not stop the application.\
If a general error occurs with the patients data file, the list of patients will be empty, but the application will continue to work.\
All errors included in the GoLang logging system.\
For this project, errors displayed in the console, no file configured to save them. 


## Coding style

The project follows the [Go Lang Effective](https://golang.org/doc/effective_go) recommendations.

**Test the coding style**

```shell
  docker run --rm -v $(pwd):/app -w /app golangci/golangci-lint:v1.41.1 golangci-lint run -v
```

> You can also use an older tool such as a golint

**Download and test with golint**

```shell script
go get -u golang.org/x/lint/golint
golint partners
golint main.go
```

## Running tests

You can run tests with the following command:

```shell
  go test ./patients/ -v
```