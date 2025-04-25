from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
app = FastAPI()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "name": "Foo",
                    "description": "A very nice item",
                    "Price": 35.4,
                    "tax": 3.2
                }
            ]
        }
    }

# class Item(BaseModel):
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(default=None, examples=["A very nice Item"])
#     price: float = Field(examples=[35.4])
#     tax: float | None = Field(default=None, examples=[3.2])

class Student(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, title="Name of the student", examples=["Julius Berger"])
    gender: str = Field("Male", min_length=4, max_length=6, title="Gender of the student", examples=["Male"])
    phone: str | None = Field(None, min_length=11, examples=["08032077920"])
    address: str | None = Field(None, min_length=20, examples=["Olaiya Area, Ogo-Oluwa, Osogbo, Osun State"])
    matric_number: str | None = Field(..., max_length=15, examples=["UNN/2012/879929"])
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"id": item_id, "item":Item }
    return results

@app.put("/update_student/{matric_number}")
async def update_record(post:Student, matric_number: str = Path(..., max_length=15)):
    db = []
    for index, student in db:
        if student["matric number"] == matric_number:
            updated_student = {student["name"] : post.name, student["gender"] : post.gender, student["phone"] : post.phone, student["address"] : post.address}
            db[index].update(updated_student)
            return db
        raise HTTPException(status_code=404, detail="Matriculation number not found.")    