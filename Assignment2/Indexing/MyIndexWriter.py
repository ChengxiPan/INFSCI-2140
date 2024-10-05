import Classes.Path as Path
import json
# import jsonlines

class MyIndexWriter:
    def __init__(self, type):
        self.docid_map = {}  # key: docNo, value: docId
        self.inverted_index = {}  # key: term, value: posting list (docId, [appearance locator])
        self.counter = 0  # Used to assign unique docIds
        self.buffer_limit = 30000  # Limit for the number of documents in memory before flushing
        self.buffer_count = 0  # Track the number of documents processed so far
        self.type = type

        if type == "trecweb":
            self.dictionary_file = open(f"{Path.IndexWebDir}/dictionary_{self.type}.jsonl", "w") # [term, docId, freq]
            self.posting_file = open(f"{Path.IndexWebDir}/posting_{self.type}.jsonl", "w") # docNo: docId
        elif type == "trectext":
            self.dictionary_file = open(f"{Path.IndexTextDir}/dictionary_{self.type}.jsonl", "w")
            self.posting_file = open(f"{Path.IndexTextDir}/posting_{self.type}.jsonl", "w")

        
        return

    def index(self, docNo, content):
        # For every docNo, assign a unique docId
        if docNo not in self.docid_map:
            self.docid_map[docNo] = self.counter
            self.counter += 1

        docid = self.docid_map[docNo] # {docNo: docId}

        # Count the frequency of each term
        terms = content.split()  # Get terms
        term_freq = {}
        for term in terms:
            if term not in term_freq:
                term_freq[term] = 0
            term_freq[term] += 1

        # Process each term in the document
        for term, freq in term_freq.items():
            if term not in self.inverted_index:
                self.inverted_index[term] = []
            self.inverted_index[term].append((docid, freq))  #{docId: [posting list]}

        self.buffer_count += 1

        # If buffer limit is reached, flush the buffer
        if self.buffer_count >= self.buffer_limit:
            self.refresh_buffer()

    def refresh_buffer(self):
        for term, postings in self.inverted_index.items():
            # Write the posting list to the posting file (docId and frequency)
            for docid, freq in postings:
                self.dictionary_file.write(json.dumps({"term": term, "docId": docid, "freq": freq}) + "\n")
        
        for docNo, docId in self.docid_map.items():
            self.posting_file.write(json.dumps({"docNo": docNo, "docId": docId}) + "\n")

        self.inverted_index.clear()
        self.docid_map.clear()
        self.buffer_count = 0 # reInit

    def close(self):
        if self.buffer_count > 0:
            self.refresh_buffer()  # Flush the remaining buffered data
        self.dictionary_file.close()
