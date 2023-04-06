import os
import firebase_admin
from firebase_admin import credentials, storage, firestore, auth
# import pyrebase
# from pyrebase.pyrebase import storage 
# from google.cloud import storage


credential_path = os.path.dirname(__file__) + "/serviceAccountKey.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ba-automation-5a4ae.appspot.com'
})
firestore_client = firestore.client()

# Initialize a client
db = firestore.client()


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


def get_all_users():
    docs = db.collection("users").get()

    all_users = {}
    for doc in docs:
        # print(user.to_dict())
        user = doc.to_dict()
        # print(user)
        user_info = {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"], 
        "role": user["role"],
        }
        all_users[doc.id] = user_info
        # print(user_info)
    # for doc in docs:
    print(all_users)
    return all_users

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


def get_user(user_id):
    print(f"user id in get_user function = {user_id}")
    doc = db.collection("users").document(user_id).get()
    print(doc)
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')

    data = {}
    data[doc.id] = doc.to_dict()
    print(data)
    return data

    
def get_all_collections(user_id):
    collections = db.collection('users').document(user_id).collections()
    for collection in collections:
        for doc in collection.stream():
            print(f'{doc.id} => {doc.to_dict()}')
            
# get_all_collections(user_id='ryMMVLaEJ5NBmNswSTgL')

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
                                }
                                }}
                                , merge = True )

    return file_data["file_reference"]
        

def add_project_to_users(user_id, project_data):
    user_ref = firestore_client.collection("users").document(user_id)
    # user_ref.set(project_data)
    #     # {
    #     #     "name": "Apple Macbook Pro",
    #     #     "brand": "Apple",
    #     # }

    # Specify the subcollection for a laptop document.
    projects = user_ref.collection("projects")

    # Add documents to the subcollection.
    attr_ref = projects.document(project_data["name"])
    attr_ref.set({"name": project_data["name"], "description": project_data["description"]}, { merge: true })

    # We don't need to create the doc ref beforehand if the metadata is not needed.
    # projects.document("ram").set({"name": "ram", "value": "16", "unit": "GB"})
    
def get_user_id(email):
    docs = db.collection("users").where("email", "==", email).get()
    for doc in docs:
        user_id = doc.id
    return user_id
# print(get_user_id("kirolosyassa2017@gmail.com"))

def get_subcollection_projects(user_id):
    collections = db.collection('users').document(user_id).collections()
    data = {}
    for collection in collections:
        for doc in collection.stream():
            data[doc.id] = doc.to_dict()
    return data
    
def get_specific_project(user_id, project_id):
    user_name = get_user(user_id=user_id)
    collections = db.collection('users').document(user_id).collections()
    # print(f"project_id = {project_id}")
    data = {}
    for collection in collections:
        for doc in collection.stream():
            # print(f"doc.id inside database file = {doc.id}")
            
            if doc.id == project_id:
                print(f"doc.to_dict() inside database file = {doc.to_dict()}")

                data[doc.id] = doc.to_dict()
                data[doc.id]["user_name"] = user_name[user_id]["first_name"]
                data[doc.id]["project_id"] = doc.id
                break
    # print(f"data inside database file = {data}")
    return data
    
def add_project_by_user_id(project_data):
    data = {
        "user_id": project_data["user_id"],
        "name": project_data["name"],
        "description": project_data["description"],
        }
    db.collection('users').document(data["user_id"]).collection('projects').add(data)
    # update_time, project_ref = db.collection('users').document(data["user_id"]).collection('projects').add(data)
    # print(update_time)
    # print(project_ref)
    # print(project_ref)
    return "Project Added"
    
project_data = {
        "user_id": "fqQRCusgnORUEKRHAqzNOqrM8nh1",
        "name": "First Project",
        "description": "hanet 5las aho", 
    }
# add_project_by_user_id(project_data)

def send_project_files_URLs(user_id, project_id):
    project_data = get_specific_project(user_id=user_id, project_id=project_id)
    files = [value["url_reference"] for (key,value) in project_data[project_id]["files"].items()]
    print(f'FILES IN SEND_PROJECT_FILES = {files}')
    return  files
    
print(send_project_files_URLs(user_id="HigzIsPL2vemKLC2dw8jTlTpe8V2", project_id="Ln9fVyaDv2uQyvzsPdoP"))