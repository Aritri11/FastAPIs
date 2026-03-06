#Data validation by using Pydantic makes it simpler yet powerful & useful through the class structure
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Ranit', 'Amit'])] #Field & Annotated together is used to attach metadata for better understanding the usage of the pydantic object later
    email: EmailStr #validation that the format should be strictly email
    linkedin_url: AnyUrl #format has to be URL only
    age: int = Field(gt=0, lt=120) #Field sets up custom data validation according to your use case
    weight: Annotated[float, Field(gt=0, strict=True)] #Strict is used to prevent automatic type coercion which can sometimes inherently be done by pydantic
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)] #Optional can be used when u want something to be not absolutely required everytime
    contact_details: Dict[str, str]

#dummy function with similar logic to database
def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'Aritri', 'email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com/1322', 'age': '25', 'weight': 60.2,'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)