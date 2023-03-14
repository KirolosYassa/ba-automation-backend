import os
import firebase_admin
from firebase_admin import credentials, storage, firestore, auth
 

cred = credentials.Certificate(os.path.dirname(__file__) + "/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()
# auth = firebase_admin.auth()

db = firestore.client()

#readdata
# update_time, city_ref = db.collection(u'#users').add(city)

# new_city_ref = db.collection('#users').document()

# # later...
# new_city_ref.set({
#     u'name': u'Tokyo',
#     u'country': u'Japan'
# })

# print(f'Added document with id {new_city_ref.id}')


def log_in(email, password):
    response = auth.sign_in_with_email_and_password(email=email, password=password)
    # link = auth.generate_sign_in_with_email_link(email=email, action_code_settings=None)
    return response
    

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
    attr_ref.set({"name": project_data["name"], "description": project_data["description"]})

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
    
    collections = db.collection('users').document(user_id).collections()
    data = {}
    for collection in collections:
        for doc in collection.stream():
            if doc.id == project_id:
                data[doc.id] = doc.to_dict()
                break
    return data
    
def delete_specific_project(user_id, project_id):
    
    p_ref = db.collection('users').document(user_id).collection("projects").document(project_id).delete()
    return p_ref
    # collections = db.collection('users').document(user_id).collection("projects").document(project_id).get()
    # data = {}
    # for doc in collections:
    #     if doc.id == project_id:
    #         data = doc.to_dict()
    #         doc.delete()
    #         break
    # for collection in collections:
    #     print(collection)
    #     for doc in collection.stream():
    #         if doc.id == project_id:
    #             data = doc.to_dict()
    #             doc.delete()
    #             break
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