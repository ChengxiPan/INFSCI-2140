import Classes.Path as Path
import json
# import jsonlines

class MyIndexReader:
    def __init__(self, type):

        self.type = type
        self.docid_map = {}  # Maps docNo to docId
        self.docno_map = {}  # Maps docId to docNo
        self.posting_list = {}  # terms: {docId: freq}
        
        if type == "trecweb":
            self.dictionary_file = f"{Path.IndexWebDir}/dictionary_{self.type}.jsonl"  # [term, docId, freq]
            self.posting_file = f"{Path.IndexWebDir}/posting_{self.type}.jsonl"  # docNo: docId
        elif type == "trectext":
            self.dictionary_file = f"{Path.IndexTextDir}/dictionary_{self.type}.jsonl"
            self.posting_file = f"{Path.IndexTextDir}/posting_{self.type}.jsonl"
        
        self.initialize()
        # print("Finished reading the index.")

    def initialize(self):
        with open(self.posting_file, 'r') as f:
            for line in f:
                dic = json.loads(line)
                docNo, docId = dic["docNo"], dic["docId"]
                docId = int(docId)
                self.docid_map[docNo] = docId
                self.docno_map[docId] = docNo
                
        '''
        self.posting_list: 
        {
            term: {
                docId: freq
            }
        }
        '''
        with open(self.dictionary_file, 'r') as f:
            for line in f:
                dic = json.loads(line)
                term, docid, freq = dic["term"], dic["docId"], dic["freq"]
                if term not in self.posting_list:
                    self.posting_list[term] = {}
                self.posting_list[term][docid] = freq
        
    
    # def load_docid_map(self):
    #     with open(self.posting_file, 'r') as f:
    #         for line in f:
    #             docNo, docId = line.strip().split()
    #             docId = int(docId)
    #             self.docid_map[docNo] = docId
    #             self.docno_map[docId] = docNo
    #     # print the first element of the dictionary
    #     print("First element of docid_map: ", list(self.docid_map.items())[0])
    #     print("First element of docno_map: ", list(self.docno_map.items())[0])

    
    # def load_posting_list(self):
    #     with open(self.dictionary_file, 'r') as f:
    #         for line in f:
    #             dic = json.loads(line)
    #             term = dic["term"]
    #             docid = dic["docId"]
    #             freq = dic["freq"]
    #             if term not in self.posting_list:
    #                 self.posting_list[term] = {}
    #             self.posting_list[term][docid] = freq

    # Returns the integer docId for a given docNo
    def getDocId(self, docNo):
        return self.docid_map.get(docNo, -1)

    # Returns the string docNo for a given docId
    def getDocNo(self, docId) -> str:
        return self.docno_map.get(docId, "")

    # Returns the document frequency (DF) for a given term
    def DocFreq(self, token):
        if token in self.posting_list:
            return len(self.posting_list[token])
        return 0

    # Returns the collection frequency (CF) for a given term
    def CollectionFreq(self, token):
        if token in self.posting_list:
            return sum(self.posting_list[token].values())
        return 0

    # Returns the posting list for a given term
    def getPostingList(self, token):
        return self.posting_list.get(token, {})
