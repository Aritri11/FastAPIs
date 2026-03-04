from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.get("/about")
def get_about():
    return {"message":"I am a Student"}