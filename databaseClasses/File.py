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
        
        
    
    