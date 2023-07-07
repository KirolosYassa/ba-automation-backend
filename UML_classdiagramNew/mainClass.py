import os

from spacy.matcher import Matcher

import UML_classdiagramNew.plantUML as plantUML
from UML_classdiagramNew.ClassEntity import ClassEntity
from UML_classdiagramNew.hellpingFiles.concept import getClassesFromFrequency2
import UML_classdiagramNew.helperFunctions as helperFunctions
import UML_classdiagramNew.algorithm as algorithm
import uuid
import nltk
import time

nltk.download("wordnet")
# if __name__ == '__main__':


def generate_class_diagram(
    file_text,
    file_name,
):
    # variables
    print(f"file_text in mainUseCase file = {file_text}")
    file = file_text
    sentences = helperFunctions.getSentencesFromFile(file)
    sentences = algorithm.preprocess1(sentences)

    sentences2 = " ".join(sentences)
    print(sentences2)

    sentences3 = algorithm.preprocess(sentences2)
    print(sentences3)

    sentences4 = algorithm.reduceSentences(sentences)
    print("SENTENCE 4 : ", sentences4)
    sentencesForRelations = " ".join(sentences4)

    sentencesForRelations = algorithm.preprocess(sentencesForRelations)

    listOfSentences = sentences3.split(".")

    algorithm.stemmingWholeDocument(listOfSentences)
    algorithm.parsingWholeDocument(listOfSentences)

    algorithm.generateSentencesFreeFromStopWords(listOfSentences)
    algorithm.extraction(listOfSentences)
    algorithm.removingDublicatesSw()

    print("main####")
    print("nouns and verbs:", algorithm.nounsAndVerbs)
    print("stopwords found : ", algorithm.stopwordsFound)
    print("concepts before :", algorithm.conceptList)

    concepts_Tokens = algorithm.concept(listOfSentences)

    print("conceptList:", algorithm.conceptList)
    print("concept tokens:", concepts_Tokens)
    algorithm.findGeneralization()
    print("generalization list :: ", algorithm.generalizationList.items())
    algorithm.extractClassByRules()
    getClassesFromFrequency2(algorithm.sentencesWithoutSW.values())

    print("concept list : ", algorithm.conceptList)

    algorithm.ExtractAttributes(sentences3)
    algorithm.ExtractInheritanceR(sentencesForRelations)
    algorithm.ExtractAggregationR(sentencesForRelations)
    algorithm.ExtractCompositionR(sentences3)
    algorithm.ExtractMethods(sentencesForRelations)

    print(algorithm.methodsClasses)

    # creating uml model and rendering picture for output
    new_id = uuid.uuid4()
    current_directory = os.getcwd()
    file_name = file_name.replace(".txt", "")
    # txt_plantuml_file = f"other/class_diagram_{file_name}_{new_id}.txt"
    # txt_plantuml_file = f"{current_directory}/UML_classdiagramNew/other/class_diagram_{file_name}_{new_id}.txt"

    txt_plantuml_file = r"{}/UML_classdiagramNew/other/class_diagram_{}_{}.txt".format(
        current_directory, file_name, new_id
    )

    png_diagram_file_extracted = (
        # f"other/class_diagram_{file_name}_{new_id}.png"
        # f"{current_directory}\\UML_classdiagramNew\\other\\class_diagram_{file_name}_{new_id}.png"
        r"{}/UML_classdiagramNew/other/class_diagram_{}_{}.png".format(
            current_directory, file_name, new_id
        )
    )

    # txt_plantuml_file = f"diagrams/{id}.txt"
    # png_diagram_file_extracted = f"diagrams/{id}.png"
    if os.path.exists(txt_plantuml_file):
        os.remove(txt_plantuml_file)
    else:
        print("The txt_plantuml_file does not exist")

    if os.path.exists(png_diagram_file_extracted):
        os.remove(png_diagram_file_extracted)
    else:
        print("The png_diagram_file_extracted does not exist")

    print(f"os.getcwd() = {os.getcwd()}")

    os.system("pip install plantuml")
    classModel = plantUML.ClassModel(txt_plantuml_file)

    # adding classes and attributes to model
    for classVar in algorithm.classes:
        print(f"classVar = {classVar}")
        classEntity = ClassEntity(classVar)
        if classEntity.className in algorithm.attributes.keys():
            for x in algorithm.attributes[classEntity.className]:
                classEntity.addAttributeToClass(x)
        classModel.addClass(classEntity.className)
        for att in classEntity.classAttributes:
            classModel.addMorFtoClass(classEntity.className, att, "+")
    for key in algorithm.attributes.keys():
        if key not in algorithm.classes:
            classModel.addClass(key.lower())
            for att in algorithm.attributes[key]:
                classModel.addMorFtoClass(key, att, "+")

    # adding Inheritance relationships to model
    for class1 in algorithm.IRelations.keys():
        if class1 not in algorithm.classes:
            classModel.addClass(class1.lower())
            for class2 in algorithm.IRelations[class1]:
                classModel.addExtensionRelation(class1, class2)

    # adding aggregation relationships to model
    for class1 in algorithm.AggRelations.keys():
        if class1 not in algorithm.classes:
            classModel.addClass(class1.lower())
            for class2 in algorithm.AggRelations[class1]:
                classModel.addAggregationRelation(class1.lower(), class2)
        else:
            for class2 in algorithm.AggRelations[class1]:
                classModel.addAggregationRelation(class1, class2)

        # adding aggregation relationships to model
    for class1 in algorithm.ComposRelations.keys():
        if class1 not in algorithm.classes:
            classModel.addClass(class1.lower())
        for class2 in algorithm.ComposRelations[class1]:
            classModel.addCompositionRelation(class1, class2)
    # adding methods to model
    for class1 in algorithm.methodsClasses.keys():
        for method in algorithm.methodsClasses[class1]:
            classModel.addMorFtoClass(class1, method, "+")

    classModel.closeFile()

    # os.chdir("UML_classdiagramNew\other")
    # print(f"os.getcwd() AFTER CHANGING = {os.getcwd()}")
    print(f"os.getcwd() = {os.getcwd()}")
    os.chdir("UML_classdiagramNew/other/")
    print(f"os.getcwd() AFTER CHANGING = {os.getcwd()}")
    time.sleep(2)
    os.system("python -m plantuml " + '"' + txt_plantuml_file + '"')

    print(f"txt_plantuml_file = {txt_plantuml_file}")
    print(f"png_diagram_file_extracted = {png_diagram_file_extracted}")
    return png_diagram_file_extracted
