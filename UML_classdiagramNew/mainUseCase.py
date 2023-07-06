# dont forget to run pip install -r requirements.txt
import os
from pprint import pprint
import spacy.tokens

# import UseCase.Actor
import UML_classdiagramNew.algorithm as algorithm
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
    # get sentences
    print(f"file_text in mainUseCase file = {file_text}")
    file = file_text

    # file = helperFunctions.getFile("userStories/test2.txt")
    sentences = helperFunctions.getSentencesFromFile(file)
    pprint(sentences)
    # reduce sentences
    # removes determinants , aux verbs and adjectives.
    sentences = algorithm.reduceSentences(sentences)
    sentences = algorithm.preprocess1(sentences)

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

    print("in main ######################################################")
    for actor in actors:
        print("################################")
        print(actor.name)
        for actorusecase in actor.usecases:
            print(actorusecase)

    id = uuid.uuid4()

    file_name = file_name.replace(".txt", "")

    if diagram_type == "use_case_diagram":
        filename = f"other/use_case_{file_name}_{id}.txt"
        dir = os.getcwd()
        filename = r"{}\UML_classdiagramNew\other\use_case_{}_{}.txt".format(
            dir, file_name, id
        )
        print(f"filename = {filename}")
        # filename = f"{os.getcwd()}\\other\\use_case_{file_name}_{id}.txt"

        # filename2 = f"other/use_case_{file_name}_{id}.png"
        # filename2 = f"D:/Graduation project/BA Automation Project/ba-automation/backend/UML_classdiagramNew/other/use_case_{file_name}_{id}.png"
        # filename2 = f"D:\\Graduation project\\BA Automation Project\\ba-automation\\backend\\UML_classdiagramNew\\other\\use_case_{file_name}_{id}.png"
        # filename2 = f"./UML_classdiagrmaNew/other/use_case_{file_name}_{id}.png"
        filename2 = r"{}\UML_classdiagramNew\other\use_case_{}_{}.png".format(
            dir, file_name, id
        )
    elif diagram_type == "class_diagram":
        filename = f"D:\\Graduation project\\BA Automation Project\\ba-automation\\backend\\UML_classdiagramNew\\other\\class_diagram_{file_name}_{id}.txt"
        filename2 = f"D:\\Graduation project\\BA Automation Project\\ba-automation\\backend\\UML_classdiagramNew\\other\\class_diagram_{file_name}_{id}.png"

    # filename = "other/usecasediagram2.txt"
    # filename2 = "other/usecasediagram2.png"
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The filename does not exist")

    if os.path.exists(filename2):
        os.remove(filename2)
    else:
        print("The filename2 does not exist")
    print(f"os.getcwd() = {os.getcwd()}")
    os.system("pip install plantuml")
    usecasemodel = plantUML.UseCaseModel(filename)
    usecasemodel.addCustomMessage("left to right direction")

    for i, actor in enumerate(actors):
        # usecasemodel.addActor ( actor.name )
        count = 0
        for i, usecasesobj in enumerate(actor.usecases):
            print(type(usecasesobj))
            if usecasesobj != [] and usecasesobj:
                if type(usecasesobj) == list:
                    count1 = 0
                    for useCaseObj in usecasesobj:
                        if count1 < 10:
                            usecasemodel.addUseCase(useCaseObj)
                            usecasemodel.addUseCasetoActor(actor.name, useCaseObj)
                            count1 = count1 + 1
                        elif count1 >= 10:
                            usecasemodel.addUseCase(useCaseObj)
                            usecasemodel.addUseCasetoActorLeftSide(
                                actor.name, useCaseObj
                            )
                            count1 = count1 + 1
                else:
                    if usecasesobj != " ":
                        if count < 10:
                            usecasemodel.addUseCase(usecasesobj)
                            usecasemodel.addUseCasetoActor(actor.name, usecasesobj)
                            count = count + 1
                        elif count >= 10:
                            usecasemodel.addUseCase(usecasesobj)
                            usecasemodel.addUseCasetoActorLeftSide(
                                actor.name, usecasesobj
                            )
                            count = count + 1

                for key in actor.dependencies.keys():
                    if key != None:
                        if actor.usecases[key] == usecasesobj and actor.usecases[key]:
                            if actor.usecases[actor.dependencies[key]] != " ":
                                print(
                                    "act dep key :",
                                    actor.usecases[actor.dependencies[key]],
                                )
                                usecasemodel.addUseCase2toUseCase1(
                                    usecasesobj, actor.usecases[actor.dependencies[key]]
                                )

    usecasemodel.closeFile()
    os.system("python -m plantuml " + filename)
    print(f"filename2 = {filename2}")
    return filename2
