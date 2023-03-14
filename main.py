'''
cd .\backend\
python -m uvicorn main:app --reload
'''

from typing import Optional
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import *


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


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: str
    password: str
    
class Project(BaseModel):
    user_id: str
    name: str
    description: str


# Add project for specific user with his/her user_id
@app.post("/addproject")
async def add_project(project: Project):
    project_data = {
        "user_id": project.user_id,
        "name": project.name,
        "description": project.description, 
    }
    print("add_project is activated!")
    print(f"user id in add_project backend = {project.user_id}")
    response = add_project_by_user_id(project_data)
    print(response)
    return response


# Get from MyProfile Page to display all projects of a single user
@app.get("/projects")
async def get_user_projects(user_id: str):
    print("get_user_projects is activated!")
    print(f"user id in get_user_projects backend = {user_id}")
    data = get_subcollection_projects(user_id)
    print(data)
    return {"data": data}


# Get from Single Page to display specific project of a single user
@app.get("/single_project")
async def get_project(user_id: str, project_id: str):
    # print(query)
    # query = query.split("/")
    # user_id = query[0]
    # project_id = query[2]
    print("get_project is activated!")
    print(f"user id in get_project backend = {user_id}")
    print(f"project_id id in get_project backend = {project_id}")
    data = get_specific_project(user_id, project_id)
    print(data)
    return {"data": data}

# Delete specific project of a single user
@app.delete("/single_project")
async def delete_project(user_id: str, project_id: str):
    print("delete_project is activated!")
    print(f"user id in delete_project backend = {user_id}")
    print(f"project_id id in delete_project backend = {project_id}")
    data = delete_specific_project(user_id, project_id)
    print(data)
    return {"data": data}


@app.post("/signup")
def signup(user: User):
    try:
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email, 
            "password": user.password,
            "role": user.role,
        }
        # print(user_data)
        response = add_user(user_data)
        if response == "UserAlreadyExists":
            print("User already exists")
            return "UserAlreadyExists"
        else:
            print(response)
            return response
    except HTTPException:
        print("Format is not right!")
    return True
# kirolosyassa2017@gmail.com
# 333333
# @app.post("/login")
# def logIn(user: User):
#         user_data = {
#         # "first_name": "",
#         # "last_name": "",
#         "email": user.email, 
#         "password": user.password,
#         # "role": "",
#         }

#     # try:
#         response = log_in(email=user_data["email"], password=user_data["password"])
#         # print(user_data)
#         # response = add_user(user_data)
#         # if response == "UserAlreadyExists":
#         #     print("User already exists")
#         #     return "UserAlreadyExists"
#         # else:
#         #     print(response)
#         #     return response
#     # except HTTPException:
#         # print("Format is not right!")
#         # return True
#         print(response)
#         return response


# @app.get("/users")
# def get_users():
#     data = get_all_users()
#     return data


# @app.get("/user-id")
# def get_id(email: str = None):
#     id = get_user_id(email)
#     return {"id": id}













# class Student(BaseModel):
#     name: str
#     age: int
#     year: str

# class UpdateStudent(BaseModel):
#     name: Optional[str] = None
#     age: Optional[int] = None
#     year: Optional[str] = None

# @app.get("/get-student/{student_id}")
# def get_student(student_id: int = Path(None, description="The Id of the Student Required", gt=0)):
#     if student_id not in students:
#         return {"Data":"Data Not Found!"}
#     return students[student_id]

# @app.get("/get-by-name")
# def get_student(name: str= None):
#     for student_id in students:
#         if students[student_id]["name"] == name:
#             return students[student_id]
#     return {"Data":"Data Not Found!"}

#     # if student_id in students:
#     #     return {"Error msg": "This Student is already exist"}
    
#     # students[student_id] = student
#     # return students[student_id]

# @app.put("/update-student/{student_id}")
# def update_student(student_id: int, student: UpdateStudent):
#     pass
#     # if student_id not in students:
#     #     return {"Error msg": "This Student is not exist"}
    
#     # if student.name != None:
#     #     students[student_id].name = student.name
    
#     # if student.age != None:
#     #     students[student_id].age = student.age
    
#     # if student.year != None:
#     #     students[student_id].year = student.year

#     # return students[student_id]

# @app.delete("/delete-student/{student_id}")
# def delete_student(student_id: int, student: Student):
#     pass
#     # if student_id not in students:
#     #     return {"Error msg": "This Student is not exist"}
    
#     # del students[student_id]
#     # return {"msg": "This Student is deleted successfully"}