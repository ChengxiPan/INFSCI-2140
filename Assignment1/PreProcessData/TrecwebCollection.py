import Classes.Path as Path
from tqdm import tqdm
import re

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.

# Please add comments along with your code.
class TrecwebCollection:

    def __init__(self):
        # 1. Open the file in Path.DataWebDir.
        self.file = open(Path.DataWebDir, 'r', encoding='utf-8')
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        return

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        # 3. the HTML tags should be removed in document content.
        docNo = ""
        content = ""
        in_content_flag = False
        
        for line in tqdm(self.file, desc="TrecwebCollection"):
        # for line in self.file:
            line = line.strip()# remove blank
            if(line == "<DOC>"):
                # Now Enter <DOC></DOC>
                # reInit
                docNo = ""
                content = ""
                
            if(line == "</DOCHDR>"):
                # Now Enter </DOCHDR></DOC>
                in_content_flag = True
            elif(line == "</DOC>"):
                # Now Exit </DOCHDR></DOC>
                in_content_flag = False
                print(f"content: {content}\n")
                return [docNo, content]
            
            if(line.startswith("<DOCNO>")):
                docNo = re.sub(r"</?DOCNO>", "", line).strip()
                # docNo = docNo.replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            elif(in_content_flag):
                content+=line+" "
                content = re.sub(r"<.*?>", "", content)
        
        self.file.close()
        return ["", ""]