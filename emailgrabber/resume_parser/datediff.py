import re
import dateparser
from datetime import datetime
import json
def getdate(i_date):
    i_date=re.sub(' +','/',i_date)
    count=0
    spl_char_list=['`','\\','-','~','\'',':','"','|','/']
    for i in i_date:
        if i in spl_char_list:
            count=count+1
    o_date=re.split(r'[`\-~^\'\\:"|/]', i_date)
    if len(o_date) == 1:
        o_date.append('Jan')
        o_date.append('01')
    elif len(o_date) == 2:
        o_date.append('01')
    op_final_date='-'.join(o_date)
    return op_final_date

def getdiff(date1,date2):
    work_ex=0.0
    diff=0
    f_date1=getdate(date1)
    d1=dateparser.parse(f_date1)
    f_date2=getdate(date2)
    d2=dateparser.parse(f_date2)
    diff=d2-d1
    work_ex=work_ex+diff.days
    work_ex=round(work_ex/365,2)
    print "work ex",work_ex
    return work_ex







