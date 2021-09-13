# Blink Backend Interview
## Installation

Install the required packages:

```pip install -r requirements.txt```

## Running the project

First, run the ```patients_api.py``` file, either through the command prompt or your IDE. If you're working with the command prompt, open it and navigate to the project folder, then execute the following command:

```python patients_api.py```

Now that the server is running, run the ```api_call.py``` file, either through the command prompt or your IDE. If you're working with the command prompt, open it and navigate to the project folder, then execute the following command:

```python api_call.py```

The aforementioned file will prompt you to enter a location, in the following format: ```latitude,longitude```. Once the location is entered, a GET request will be sent to the API with the given location and the result will be printed.

## Running the tests

First, run the ```patients_api.py``` file, either through the command prompt or your IDE. If you're working with the command prompt, open it and navigate to the project folder, then execute the following command:

```python patients_api.py```

Now that the server is running, run the ```test_patients_logic.py``` file, either through the command prompt or your IDE. If you're working with the command prompt, open it and navigate to the project folder, then execute the following command:

```python test_patients_logic.py```

All the tests will then run automatically and you'll be able to see whether any of them failed.

## Error handling

If an error occurs due to invalid data, an exception will be raised and the program will stop running. The API will return a response with a 404 status code, containing a detailed description of the error.