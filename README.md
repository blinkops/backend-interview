# Blink-backend-interview

## Project setup
Python - 3.10.0
```
pip install -r requirements.txt
```

### Run server
```
uvicorn server:app
```

### Test
```
python -m unittest
```

## Routes
* /patients?location='latitude,longitude' -> methods = [GET], GET: Return the best 10 patients according to the location  
* /docs -> Docs of the API


## Explanation of my algorithm
By sorting the list of patients against the patient.get(field) I can know
for each patient how good is he/she in that field in ratio to other patients. 
Let's look at an example, say we sort by age and my patients 
= [p1: age=20, p2: age=30, p3: age=40] p3 will get the best score, followed by p2, etc...

The sorting method creates a good balance between different metrics that we measured.
However, it does not provide good differentiation when there are large differences 
between different patients. For example, if patients 
= [p1: age=20, p2: age=21, p3: age=22, p4: age=50]. The grade for p3 and p4 will be
very similar, although the age difference is very large.
