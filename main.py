'''
pip install -r requirements.txt

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
    "http://localhost:3000/",
    "http://127.0.0.1/3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
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
    
class UploadedFiles(BaseModel):
      user_id: str
      project_: str
      files: dict
    
class DeletedProject(BaseModel):
      user_id: str
      project_id: str
    
class DeletedFile(BaseModel):
      user_id: str
      project_id: str
      file_name: str


@app.get("/login")
async def login(user_id: str):
    print("login is activated!")
    print(f"user id in login backend = {user_id}")
    data = get_user(user_id=user_id)
    print(data)
    return {"data": data}



# Delete specific project of a single user
@app.delete("/single_file/")
async def delete_file(deleted_file: DeletedFile):
    deletedFile_data = {
    "user_id": deleted_file.user_id,
    "project_id":  deleted_file.project_id,
    "file_name": deleted_file.file_name,
    }
    print("delete_file is activated!")
    user_id = deletedFile_data["user_id"]
    project_id = deletedFile_data["project_id"]
    file_name = deletedFile_data["file_name"]
    print(f"user id in delete_file backend = {user_id}")
    print(f"project_id id in delete_file backend = {project_id}")
    print(f"file_name in delete_file backend = {file_name}")
    data = delete_file(deleted_file)
    print(data)
    return {"data": data}

# Delete specific project of a single user
@app.delete("/single_project/")
async def delete_project(deletedProject: DeletedProject):
    deletedProject_data = {
    "user_id": deletedProject.user_id,
    "project_id":  deletedProject.project_id,
    }
    user_id = deletedProject_data["user_id"]
    project_id = deletedProject_data["project_id"]
    print("delete_project is activated!")
    print(f"user id in delete_project backend = {user_id}")
    print(f"project_id id in delete_project backend = {project_id}")
    data = delete_specific_project(deletedProject_data)
    print(data)
    return {"data": data}


# Add project for specific user with his/her user_id
@app.post("/generate_use_case_with_file")
async def generate_use_case_with_file(user_id: str, user_name: str, project_id: str, project_name: str, file_url_reference: str, file_name: str):
    print("generate_use_case_with_file is activated!")
    print(f"user id in generate_use_case_with_file backend = {user_id}")
    print(f"project_id id in generate_use_case_with_file backend = {project_id}")
    file_data = {
        "user_id": user_id,
        "user_name": user_name,
        "project_id": project_id,
        "project_name": project_name,
        "file_url_reference": file_url_reference,
        "file_name": file_name,
    }
    data = generate_use_case(file_data)
    print(f"data inside main file = {data}")
    return {"data": data}

# Add project for specific user with his/her user_id
@app.post("/addproject")
async def add_project(project: Project):
    print("add_project is activated!")
    print(f"user id in add_project backend = {project.user_id}")
    response = add_single_project(project.user_id, project.name, project.description)
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
    print("get_project is activated!")
    print(f"user id in get_project backend = {user_id}")
    print(f"project_id id in get_project backend = {project_id}")
    data = get_specific_project(user_id, project_id)
    print(f"data inside main file = {data}")
    return {"data": data}


# Post to Single Page to save files_data_uploaded to cloud firestore
@app.post("/single_project")
async def post_project(user_id: str, project_id: str, file_name: str, file_type: str, file_size: str, file_reference: str, url_reference: str):
    print("post_project is activated!")
    print(f"user id in post_project backend = {user_id}")
    print(f"project_id id in post_project backend = {project_id}")
    file_data = {
        "user_id": user_id,
        "project_id": project_id,
        "file_name": file_name,
        "file_type": file_type,
        "file_size": file_size,
        "file_reference": file_reference,
        "url_reference": url_reference,
    }
    data = add_file_to_project(file_data)
    print(f"data inside main file = {data}")
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