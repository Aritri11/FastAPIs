from fastapi import FastAPI
from model.predict import predict_output, model, MODEL_VERSION
from fastapi.responses import JSONResponse
from user_input import UserInput
from model.predict import model
from prediction_response import PredictionResponse


app = FastAPI()

#human readable
@app.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}

#When trying to deploy on AWS , this parameter check is mandatory (this is machine readable)
@app.get('/health')
def health_check():
    return {
        'status': 'Ok',
        'version': '1.0.0',
        'model_loaded': model is True
    }

#connecting the ML model with a FastAPI end point (post method is used in 2 cases- to create new entries and also to call output from ML/DL models)
@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input =({
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    })

    try:

        prediction=predict_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})

    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})