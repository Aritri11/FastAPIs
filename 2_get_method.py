from fastapi import FastAPI
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

@app.get("/view")
def view():
    data = load_data()
    return data