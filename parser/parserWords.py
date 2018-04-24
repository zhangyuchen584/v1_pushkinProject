import nltk
from nltk.tokenize import word_tokenize

#pos tag: NN Adj etc...
def posTag(sentence):
    text = word_tokenize(sentence)
    return nltk.pos_tag(text)

