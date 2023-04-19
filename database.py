from databaseStructure import *
from databaseClasses.Project import Project
from databaseClasses.File import File
from databaseClasses.User import User

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    credentials = service_account.Credentials.from_service_account_file(credential_path)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    print(f"URL REFERENCE = {blob.public_url}")
    return blob.public_url
# upload_blob(firebase_admin.storage.bucket().name, 'backend/UML/other/usecasediagram1111.png', 'images/usecasediagram1111.png')


def save_generated_file_in_firestore(url_reference, file_data, destination_file_name):
    project_ref = firestore_client.collection("users").document(file_data["user_id"]).collection("projects").document(file_data["project_id"])
    # Add project data to the single project.
    project_ref.set({"files": {
                            file_data["file_name"]:
                                { 
                                 "has_useCase_diagram": True,
                                 "diagram_url_reference": url_reference,
                                }
                                }}
                                , merge = True )

    return 


def generate_use_case(file_data):
    data = {
        "user_id": file_data["user_id"],
        "user_name": file_data["user_name"],
        "project_id": file_data["project_id"],
        "project_name": file_data["project_name"],
        "file_url_reference": file_data["file_url_reference"],
        "file_name": file_data["file_name"],
        }
    image_reference = f"users/{data['user_name']}_{data['user_id']}/{data['project_name']}_{data['project_id']}/diagrams/useCase_diagram_{data['file_name']}.png"
    url_reference = upload_blob(firebase_admin.storage.bucket().name, source_file_name='../backend/UML/other/usecasediagram1111.png', destination_blob_name=image_reference)
    save_generated_file_in_firestore(url_reference=url_reference, file_data =data,destination_file_name= image_reference)
    
    return data
    
    
def delete_file(deleted_file):
    print("Deleting file in database file")

    user_id = deleted_file["user_id"]
    project_id = deleted_file["project_id"]
    file_name = deleted_file["file_name"]
    
    print(f"user id in delete_file database file = {user_id}")
    print(f"file_name in delete_file database file = {file_name}")
    print(f"project_id id in delete_file database file = {project_id}")
    
    # Delete the file from Firebase Firestore
    file_ref = db.collection('users').document(user_id).collection("projects").document(project_id).update({f"files[{file_name}]": firestore.DELETED_FIELD})
    
    return file_ref

def delete_specific_project(deleted_project):
    print("Deleting project in database file")

    user_id = deleted_project["user_id"]
    project_id = deleted_project["project_id"]
    
    print(f"user id in delete_project database file = {user_id}")
    print(f"project_id id in delete_project database file = {project_id}")

    # First delete the project from Firebase Firestore
    p_ref = db.collection('users').document(user_id).collection("projects").document(project_id).delete()
    
    return p_ref


def add_user(user_data):
    data = {
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "email": user_data["email"],
        "role": user_data["role"],
        }
    # Add the user to the AuthenticationManager
    try:
        u = auth.create_user(email=user_data["email"], password=user_data["password"])
    except ValueError:
        return "Password must be more than or equal to 6 characters"
    except firebase_admin._auth_utils.EmailAlreadyExistsError:
        return "UserAlreadyExists"

    # Add the user to Cloud firestore
    db.collection("users").document(u.uid).set(data)
    return "User Added"


def add_file_to_project(file_data):    
    project_ref = firestore_client.collection("users").document(file_data["user_id"]).collection("projects").document(file_data["project_id"])
    # Add project data to the single project.
    project_ref.set({"files": {
                            file_data["file_name"]:
                                { 
                                "name": file_data["file_name"],
                                "type": file_data["file_type"],
                                "size": file_data["file_size"],
                                "file_reference": file_data["file_reference"],
                                "url_reference": file_data["url_reference"],
                                "has_useCase_diagram": file_data["has_useCase_diagram"],
                                }
                                }}
                                , merge = True )

    return file_data["file_reference"]
        

def get_subcollection_projects(user_id):
    projects_of_user = Project(user_id=user_id)
    data = projects_of_user.get_multiple_projects()
    return data
    
def get_specific_project(user_id, project_id):
    project = Project(user_id=user_id, project_id=project_id)
    data = project.get_single_project()
    return data
    
def add_single_project(user_id, project_name, description):
    new_project = Project(user_id=user_id, project_name=project_name, description=description)
    response = new_project.add_single_project()
    return response
    
    
def send_project_files_URLs(user_id, project_id):
    project_data = get_specific_project(user_id=user_id, project_id=project_id)
    files = [value["url_reference"] for (key,value) in project_data[project_id]["files"].items()]
    print(f'FILES IN SEND_PROJECT_FILES = {files}')
    return  files
    

def upload_generated_UML_image_to_firebase():
    pass