import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

cred = credentials.Certificate(os.path.dirname(__file__) + "/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()


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
        "password": user["password"],
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
        "password": user_data["password"]
        }
    db.collection("users").add(data)


def get_user(user_id):
    doc = db.collection("users").document(user_id).get()
    print(doc)
    data = {}
    data[doc.id] = doc.to_dict()
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
