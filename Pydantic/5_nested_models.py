from pydantic import BaseModel

#definig a field as a pydantic object and then using it inside another pydantic model as a field
class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'katwa', 'state': 'west bengal', 'pin': '713130'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Aritri', 'gender': 'female', 'age': 25, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(include=['name'])
print(temp)
print(type(temp))


#Benifits:
# Better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use Vitals in multiple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically—no extra work needed