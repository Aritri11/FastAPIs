from fastapi import FastAPI, Path, HTTPException, Query
import json
app=FastAPI()

def load_data():
    with open("patient_data.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def get_about():
    return {"message":"A fully functional API to manage your patient records"}

#gives all the patient info at once
@app.get("/view")
def view():
    data = load_data()
    return data

#to get only a particular patient info
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str= Path(..., description="ID of the patient in the DB", example='P001')): #Path gives proper description and example for the client to know what to give as input
    #load all patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found") #proper handling of errors with standard error code and message

#endpoint to implement sorting
@app.get("/sort")
def sort_patients(sort_by: str= Query(..., description="Sort on basis of height, weight or BMI"), order: str=Query('asc', description="ascending or descending order", example='asc')):
    data = load_data()
    valid_fields=["height","weight","BMI"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_fields}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Select between asc or desc")

    sort_order=True if order=='desc' else False

    sorted_data= sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return sorted_data