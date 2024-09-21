import Classes.Path as Path
import re

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.

# Please add comments along with your code.
class TrectextCollection:

    def __init__(self):
        # 1. Open the file in Path.DataTextDir.
        self.file = open(Path.DataTextDir, 'r', encoding='utf-8')
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its TEXT number and content.
        # 2. When no document left, return null, and close the file.
        docNo = ""
        content = []
        in_content_flag = False
        
        for line in self.file:
            line = line.strip()# remove blank
            if(line == "<DOC>"):
                # Now in <DOC></DOC>
                docNo = ""
                content = []
            if(line == "<TEXT>"):
                # Now in <TEXT></TEXT> 
                in_content_flag = True
            elif(line == "</TEXT>"):
                # Now Exit <TEXT></TEXT>
                in_content_flag = False
                content = ' '.join(content)
                return [docNo, content]
            
            if(line.startswith("<DOCNO>")):
                docNo = line.split(' ')[1] # extract docNo  
            elif(in_content_flag):
                content.append(line)
        
        self.file.close()
        return ["", ""]
