import time
import sys
from databaseStructure import *
from databaseClasses.Project import Project
from databaseClasses.File import File
from databaseClasses.User import User

sys.path.append("./UML-classdiagramNew/mainUseCase.py")
import UML_classdiagramNew.mainUseCase as generate_usecase_diagram
import UML_classdiagramNew.mainClass as generate_class_diagram


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    credentials = service_account.Credentials.from_service_account_file(credential_path)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    blob.make_public()
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    print(f"URL REFERENCE = {blob.public_url}")
    print(f"blob._get_download_url = {blob._get_download_url}")
    return blob.public_url


# upload_blob(firebase_admin.storage.bucket().name, 'backend/UML/other/usecasediagram1111.png', 'images/usecasediagram1111.png')


def save_generated_file_in_firestore(
    url_reference, file_data, destination_file_name, diagram_type
):
    project_ref = (
        firestore_client.collection("users")
        .document(file_data["user_id"])
        .collection("projects")
        .document(file_data["project_id"])
    )
    if diagram_type == "use_case_diagram":
        # Add project data to the single project.
        project_ref.set(
            {
                "files": {
                    file_data["file_name"]: {
                        "has_useCase_diagram": True,
                        "usecase_diagram_url_reference": url_reference,
                    }
                }
            },
            merge=True,
        )
    elif diagram_type == "class_diagram":
        # Add project data to the single project.
        project_ref.set(
            {
                "files": {
                    file_data["file_name"]: {
                        "has_Class_diagram": True,
                        "class_diagram_url_reference": url_reference,
                    }
                }
            },
            merge=True,
        )

    return


def generate_diagram(file_data, diagram_type):
    data = {
        "user_id": file_data["user_id"],
        "user_name": file_data["user_name"],
        "project_id": file_data["project_id"],
        "project_name": file_data["project_name"],
        "file_text": file_data["file_text"],
        "file_name": file_data["file_name"],
    }

    image_reference = f"users/{data['user_name']}_{data['user_id']}/{data['project_name']}_{data['project_id']}/diagrams/{diagram_type}_{data['file_name']}.png"

    # After processing then should be saved at firestore and firebase storage
    diagram_file_pathname = processing_on_file(data, diagram_type)
    # time.sleep(6)

    print(f"diagram_file_pathname = {diagram_file_pathname}")
    url_reference = upload_blob(
        firebase_admin.storage.bucket().name,
        source_file_name=diagram_file_pathname,
        destination_blob_name=image_reference,
    )
    print("----------------------------------------------------------------")
    print(f"url_reference = {url_reference}")
    print("----------------------------------------------------------------")
    save_generated_file_in_firestore(
        url_reference=url_reference,
        file_data=data,
        destination_file_name=image_reference,
        diagram_type=diagram_type,
    )

    return data


def processing_on_file(file_data, diagram_type):
    if diagram_type == "use_case_diagram":
        file_path = generate_usecase_diagram.generate_usecase_diagram(
            file_text=file_data["file_text"],
            file_name=file_data["file_name"],
        )
    elif diagram_type == "class_diagram":
        file_path = generate_class_diagram.generate_class_diagram(
            file_text=file_data["file_text"],
            file_name=file_data["file_name"],
        )
    # time.sleep(6)
    return file_path


def deleteFile(deleted_file: object):
    file_name_wanted_to_be_deleted = deleted_file["file_name"]
    file_wanted_to_be_deleted = File(
        file_name=file_name_wanted_to_be_deleted,
    )
    file_ref = file_wanted_to_be_deleted.delete_single_file(deleted_file)
    return file_ref


def delete_specific_project(deleted_project):
    project = Project(
        user_id=deleted_project["user_id"], project_id=deleted_project["project_id"]
    )
    time_deletion_of_project = project.delete_single_project()
    return time_deletion_of_project


def add_file_to_project(file_data):
    project = Project(user_id=file_data["user_id"], project_id=file_data["project_id"])
    file_reference = project.add_file_to_project(file_data)
    return file_reference


def add_user(user_data):
    new_user = User(
        email=user_data["email"],
        password=user_data["password"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        role=user_data["role"],
    )
    response_on_creating_user = new_user.add_user()
    return response_on_creating_user


def get_subcollection_projects(user_id):
    projects_of_user = Project(user_id=user_id)
    data = projects_of_user.get_multiple_projects()
    return data


def get_specific_project(user_id, project_id):
    project = Project(user_id=user_id, project_id=project_id)
    data = project.get_single_project()
    return data


def add_single_project(user_id, project_name, description):
    new_project = Project(
        user_id=user_id, project_name=project_name, description=description
    )
    response = new_project.add_single_project()
    return response


def send_project_files_URLs(user_id, project_id):
    project_data = get_specific_project(user_id=user_id, project_id=project_id)
    files = [
        value["url_reference"]
        for (key, value) in project_data[project_id]["files"].items()
    ]
    print(f"FILES IN SEND_PROJECT_FILES = {files}")
    return files


def upload_generated_UML_image_to_firebase():
    pass


def get_user(user_id):
    user = User(user_id=user_id)
    user_data = user.get_user_data()
    user = Project(user_id=user_id)
    projects = user.get_multiple_projects()
    user_data["projects"] = projects
    return user_data


def getTextContent(url=""):
    new_file = File(url_reference=url)
    return new_file.get_content_text()
