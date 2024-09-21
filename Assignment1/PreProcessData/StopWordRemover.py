import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.

# Please add comments along with your code.
class StopWordRemover:

    def __init__(self):
        # Load and store the stop words from the fileinputstream with appropriate data structure.
        # NT: address of stopword.txt is Path.StopwordDir.
        # Initialize a set to store stop words.
        self.stopwords = set()

        with open(Path.StopwordDir, 'r') as file:
            for word in file.readlines():
                self.stopwords.add(word.strip())

    def isStopword(self, word):
        # Return true if the input word is a stopword, or false if not.
        return word in self.stopwords
