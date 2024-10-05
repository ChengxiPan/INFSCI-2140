1. Quick Start
    Environment: conda 24.1.2, Python 3.12.3
    Command: 
        - pip install -r requirements.txt
        - python3 main.py
    Output: ./data/output/result.trectext, ./data/output/result.trecweb
    Terminal Output: 
        ```
        Total : 503473 docs
        Time to index text corpus:  0:27:18.355848

        Total : 198362 docs
        Time to index web corpus: 0:13:00.864175
        ```
    Estimated Time to Run: 40 minutes

2. File Structure and Description
    src
    ├── Classes
    │   ├── Path.py: Define the path of input and output files
    │   ├── Query.py
    ├── PreProcessData
    │   ├── StopWordRemover.py: Remove stop words from the text
    │   ├── TrectextCollection.py: read + tokenize + stopwords removal + normalization
    │   ├── TrecwebCollection.py: read + tokenize + stopwords removal + normalization
    │   ├── WordNormalizer.py: Use nltk.stemmer to normalize the words
    │   ├── WordTokenizer.py: Use re to tokenize the words
    ├── README.txt
    ├── data
    │   ├── input
    │   │   ├── docset.trectext: Text corpus
    │   │   ├── docset.trecweb: Web corpus
    │   │   └── stopwords.txt
    │   └── output
    │       ├── result.trectext: Trectext output but not provided
    │       └── result.trecweb: Trecweb output but not provided
    ├── main.py: Project Entry
    └── requirements.txt: Required packages

    I found python is much slower than Java, and it's because nltk's stemmer is extremely slow.
    There're 503473 docs in the text corpus, and it took 27 minutes to process.
    There're 198362 docs in the web corpus, and it took 13 minutes to process.