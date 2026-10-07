from fastapi import FastAPI,Path,HTTPException,Query
import json
from pathlib import Path as FilePath

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "This is patient management website"}


@app.get("/view")
def view():
    return load_data()

@app.get("/about")
def mess():
    return { "FastApi websites"}

def load_data():
    data_path = FilePath(__file__).with_name("patients.json")
    with data_path.open("r", encoding="utf-8") as file:
        return json.load(file)


    

@app.get("/patient/{patient_id}")
def load_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the DB",
        examples=["P001"]
    )
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404,detail="Patient not found") 

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(
        ...,
        description='Sort based on height, weight or bmi'
    ),
    order: str = Query('asc', description='Sort in asc or desc order')
):
    data = load_data()
    patients = list(data.values())

    valid_sort_fields = {'height', 'weight', 'bmi'}
    sort_field = sort_by.lower()
    sort_order = order.lower()

    if sort_field not in valid_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if sort_order not in {'asc', 'desc'}:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")

    sorted_patients = sorted(
        patients,
        key=lambda patient: patient.get(sort_field, 0),
        reverse=(sort_order == 'desc')
    )
 
    return sorted_patients

    valid_fields = ['height']