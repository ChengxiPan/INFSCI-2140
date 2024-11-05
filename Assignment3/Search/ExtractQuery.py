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
        known_terms = set()  # Store known terms

        # Read even lines from result.trectext and result.trecweb files
        for result_file in ['data/result.trectext', 'data/result.trecweb']:
            with open(result_file, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file):
                    if line_number % 2 != 0:  # Process only even lines because only even lines are documents
                        known_terms.update(line.strip().split())
                        # print(type(known_terms), len(known_terms))
                        # break
                        # print(known_terms)

        # Read the topic file
        with open(self.topic_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if line.startswith("<num>"):
                    current_query_id = line.replace("<num> Number:", "").strip()  # Extract query ID
                elif line.startswith("<title>"):
                    current_query_content = line.replace("<title>", "").strip()  # Extract query content

                    # Process the query after extracting both num and title
                    if current_query_id and current_query_content:
                        processed_query = self.process_query(current_query_content)  # Process the query
                        # print(f"Query ID: {current_query_id}, Query Content: {processed_query}")

                        # Check for unknown terms
                        for term in processed_query:
                            if term not in known_terms:
                                # Delete the query if an unknown term is detected
                                processed_query.remove(term)
                        
                        # print(f"Processed Query: {processed_query}")
                        query = Query()  # Create an instance of Query
                        query.setTopicId(current_query_id)  # Set the query ID
                        query.setQueryContent(processed_query)  # Set the processed query content
                        queries.append(query)  # Append the query to the list
                        
                        # Reset for the next query
                        current_query_id = None
                        current_query_content = None

        return queries  # Return the list of queries


    def process_query(self, query):
        # Tokenize and lowercase
        tokenizer = re.compile(r'\b\w+\b')
        tokens = tokenizer.findall(query.lower())  
        processed_tokens = []

        for token in tokens:
            if token not in self.stopwords:
                stemmed_token = self.stemmer.stem(token)
                processed_tokens.append(stemmed_token)
        
        # return list of processed tokens
        return processed_tokens


    # Return extracted queries with class Query in a list.
    def getQueries(self):
        return self.queries
