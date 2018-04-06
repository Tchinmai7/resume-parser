from stopwords.Stopwords import removeStopWords
from getresumecontent import getresumecontent
resume_content=getresumecontent('/Users/sangeethaswaminathan/Desktop/ResumeSample/xyz1')
for r in resume_content:
    print r
    print 'filtered',removeStopWords(unicode(r,"utf-8"))
