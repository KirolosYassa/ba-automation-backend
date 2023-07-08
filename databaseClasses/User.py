from databaseClasses import File
from database import *


class User:
    def __init__(
        self,
        user_id="",
        email="",
        password="",
        first_name="",
        last_name="",
        role="",
        projects=[],
    ):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.projects = projects

    def add_user(self):
        # needs to email & first_name & last_name & role
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }
        # Add the user to the AuthenticationManager
        try:
            new_user = auth.create_user(email=self.email, password=self.password)
        except ValueError:
            return "Password must be more than or equal to 6 characters"
        except firebase_admin._auth_utils.EmailAlreadyExistsError:
            return "UserAlreadyExists"

        # Add the user to Cloud firestore
        db.collection("users").document(new_user.uid).set(data)
        return "User Added"

    def get_user_data(self):
        # needs user_id only

        doc = db.collection("users").document(self.user_id).get()
        print(doc)
        if doc.exists:
            print(f"Document data: {doc.to_dict()}")
        else:
            print("No such document!")

        data = {}
        data[doc.id] = doc.to_dict()
        print(data)
        return data

    def get_user_id_by_email(self):
        # needs email only
        docs = db.collection("users").where("email", "==", self.email).get()
        for doc in docs:
            self.user_id = doc.id
        return self.user_id
