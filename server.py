from typing import Optional
from fastapi import FastAPI, HTTPException

from default_values import FIELD_TO_MAX_SCORE, NUMBER_OF_PATIENTS_TO_RETURN
from location import parse_location
from main import patients_objects_list
from final_score import set_score, get_top_list


app = FastAPI()


@app.get("/patients",  status_code=200)
def read_root(location: Optional[str] = None):
    """
    Return the best 10 patients according to the location
    :param location: <latitude>,<longitude>
    """
    try:
        location_obj = parse_location(location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    set_score(patients_objects_list, location_obj, FIELD_TO_MAX_SCORE["location"])

    return {"data": get_top_list(patients_objects_list, NUMBER_OF_PATIENTS_TO_RETURN)}


