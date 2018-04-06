from __future__ import unicode_literals
import spacy
from spacy import en

def removeStopWords (inputString):
    nlp = en.English()
    sent = nlp(inputString)
    first = True
    for word in sent:
        if word.is_stop:
            print ''
        else:
            if first:
                final = word.string + ' '
                first = False
            else:
                final = final + word.string + ' '
    return final

