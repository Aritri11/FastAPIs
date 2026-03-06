from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'katwa', 'state': 'west bengal', 'pin': '713130'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Aritri', 'age': 25, 'address': address1}

patient1 = Patient(**patient_dict)

#exclude_unset only allows those fields mentioned in the patient_dict to be exported
temp = patient1.model_dump(exclude_unset=True)

print(temp)
print(type(temp))