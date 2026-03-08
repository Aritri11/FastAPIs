import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

#To create this we need MLFlow typically, but here we are doing it manually
MODEL_VERSION='1.0.0'

#Get class labels from the model
class_labels= model.classes_.tolist()

def predict_output(user_input: dict):

    df=pd.DataFrame([user_input])

    #extract the predicted class
    predicted_class=model.predict(df)[0]

    #get probabilities for all classes
    probabilities=model.predict_proba(df)[0]
    confidence=max(probabilities)

    #craete mapping: {class_name: probability}
    class_probs= dict(zip(class_labels,map(lambda p: round(p, 4), probabilities)))

    return {
        'predicted_category': predicted_class,
        'confidence': round(confidence,4),
        'class_probs': class_probs
    }
