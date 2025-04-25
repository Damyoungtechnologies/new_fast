import json
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

students_db = "students_db.json"
def load_db():
    try:
        with open(students_db) as file:
            return json.load(file)
    except FileNotFoundError:
        return []  
    except json.JSONDecodeError:
        return []  
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error loading database")

def save_db(db):
    try:
        with open(students_db, "w") as file:
            json.dump(db, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to save record")
    
class Student(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, title="Name of the student")
    gender: str = Field("Male", min_length=4, max_length=6, title="Gender of the student")
    phone: str | None = Field(None, min_length=11)
    address: str | None = Field(None, min_length=20)
    matric_number: str | None = Field(..., max_length=15)

@app.post("/post/")
async def add_student(age: Annotated[int, Query(ge=18, le=65)], post: Student):
    db = load_db()
    record = {
        "name": post.name,
        "gender": post.gender,
        "phone": post.phone,
        "address": post.address,
        "matric number": post.matric_number,
        "age": age
    }
    db.append(record)
    save_db(db)
    return {"message": "Student added successfully", "student": record}
@app.get("/search_by/{gender}")
async def search_by_gender(gender:Annotated[str, Path(min_length=4, max_length=6)]):
    db = load_db()
    matching_students = [student for student in db if student["gender"] == gender]
    if not matching_students:
        raise HTTPException(status_code=404, detail="No student found with the specified gender")
    return {"message": "Students found", "students": matching_students}

@app.get("/")
async def get_all_students():
    db = load_db()
    return db

@app.get("/search_list/")
async def search_list(phone: Annotated[str | None, Query(min_length=11)]=None, gender: str | None = None):
    db = load_db()
    for student in db:
        if student["gender"] == gender and student["phone"] == phone:
            return student
    raise HTTPException(status_code=404, detail="Record not found")

# to update using matric number
@app.put("/update_student/{matric_number}")
async def update_record(post:Student, matric_number: str = Path(..., max_length=15)):
    db = load_db()
    for index, student in db:
        if student["matric number"] == matric_number:
            updated_student = {student["name"] : post.name, student["gender"] : post.gender, student["phone"] : post.phone, student["address"] : post.address}
            db[index].update(updated_student)
            save_db(db)
            return db
        raise HTTPException(status_code=404, detail="Matriculation number not found.")    
        
            