def getresumecontent(fn):
     with open(fn) as fresume:
        resume_content = fresume.readlines()
        resume_content = [x.strip() for x in resume_content]
        for resume_iter in resume_content:
            if len(resume_iter)==0:
                resume_content.remove(resume_iter)
        return resume_content
