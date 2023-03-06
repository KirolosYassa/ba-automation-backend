import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


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
docs = db.collection("#users").get()

for doc in docs:
    print(doc.to_dict())
    
   