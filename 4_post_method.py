from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated, Literal

app=FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient',examples=['P001'])]
    name: Annotated[str, Field(..., title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Ranit', 'Amit'])] #Field & Annotated together is used to attach metadata for better understanding the usage of the pydantic object later
    city: Annotated[str, Field(..., description='City of the patient')]
    age: int = Field(gt=0, lt=120) #Field sets up custom data validation according to your use case
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(...,gt=0,description='Height of the patient in meters')]
    weight: Annotated[float, Field(...,gt=0, description='Weight of the patient in kg')] #Strict is used to prevent automatic type coercion which can sometimes inherently be done by pydantic


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return 'underweight'
        elif self.bmi <25:
            return 'normal'
        elif self.bmi <30:
            return 'normal'
        else:
            return 'obese'

def load_data():
    with open("patient_data.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patient_data.json", "w") as f:
        json.dump(data, f)

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

#to create a new patient
@app.post('/create')
def create_patient(patient: Patient):
    #load existing data
    data = load_data()

    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    #new patient then add to database
    data[patient.id] = patient.model_dump(exclude=['id']) #model_dump used because a pydantic object(patient) has to be added to a dictionary (data)

    #save into the json
    save_data(data)

    return JSONResponse(status_code=201,content={"message":"Patient created successfully"})
