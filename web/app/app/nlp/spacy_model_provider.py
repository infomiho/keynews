import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')

def get_model():
    return nlp

def get_stopwords_set():
    return STOP_WORDS
