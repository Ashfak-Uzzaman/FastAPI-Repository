# `Pydantic` Library

`Pydantic` is a Python library used for:

* Data validation
* Data parsing
* Type checking
* Automatic data conversion

It mainly works using Python type hints.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

Now if you create:

```python
user = User(name="Ashfak", age="25")
```

Pydantic automatically converts `"25"` (string) into `25` (integer).

So:

```python
print(user.age)
```

Output:

```python
25
```

And type becomes:

```python
int
```

---

## Why Pydantic is useful

Without Pydantic:

```python
data = {
    "name": "Ashfak",
    "age": "25"
}
```

You manually need to check:

* Is `name` really string?
* Is `age` integer?
* Is email valid?
* Is URL valid?
* Is required field missing?

Pydantic does all these automatically.

---

## Main features

1. Validation

```python
from pydantic import BaseModel

class User(BaseModel):
    age: int

User(age="abc")
```

This gives validation error because `"abc"` cannot become integer.

---

2. Automatic conversion

```python
User(age="25")
```

Converts string → integer automatically.

---

3. Useful built-in types

```python
from pydantic import EmailStr, AnyUrl
```

Example:

```python
email: EmailStr
website: AnyUrl
```

These validate email and URL formats automatically.

---

4. Very useful in FastAPI

FastAPI uses Pydantic heavily.

Example:

```python
@app.post("/users")
def create_user(user: User):
    return user
```

When client sends JSON:

```json
{
  "name": "Ashfak",
  "age": "25"
}
```

FastAPI + Pydantic automatically:

* validate data
* convert types
* generate API docs
* return errors if invalid

---

## What is BaseModel?

`BaseModel` is the parent class of all Pydantic models.

```python
class User(BaseModel):
```

This tells Pydantic:

"Validate and manage this class as a data model."

---

## Simple mental model

Pydantic = Smart Python data checker

It:

* checks incoming data
* fixes simple type mismatches
* throws errors for invalid data
* makes APIs safer and cleaner

---

## Example with error

```python
from pydantic import BaseModel

class Student(BaseModel):
    age: int

student = Student(age="hello")
```

Error:

```python
ValidationError
```

Because `"hello"` cannot convert to integer.

---

### An example use of `pydentic` :

```python
# Import BaseModel:
# BaseModel is the main class from Pydantic.
# We inherit from this class to create a data model with validation.
from pydantic import BaseModel, EmailStr, AnyUrl, Field

# Import typing utilities:
# List -> list type
# Dict -> dictionary type
# Optional -> value can be None
# Annotated -> allows adding metadata/validation with Field()
from typing import List, Dict, Optional, Annotated


# Create a Patient model.
# This class will automatically validate incoming data.
class Patient(BaseModel):

    # name field:
    # str -> must be a string
    # Annotated is used to attach Field() validation metadata.
    name: Annotated[
        str,

        # Field() adds extra validation and documentation
        Field(

            # Maximum allowed characters = 50
            max_length=50,

            # Title used in API docs / schema
            title="Name of the patient",

            # Description used in docs
            description="Give the name of the patient in less than 50 chars",

            # Example values shown in docs
            examples=["Nitish", "Amit"],
        ),
    ]

    # email field:
    # EmailStr validates whether input is a valid email.
    email: EmailStr

    # linkedin_url field:
    # AnyUrl validates whether input is a valid URL.
    linkedin_url: AnyUrl

    # age field:
    # int means integer.
    # Field(gt=0, lt=120)
    # gt = greater than
    # lt = less than
    # So age must be between 1 and 119.
    age: int = Field(gt=0, lt=120)

    # weight field:
    # float means decimal number.
    # gt=0 -> must be positive
    # strict=True -> only real float accepted.
    # Example:
    # 75.2 ✔
    # "75.2" ✘
    weight: Annotated[float, Field(gt=0, strict=True)]

    # married field:
    # bool -> True or False
    # default=None -> optional field
    # description used for documentation
    married: Annotated[
        bool,
        Field(default=None, description="Is the patient married or not")
    ]

    # allergies field:
    # Optional[List[str]]
    # Means:
    # Either:
    #   - None
    # OR
    #   - list of strings
    #
    # Example:
    # ["Dust", "Milk"]
    #
    # max_length=5 means maximum 5 items in the list.
    allergies: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=5)
    ]

    # contact_details field:
    # Dictionary where:
    # key = string
    # value = string
    #
    # Example:
    # {"phone": "2353462"}
    contact_details: Dict[str, str]


# Function that accepts a Patient object
def update_patient_data(patient: Patient):

    # Print patient name
    print(patient.name)

    # Print patient age
    print(patient.age)

    # Print allergies list
    print(patient.allergies)

    # Print married status
    print(patient.married)

    # Print confirmation message
    print("updated")


# Dictionary containing patient data
patient_info = {

    # name value
    "name": "nitish",

    # valid email
    "email": "abc@gmail.com",

    # valid URL
    "linkedin_url": "http://linkedin.com/1322",

    # age given as STRING
    # Pydantic automatically converts it to int.
    "age": "30",

    # float value
    "weight": 75.2,

    # dictionary for contact details
    "contact_details": {"phone": "2353462"},
}


# Create Patient object
#
# ** unpacks the dictionary
#
# Equivalent to:
# Patient(
#     name="nitish",
#     email="abc@gmail.com",
#     ...
# )
#
# Pydantic validates all data here.
patient1 = Patient(**patient_info)


# Pass validated Patient object to function
update_patient_data(patient1)
```