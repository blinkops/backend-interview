# Blink backend interview

* [Installation](#installation)
  * [Requirements](#Requirements)
  * [Python virtual environment](#python-virtual-environment)
* [Run the project](#run-the-project)
* [API](#api)
	* [API documentation](#api-documentation)
	* [API requests](#api-requests)
* [Projects errors handling](#projects-errors-handling)  
* [Projects errors handling](#projects-errors-handling)
* [Coding style](#coding-style)
* [Running tests](#running-tests)  


## Installation

### Requirements

The project works with Python 3.8 or higher version and pip3 version 21.1.3 or higher 

### Python virtual environment 

**Create a virtual environment**

Open the project folder and then execute:
```shell
  python3 -m venv venv
  source venv/bin/activat
```

**Install the necessary packages**
```shell
  pip3 install -r requirements.txt
```

## Run the project

**Start the web services:**
```shell
  uvicorn main:app --reload
```

## API

### API documentation

You can view the API documentation and do test by opening the browser and loading the local project URL: http://localhost:8000/docs 

### API requests

You can use the REST API by opening local project URL in the following format - http://localhost:8000/patients?location=latitude,longitude

## Projects errors handling

Exceptions during the processing of the file with patients do not stop the application.\
If a general error occurs with the patients data file, the list of patients will be empty, but the application will continue to work.\
If there is an error with missing or wrong data for one patient, the patient will be ignored.\
All errors included in the python logging system.\
For this project, errors displayed in the console, no file configured to save them. 

## Coding style

The project follows the [PEP8](https://www.python.org/dev/peps/pep-0008/) coding standard except the line length.\
The limit of line length for this project is 120 character per line. \

**Test the coding style**

```shell
  flake8 --max-line-length 120 patients/
```

## Running tests

You can run tests with the following command:

```shell
  python -m unittest discover
```