import Classes.Path as Path
import re
from tqdm import tqdm

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
        content = ""
        in_content_flag = False
        
        for line in tqdm(self.file, desc="TrectestCollection"):
            line = line.strip()# remove blank
            if(line == "<DOC>"):
                # Now Enter <DOC></DOC>
                # reInit
                docNo = ""
                content = ""
                
            if(line == "<TEXT>"):
                # Now Enter <TEXT></TEXT> 
                in_content_flag = True
            elif(line == "</TEXT>"):
                # Now Exit <TEXT></TEXT>
                in_content_flag = False
                content = re.sub(r"<.*?>", "", content)
                # print("docNO:", docNo)
                # print("content: ", content)
                return [docNo, content]
            
            if(line.startswith("<DOCNO>")):
                docNo = re.sub(r"</?DOCNO>", "", line).strip()
                # docNo = docNo.replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            elif(in_content_flag):
                content+=line+" "
        
        self.file.close()
        return ["", ""]
