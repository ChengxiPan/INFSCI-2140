import Classes.Path as Path
import re

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.

# Please add comments along with your code.
class WordTokenizer:

    def __init__(self, content):
        # Tokenize the input texts.
        self.words = re.findall(r'\b\w+\b', content)
        self.current_index = 0

    def nextWord(self):
        # Return the next word in the document.
        # Return null, if it is the end of the document.
        if self.current_index < len(self.words):
            # Get the word at the current index.
            word = self.words[self.current_index]
            # Increment index
            self.current_index += 1
            return word
        else:
            # Return None if there are no more words left.
            return None