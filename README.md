# Blink Task - Patients List

## Installation

Create virtual environment - open the project folder and execute:
```shell
python3 -m venv venv
```

Install the project's dependencies:
```shell
pip3 install -r requirements.txt
```

## Usage

Start the service:
```shell
flask run
```

## Testing

Run the tests:
```shell
python3 -m unittest
```

You can run tests with more detail (higher verbosity) by passing in the -v flag:
```shell
python3 -m unittest -v 
```

## Implementations Details

### General information

Each category has a maximum value that grants the maximum score for the category (specified in constants.py).
The scores will increase / decrease linearly between 0 and the max value.
Any number above the specified max will grant the patient the maximum score for this category.
For example: Age 0 grants 0 score. Age 80 grants the max score (AGE_WEIGHT). Age 150 also grants the max score.
0 reply time will grant max score. 1200 seconds reply time will grant 0 score. 3500 reply time will also grant 0 score.

### Patients with missing / erroneous attributes

If a patient has missing / erroneous attributes (this also answers to little behavioral data), he will be given a random score for the missing / erroneous category between 0 and MAX_CATEGORY_WEIGHT.
This way, patients with little / no behavioral data will be given a chance to be selected.
This also handles errors, because if a patient has erroneous data, he can still be selected.
For example: If a patient has no age / age is not an integer ('82a') he will get a random age score.

### Performance

In order to optimize the app's performance, the patients list is preproccessed and each patient is given a score (without taking distance into account). On each request, only the distance score needs to be calculated.
The patients list still has to be sorted in each request, meaning it still runs in O(nlogn).
* Note: If the data was stored in a database, I would have created a trigger that calculates the score without distance on insert/update. The current solution doesn't handle changes in the patients list.

## Error Handling

Any exception or error in proccessing a patient's data does not cause the app to stop.
To make sure that all of the patients have a chance to be selected, even patients with erroneous data will get a random score and the app will continue running normally.
The app does not log errors - this could be a future improvement.