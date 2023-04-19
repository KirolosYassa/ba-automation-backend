from databaseClasses import File
from database import *


class User:
                
    
    def __init__(self, user_id="", email="", first_name="", last_name="", role="", projects=[]):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.projects = projects

    
    def get_user_data(self):
        # needs user_id only

        doc = db.collection("users").document(self.user_id).get()
        print(doc)
        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
        else:
            print(u'No such document!')

        data = {}
        data[doc.id] = doc.to_dict()
        print(data)
        return data
        pass
    
    
    def get_user_id(self):
        # needs email only
        docs = db.collection("users").where("email", "==", self.email).get()
        for doc in docs:
            self.user_id = doc.id
        return self.user_id