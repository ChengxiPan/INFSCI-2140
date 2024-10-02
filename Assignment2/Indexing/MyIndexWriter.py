import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
#
# Please explain the code with necessary comments.
class MyIndexWriter:
    def __init__(self, type):
        self.docid = {} # key: docNo, value: docid
        self.inverted_index = {} # key: term, value: posting list
        self.counter = 0
        self.buffer_limit = 1000
        self.buffer_count = 0
        self.type = type
        if(type == "trecweb"):
            self.index_file = open(f"{Path.IndexWebDir}/index_{self.type}.txt", "w")  # Open the index file for writing
        if(type == "trectext"):
            self.index_file = open(f"{Path.IndexTextDir}/index_{self.type}.txt", "w")  # Open the index file for writing
        return

    # This method build index for each document.
	# NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo, content):
        if docNo not in self.docid:
            self.docid[docNo] = self.counter
            self.counter += 1
        
        docid = self.docid[docNo]
        terms = content.split()
        
        for term in terms:
            if term not in self.inverted_index:
                self.inverted_index[term] = []
            if docid not in self.inverted_index[term]:
                self.inverted_index[term].append(docid)  # Add docid to the term's posting list
        
        self.buffer_count += 1
        if self.buffer_count >= self.buffer_limit:
            self.refresh_buffer()
            
    def refresh_buffer(self):
        for term, docids in self.inverted_index.items():
            # Write the term and its posting list to the index file
            self.index_file.write(f"{term}: {','.join(map(str, docids))}\n")

        # Clear the in-memory index after flushing
        self.inverted_index.clear()
        self.buffer_count = 0
        # return

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        if self.buffer_count > 0:
            self.refresh_buffer()

        self.index_file.close()