from flask import Flask
from flask import request
import json
from utils import calculate_patients_score, calculate_patients_score_without_distance

with open('patients.json') as f:
    patients = json.load(f)
    calculate_patients_score_without_distance(patients)  #preproccess patients scores excluding distance 

app = Flask(__name__)

@app.route('/')
def index():
    return {"Message": "Please use the patients path /patients/?location=latitude,longitude to get the top 10 patients"}

@app.route('/patients')
def get_patients():
    try:
        location = request.args.get('location')
        if location is None:
            raise Exception({"Message": f"No coordinates were passed in the query string. "
            f"For example, you can try:    {request.base_url}?location=-77.5235,175.3549"})
        location = location.split(',')
        if len(location) != 2:
            raise Exception({"Message": f"The coordinates weren't passed in the correct format. "
            f"For example, you can try:    {request.base_url}?location=-77.5235,175.3549"})
        try:
            lat = float(location[0])
            lon = float(location[1])
        except:
            raise Exception({"Message": f"The coordinates weren't passed in the correct format. "
            f"For example, you can try:    {request.base_url}?location=-77.5235,175.3549"})
        calculate_patients_score(patients, lat, lon)
        patients.sort(key = lambda patient: patient['totalScore'], reverse = True)
        return json.dumps(patients[:10])
    except Exception as e:
        return str(e), 400


if __name__ == "__main__":
    app.run()

