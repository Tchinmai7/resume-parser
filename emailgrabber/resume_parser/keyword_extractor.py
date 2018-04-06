import spacy.en

def cleanup(token, lower = True):
    if lower:
        token = token.lower()
    return token.strip()


def extract_keywords(in_str):
    nlp = spacy.load('en')

    document = unicode(in_str.decode('utf8'))
    document = nlp(document)

    #Import the keywords
    f = open('gazetteer-tech.txt', 'r')
    allKeywords = f.read().lower().split("\n")
    f.close()
    matches = 0
    storedMatches = []
    for sent in document.sents:
        for keyword in allKeywords:
            if len(keyword) == 0:
                continue
            if keyword in sent.text.lower().replace('-', ' '):
                if keyword in storedMatches:
                    continue
                else:
                    storedMatches.append(keyword)
                    matches += 1
    #print "Matches: " + str(matches)
    #print storedMatches
    #print '**********'
    return storedMatches

# for testing
extract_keywords('this is a test php')
