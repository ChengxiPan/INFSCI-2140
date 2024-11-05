from Classes.Query import Query
import Classes.Path as Path
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import os
import re

class ExtractQuery:
    
    def __init__(self):
        # 1. you should extract the 4 queries from the Path.TopicDir
        # 2. the query content of each topic should be 1) tokenized, 2) to lowercase, 3) remove stop words, 4) stemming
        # 3. you can simply pick up title only for query.
        self.topic_file_path = Path.TopicDir
        self.stopwords_file_path = "data/stopwords.txt"
        self.stemmer = PorterStemmer()
        self.stopwords = self._load_stopwords()
        self.queries = self._extract_queries()

    def _load_stopwords(self):
        with open(self.stopwords_file_path, 'r', encoding='utf-8') as file:
            return set(word.strip().lower() for word in file.readlines())

    def _extract_queries(self):
        queries = []
        current_query_id = None
        current_query_content = None

        with open(self.topic_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if line.startswith("<num>"):
                    current_query_id = line.replace("<num> Number:", "").strip()
                elif line.startswith("<title>"):
                    current_query_content = line.replace("<title>", "").strip()

                    # Process the query after extracting both num and title
                    if current_query_id and current_query_content:
                        processed_query, unknown_terms = self.process_query(current_query_content)
                        query = Query()  # Create an instance of Query
                        query.setTopicId(current_query_id)
                        query.setQueryContent(processed_query)
                        queries.append(query)
                        
                        # Reset for the next query
                        current_query_id = None
                        current_query_content = None

        return queries

    def process_query(self, query):
        # Tokenize and lowercase
        tokenizer = re.compile(r'\b\w+\b')
        tokens = tokenizer.findall(query.lower())  
        processed_tokens = []
        unknown_terms = []

        for token in tokens:
            if token not in self.stopwords:
                stemmed_token = self.stemmer.stem(token)
                processed_tokens.append(stemmed_token)
                if self.is_unknown_term(stemmed_token):
                    unknown_terms.append(stemmed_token)
        
        return ' '.join(processed_tokens), unknown_terms

    def is_unknown_term(self, term):
        # Dummy method to detect unknown terms
        # Replace with actual logic to check if the term exists in the collection
        return False

    # Return extracted queries with class Query in a list.
    def getQueries(self):
        return self.queries
