# dont forget to run pip install -r requirements.txt
import os
from pprint import pprint
import spacy.tokens
import UML_classdiagramNew.UseCase.Actor
import UML_classdiagramNew.helperFunctions as helperFunctions
import UML_classdiagramNew.plantUML as plantUML
from UML_classdiagramNew.UserStory import UserStory
import uuid

###pipeline
"""
format of user story . As a ..... , i want to , so that   ...... .
0-getting file
1-file preproccessing (detection of line rules . starting of 
    sentence is as and middle word i want to ,so that and full stop .((not done yet))
2-sentence separation . (done)
3-actor detection       (done)
4-use case extraction for each actor. (done)
5-drawing. (done)


"""


def generate_usecase_diagram(
    file_text,
    file_name,
    diagram_type,
):
    # print(f"url_reference = {url_reference}")
    # get sentences
    # file = helperFunctions.getFileByUrl(
    #     fileURL=url_reference
    #     # fileURL="https://firebasestorage.googleapis.com/v0/b/ba-automation-5a4ae.appspot.com/o/users%2FTestOneUser_bAetrNSQkVcGLPExoRjaoKYPQMg1%2FCoffee%20Shop_AsggMcho2theo8nGuL15%2Ffiles%2Funiversity.txt_d89af01a-38b1-411a-80de-eba6f2697505?alt=media&token=e1e3ef3d-bfc1-493a-b376-41c541679167"
    # )
    print(f"file_text in mainUseCase file = {file_text}")
    file = file_text
    sentences = helperFunctions.getSentencesFromFile(file)
    pprint(sentences)
    # reduce sentences
    # removes determinants , aux verbs and adjectives.
    sentences = helperFunctions.reduceSentences(sentences)
    sentences = helperFunctions.preprocess(sentences)

    actors = UserStory.extractActors(sentences)

    # for each sentence , get its actor and its use case . and put use case in actor's use case list
    for i, sent in enumerate(sentences):
        actor = None
        try:
            print("new sentence #####################")

            print(sent)
            usecasess, actor = UserStory.extractUseCase(sent)  ##x is a use case
        except AttributeError:
            print("error   attribute error")

    for actor in actors:
        print(actor.name)
        for actorusecase in actor.usecases:
            print(actorusecase)

    id = uuid.uuid4()

    file_name = file_name.replace(".txt", "")
    # file_name = file_name.replace(".txt", "")

    if diagram_type == "use_case_diagram":
        filename = f"./other/use_case_{file_name}_{id}.txt"
        filename2 = f"./other/use_case_{file_name}_{id}.png"
    elif diagram_type == "class_diagram":
        filename = f"./other/class_diagram_{file_name}_{id}.txt"
        filename2 = f"./other/class_diagram_{file_name}_{id}.png"

    if os.path.exists(filename) and os.path.exists(filename2):
        os.remove(filename)
        os.remove(filename2)
    else:
        with open(filename, "a") as f:
            f.write("")
        print(f"{filename} created!")

        # print("The file does not exist")

    # os.system("pip install plantuml")
    usecasemodel = plantUML.UseCaseModel(filename)
    usecasemodel.addCustomMessage("left to right direction")

    for i, actor in enumerate(actors):
        # usecasemodel.addActor ( actor.name )
        for i, usecasesobj in enumerate(actor.usecases):
            if usecasesobj != []:
                if type(usecasesobj) == list:
                    for useCaseObj in usecasesobj:
                        print(f"useCaseObj = {useCaseObj}")
                        usecasemodel.addUseCase(useCaseObj)
                        usecasemodel.addUseCasetoActor(actor.name, useCaseObj)
                else:
                    usecasemodel.addUseCase(usecasesobj)
                    usecasemodel.addUseCasetoActor(actor.name, usecasesobj)
                for key in actor.dependencies.keys():
                    if key != None:
                        if actor.usecases[key] == usecasesobj:
                            usecasemodel.addUseCase2toUseCase1(
                                usecasesobj, actor.usecases[actor.dependencies[key]]
                            )

    usecasemodel.closeFile()
    os.system("python -m plantuml " + filename)
    return filename2
