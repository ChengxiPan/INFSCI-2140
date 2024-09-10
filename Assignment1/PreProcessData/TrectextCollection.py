import Classes.Path as Path
import re
from tqdm import tqdm

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.

# Please add comments along with your code.
class TrectextCollection:

    def __init__(self):
        # 1. Open the file in Path.DataTextDir.
        self.file = open(Path.DataTextDir, 'r')
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        return

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its TEXT number and content.
        # 2. When no document left, return null, and close the file.
        docNo = ""
        content = ""
        in_doc_flag = False # identify whether in <TEXT></TEXT>
        
        for line in tqdm(self.file, desc="TrectextCollection"):
            line = line.strip()# remove blank
            if(line == "<TEXT>"):
                # Now Enter <TEXT></TEXT>
                in_doc_flag = True
                # reInit
                docNo = ""
                content = ""                
            elif(line == "</TEXT>"):
                # Now Exit <TEXT></TEXT>
                in_doc_flag = False
                return [docNo, content]
            elif(in_doc_flag):
                # Now Inside <TEXT></TEXT>
                if line.startswith("<DOCNO>"):
                    docNo = re.sub(r"</?DOCNO>", "", line).strip()
                else:
                    content+=line+" "
        
        self.file.close()
        return None
