from Classes.Query import Query
from Classes.Document import Document  # Assuming you have a Document class
import math

class QueryRetrievalModel:

    def __init__(self, ixReader):
        self.indexReader = ixReader

    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN):
        # Tokenize and normalize the query
        query_terms = query.getQueryContent()

        # Initialize a dictionary to store document scores
        doc_scores = {}

        # Set the value for mu, which is a parameter for the scoring function
        mu = 200

        # Calculate collection probability (you may have a different method to calculate this)
        total_doc_count = self.indexReader.getTotalDocCount()
        collection_prob = {term: self.indexReader.CollectionFreq(term) / total_doc_count for term in query_terms}

        # Iterate through query terms and calculate scores
        for term in query_terms:
            posting_list = self.indexReader.getPostingList(term)

            if not posting_list:
                continue

            # Iterate through the posting list
            for doc_id, freq in posting_list.items():
                doc_length = self.indexReader.getDocLength(doc_id)
                score = self._calculate_score(freq, doc_length, len(posting_list), collection_prob[term], mu)

                if doc_id in doc_scores:
                    doc_scores[doc_id] += score
                else:
                    doc_scores[doc_id] = score

        # Sort documents by score in descending order and select top N
        sorted_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)[:topN]

        # Convert docId to docNo and create Document instances for the top results
        result_docs = [
            self._create_document(self.indexReader.getDocNo(doc_id), score)
            for doc_id, score in sorted_docs
        ]

        return result_docs



    def _calculate_score(self, term_freq, doc_length, doc_freq):
        # TF-IDF scoring formula
        tf = term_freq / doc_length
        idf = math.log((self.indexReader.getTotalDocCount() + 1) / (doc_freq + 1)) + 1
        return tf * idf

    def _create_document(self, doc_no, score):
        # Assuming Document class has id and score attributes
        doc = Document()
        doc.setDocNo(doc_no)
        doc.setScore(score)
        # print(f"DOCID: {doc_id}, SCORE: {score}")
        return doc
    
    def _calculate_score(self, term_freq, doc_length, doc_freq, collection_prob, mu):
    # Dirichlet smoothing score
        smoothed_prob = (term_freq + mu * collection_prob) / (doc_length + mu)
        return smoothed_prob

