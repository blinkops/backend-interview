import logging

from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse

from patients.patients import Patients

patients = Patients()
app = FastAPI(
    title="Blink backend interview REST API",
    description="This is a very simple project to ordering a list of patients according to certain criteria",
    version="0.0.1"
)


@app.get("/")
def read_root(request: Request):
    return {"INFO": f"Please, use {request.base_url}patients?location=latitude,longitude"}


@app.get("/patients")
def read_item(request: Request, location: str = Query(
        ...,
        title='Ordering list endpoint',
        description='Use this endpoint to get ordered patient list',
        example='32.109333,34.855499',
        min_length=5,
        regex="^(-?([0-8]?[0-9](.\\d+)?|90(.[0]+)?)\\s?[,]\\s?)+(-?([1]?[0-7]?[0-9](.\\d+)?|180((.[0]+)?)))$")):
    location_split = location.split(',')
    if len(location_split) != 2:
        raise HTTPException(status_code=400,
                            detail=f"The coordinates cannot be found in the correct format. "
                                   f"Please use {request.base_url}patients?location=latitude,longitude; "
                                   f"Example: {request.base_url}patients?location=32.109333,34.855499")

    try:
        lat = float(location_split[0])
        lng = float(location_split[1])
    except ValueError:
        raise HTTPException(status_code=400,
                            detail=f"The coordinates cannot be processed correctly."
                                   f"Please use {request.base_url}patients?location=latitude,longitude; "
                                   f"Example: {request.base_url}patients?location=32.109333,34.855499")

    try:
        return JSONResponse(content=patients.get_top_priority_patients(lat, lng))
    except Exception as e:
        logging.warning(f'An error occurs when receiving patients with the highest priority: {e}')
        raise HTTPException(status_code=500,
                            detail="A system error has occurred. "
                                   "If you continue to see this message, please contact us")
