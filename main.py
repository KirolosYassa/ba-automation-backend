from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware






app = FastAPI()

origins = [
    "https://ba-automation-5a4ae.web.app",
    "http://localhost:3000",
    "http://127.0.0.1/3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

@app.get("/")
def index():
    # return {"The Frontend is connected to the backend"}
    return {"msg": "The Frontend is connected to the backend"}

@app.get("/msgs")
def indexMsg():
    # return {"Hello World!"}
    return {"msg": "Hello World!"}

students={
    1:{
        "name": "john",
        "age":"21",
        "year":"year 2001"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The Id of the Student Required", gt=0)):
    if student_id not in students:
        return {"Data":"Data Not Found!"}
    return students[student_id]

@app.get("/get-by-name")
def get_student(name: str= None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data":"Data Not Found!"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    pass
    # if student_id in students:
    #     return {"Error msg": "This Student is already exist"}
    
    # students[student_id] = student
    # return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    pass
    # if student_id not in students:
    #     return {"Error msg": "This Student is not exist"}
    
    # if student.name != None:
    #     students[student_id].name = student.name
    
    # if student.age != None:
    #     students[student_id].age = student.age
    
    # if student.year != None:
    #     students[student_id].year = student.year

    # return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int, student: Student):
    pass
    # if student_id not in students:
    #     return {"Error msg": "This Student is not exist"}
    
    # del students[student_id]
    # return {"msg": "This Student is deleted successfully"}