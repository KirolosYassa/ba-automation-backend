import os
import re
from pathlib import Path

import requests

# from IPython.core.display import SVG, display, HTML
from spacy.language import Language
import spacy
from spacy import displacy


@Language.component("custom_sentencizer")
def custom_sentencizer(doc):
    for i, token in enumerate(doc[:-1]):
        if token.text == ".":
            doc[i + 1].is_sent_start = False
        elif token.text == "As":
            doc[i].is_sent_start = True
        else:
            # Explicitly set sentence start to False otherwise, to tell
            # the parser to leave those tokens alone
            doc[i + 1].is_sent_start = False
    return doc


nlp = spacy.load("en_core_web_lg")
# nlp.add_pipe ( "custom_sentencizer", before="parser" )  # Insert before the parser
stopwords = nlp.Defaults.stop_words


##############################################################
###functions
##############################################################
# get Sentences Form File By using nlp custom Sentencizer
def getSentencesFromFile(file):
    doc = nlp(file)
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.text)

    return sentences


###function removes auxiliary verbs , determinants , and adjectives .
def reduceSentence(original_sentence):
    # Parse the original sentence

    doc = nlp(original_sentence)
    # Create a list of the parts of speech to remove
    pos_to_remove = ["DET", "ADJ", "AUX"]
    # Create a list of the tokens that should be kept
    tokens_to_keep = [token for token in doc if token.pos_ not in pos_to_remove]
    # Join the remaining tokens into a simplified sentence
    simplified_sentence = " ".join([token.text for token in tokens_to_keep])
    # Print the simplified sentence
    print("After reducing sentence :: ", simplified_sentence)
    return nlp(simplified_sentence)


def reduceSentences(original_sentences):
    # Parse the original sentence
    reduced_sentences = []
    for sentence in original_sentences:
        doc = nlp(sentence)
        # Create a list of the parts of speech to remove

        pos_to_remove = ["ADJ"]
        # Create a list of the tokens that should be kept
        tokens_to_keep = [token for token in doc if token.pos_ not in pos_to_remove]
        # Join the remaining tokens into a simplified sentence
        simplified_sentence = " ".join([token.text for token in tokens_to_keep])
        # Print the simplified sentence
        # print ( "After reducing sentence :: ", simplified_sentence )
        reduced_sentences.append(simplified_sentence)
    return reduced_sentences


def preprocess(sentences):
    for i, sentence in enumerate(sentences):
        # remove all punctuations except , and '
        regex = r"[!\"#\$%&\\(\)\*\+-\./:;<=>\?@\[\\\]\^_`{\|}~”“]"
        # r'[^\w\s]'

        sentences[i] = re.sub(regex, "", sentence)  # Remove punctuation
        sentences[i] = sentence.replace("\n", "")  # Remove newline
        # print ( sentences [ 1 ] )

    return sentences


def getFileByUrl(fileURL):
    # response = requests.get(url=fileURL)
    response = requests.get(
        "https://firebasestorage.googleapis.com/v0/b/ba-automation-5a4ae.appspot.com/o/users%2FTestOneUser_bAetrNSQkVcGLPExoRjaoKYPQMg1%2FLMS_fDMuAI2iG8itZI4na7E8%2Ffiles%2Fshort%20user%20stories%20test.txt_7c09499b-2588-4f3c-9c79-384a42ae0ab1?alt=media&token=80a7e5fb-4e24-406f-9e22-556c3864a4b3"
    )
    file = response.text
    print(f"fileURL in helperFunction = {fileURL}")
    print(f"response.text in helperFunction = {response.text}")
    return file


def getFile():
    with open("userStories/text.txt", encoding="utf-8") as f:
        return f.read()


def getAllNouns(sentence):
    ##### nouns
    nouns = []

    objNlp = nlp(sentence)

    ### to remove them from chuck.text.txt
    PRONOUNS = ["it", "she", "he", "they", "them", "these", "i"]
    ### this part get compound nouns
    for i, chunk in enumerate(objNlp.noun_chunks):
        if i == 0:
            continue
        if chunk.text not in nouns and chunk.text not in [x for x in PRONOUNS]:
            nouns.append(chunk.text)
        else:
            continue
    for x in nouns:
        print(x)

    return nouns


"""
def displayRender(sentence):
    doc = nlp(sentence)
    svg = displacy.render(doc, style="dep", jupyter=False)
    displacy.serve(doc, style="dep")
    # file_name = "imgae1"+ ".svg"
    # output_path = Path (  file_name )
    # output_path.open ( "w", encoding="utf-8" ).write ( svg )

"""


def isExists(x, list):
    if x in list:
        return True
    else:
        return False


def get_token_sentences(sentences):
    list = []

    for i, sentence in enumerate(sentences):
        listOfTokens = []
        v = sentences[i].find("so that")
        sentences[i] = sentences[i][0:v]
        sentence = sentences[i].lower()
        sentence = nlp(sentence)
        for token in sentence:
            listOfTokens.append(token)
        list.append(listOfTokens)

    return listOfTokens


def printtags(sent):
    sent = nlp(sent)
    for token in sent:
        print("token:", token.text, "  token pos", token.pos_)
