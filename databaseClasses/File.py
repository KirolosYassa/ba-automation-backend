from database import *


class File:
    
    def __init__(self, file_name, file_reference="", file_size="", file_type="", url_reference="", has_useCase_diagram=False, has_Class_diagram=False):
        self.file_name = file_name
        self.file_reference = file_reference
        self.file_size = file_size
        self.file_type = file_type
        self.url_reference = url_reference
        self.has_useCase_diagram = has_useCase_diagram
        self.has_Class_diagram = has_Class_diagram
        
        
    def get_file_data(self):
        file_dict = { 
                    "name": self.file_name,
                    "type": self.file_type,
                    "size": self.file_size,
                    "file_reference": self.file_reference,
                    "url_reference": self.url_reference,
                    "has_useCase_diagram": self.has_useCase_diagram,
                    "has_Class_diagram": self.has_Class_diagram,
                    }
        return file_dict
     
        
    def delete_single_file(self, deleted_file):
        # needs user_id & project_id & file_name
        project = Project(user_id = deleted_file["user_id"],
                        project_id = deleted_file["project_id"])
        
        print("Deleting file in database file")
        print(f"user id in delete_file database file = {project.user_id}")
        print(f"file_name in delete_file database file = {self.file_name}")
        print(f"project_id id in delete_file database file = {project.project_id}")
        
        # Delete the file from Firebase Firestore
        file_ref = db.collection('users').document(project.user_id).collection("projects").document(project.project_id).update({f"files[{self.file_name}]": firestore.DELETED_FIELD})
        
        return file_ref

    
    def generate_useCase_diagram_with_file(self):
        # needs user_id & user_name & project_id & project_name & file_url_reference & file_name
        pass