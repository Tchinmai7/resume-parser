from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from getresumecontent import getresumecontent
import workexfinder
from stopwords import Stopwords
from keyword_extractor import extract_keywords
import urllib
import nltk
import re
import pdb
def workexfinder(fn):
    workex_list=['CAREER','CAREER RELATED EXPERIENCE','EMPLOYMENT HISTORY','EMPLOYMENT','EXPERIENCE','FREELANCE','FREELANCE EXPERIENCE','PROFESSIONAL BACKGROUND','PROFESSIONAL EXPERIENCE','RELATED EXPERIENCE','WORK EXPERIENCE','WORK HISTORY']
    with open('headings.txt') as fheading:
        heading_content = fheading.readlines()
        heading_content = [x.strip() for x in heading_content]

    flag=0
    with open(fn) as fresume:
        resume_content = fresume.readlines()
        resume_content = [x.strip() for x in resume_content]
        for resume_iter in resume_content:
            if len(resume_iter)==0:
                resume_content.remove(resume_iter)
        workex='t1;;'
        for line in resume_content:
            if line.upper() in heading_content:
                flag=0
            if flag==1:
                workex=workex+line+';;'
            if line.upper() in workex_list:
                flag=1
        if workex == 't1;;':
            workex='t2;;'
            for line in resume_content:
                flag=0
                for workex_val in workex_list:
                    if workex_val in line.upper() and flag==0:
                        workex=workex+line+";;"
                        flag=1

        if workex == 't2;;':
            workex='t3;;'
            for resume_iter in resume_content:
                workex=workex+resume_iter+";;"

    return workex

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def download_attachment(url):
    path = "temp.pdf"
    urllib.urlretrieve (url, path)
    return path

def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'CD':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    elif t.__getitem__(1) == 'CD':
        entity_names.append(t.__getitem__(0))

    return entity_names

def process_resume(email_data):
    path = download_attachment(email_data["attachment_url"])
    text = convert_pdf_to_txt(path)
    text = text.rstrip()
    fp = file("temp.txt","wb")
    fp.write(text)
    fp.close()
    resume_text_list = getresumecontent("temp.txt")
    resume_text = ';'.join(resume_text_list)
    clean_text = Stopwords.removeStopWords(unicode(resume_text,encoding="utf-8"))
    keywords = extract_keywords(resume_text)
    workex = workexfinder("temp.txt")
    lines = workex.split(";;")
    entity_names = []
    string = "".join(lines)
    tokens = nltk.word_tokenize(string)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    for entity in entities:
        entity_names.extend(extract_entity_names(entity))
    retval = {}
    retval["keywords"] = keywords
    retval["workex"] = entity_names
    return retval

#process_resume()
