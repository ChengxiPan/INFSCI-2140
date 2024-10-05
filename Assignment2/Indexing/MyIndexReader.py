import Classes.Path as Path
import json

class MyIndexReader:
    def __init__(self, type):
        """
        Initializes the index reader.
        Loads the index and posting files from disk and prepares the in-memory data structures.
        """
        self.type = type
        self.docid_map = {}  # Maps docNo to docId
        self.docno_map = {}  # Maps docId to docNo
        self.inverted_index = {}  # Maps terms to a list of docIds
        self.posting_list = {}  # Maps terms to {docId: frequency}
        self.load_index()  # Load index from files
        print("Finished reading the index.")

    def load_index(self):
        """
        Loads the index and posting data from disk into memory.
        """
        # Path to index and posting files
        index_file = f"{Path.IndexWebDir}/index_{self.type}.txt"
        posting_file = f"{Path.IndexWebDir}/posting_{self.type}.json"
        docid_map_file = f"{Path.IndexWebDir}/docid_map_{self.type}.txt"

        # Load docid_map (docNo to docId)
        with open(docid_map_file, 'r') as f:
            for line in f:
                docNo, docid = line.strip().split()
                docid = int(docid)
                self.docid_map[docNo] = docid
                self.docno_map[docid] = docNo

        # Load index (term to list of docIds)
        with open(index_file, 'r') as f:
            for line in f:
                term, doc_ids = line.strip().split(':')
                doc_id_list = list(map(int, doc_ids.split(',')))
                self.inverted_index[term] = doc_id_list

        # Load postings (term to {docId: frequency})
        with open(posting_file, 'r') as f:
            for line in f:
                dic = json.loads(line)
                term = dic["term"]
                docid = dic["docId"]
                freq = dic["freq"]
                if term not in self.posting_list:
                    self.posting_list[term] = {}
                self.posting_list[term][docid] = freq

    # Returns the integer docId for a given docNo
    def getDocId(self, docNo):
        """
        Returns the integer `docId` corresponding to the given `docNo`.
        If the docNo is not found, returns -1.
        """
        return self.docid_map.get(docNo, -1)

    # Returns the string docNo for a given docId
    def getDocNo(self, docId):
        """
        Returns the string `docNo` corresponding to the given `docId`.
        If the docId is not found, returns -1.
        """
        return self.docno_map.get(docId, -1)

    # Returns the document frequency (DF) for a given term
    def DocFreq(self, token):
        """
        Returns the document frequency (DF) for a given term.
        This is the number of documents that contain the term.
        """
        if token in self.inverted_index:
            return len(self.inverted_index[token])
        return 0

    # Returns the collection frequency (CF) for a given term
    def CollectionFreq(self, token):
        """
        Returns the collection frequency (CF) for a given term.
        This is the total number of occurrences of the term in the entire collection.
        """
        if token in self.posting_list:
            return sum(self.posting_list[token].values())
        return 0

    # Returns the posting list for a given term
    def getPostingList(self, token):
        """
        Returns the posting list for a given term.
        The posting list is a dictionary where the key is `docId` and the value is the frequency of the term in that document.
        """
        return self.posting_list.get(token, {})
