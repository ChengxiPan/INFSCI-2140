import Classes.Path as Path
import json

class MyIndexWriter:
    def __init__(self, type):
        """
        Initializes the index writer.
        `type` specifies the type of document (e.g., 'trecweb' or 'trectext').
        The writer will create an index file, a docid_map file, and a posting file.
        """
        self.docid_map = {}  # key: docNo, value: docId
        self.inverted_index = {}  # key: term, value: posting list (docId, frequency)
        self.counter = 0  # Used to assign unique docIds
        self.buffer_limit = 1000  # Limit for the number of documents in memory before flushing
        self.buffer_count = 0  # Track the number of documents processed so far
        self.type = type

        if type == "trecweb":
            self.index_file = open(f"{Path.IndexWebDir}/index_{self.type}.txt", "w")
            self.posting_file = open(f"{Path.IndexWebDir}/posting_{self.type}.json", "w")
            self.docid_map_file_path = f"{Path.IndexWebDir}/docid_map_{self.type}.txt"
        elif type == "trectext":
            self.index_file = open(f"{Path.IndexTextDir}/index_{self.type}.txt", "w")
            self.posting_file = open(f"{Path.IndexTextDir}/posting_{self.type}.json", "w")
            self.docid_map_file_path = f"{Path.IndexTextDir}/docid_map_{self.type}.txt"

        
        return

    def index(self, docNo, content):
        """
        Builds the index for each document.
        Converts `docNo` to a unique integer `docId`, and indexes the terms in the document.
        """
        # For every docNo, assign a unique docId
        if docNo not in self.docid_map:
            self.docid_map[docNo] = self.counter
            self.counter += 1

        docid = self.docid_map[docNo]

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
        """
        Flushes the in-memory inverted index to the disk (index and posting files).
        """
        for term, postings in self.inverted_index.items():
            # Write each term and its document list to the index file (terms and docIds)
            self.index_file.write(f"{term}: {','.join(str(docid) for docid, _ in postings)}\n")

            # Write the posting list to the posting file (docId and frequency)
            for docid, freq in postings:
                # write in json format
                # {term: term, docId: docId, freq: freq}
                # json.dump({"term": term, "docId": docid, "freq": freq}, self.posting_file)
                self.posting_file.write(json.dumps({"term": term, "docId": docid, "freq": freq}) + "\n")
                

        # Clear the in-memory index after flushing
        self.inverted_index.clear()
        self.buffer_count = 0

    def save_docid_map(self):
        """
        Writes the `docid_map` (mapping between `docNo` and `docId`) to the disk.
        """
        with open(self.docid_map_file_path, 'w') as f:
            for docNo, docId in self.docid_map.items():
                f.write(f"{docNo} {docId}\n")

    def close(self):
        """
        Closes the index writer. Flushes any remaining data in memory, and writes the docid_map to disk.
        """
        if self.buffer_count > 0:
            self.refresh_buffer()  # Flush the remaining buffered data

        # Write the docid_map to a separate file
        self.save_docid_map()

        # Close the index and posting files
        self.index_file.close()
        self.posting_file.close()
