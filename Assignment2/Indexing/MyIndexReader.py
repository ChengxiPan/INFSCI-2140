import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
#
# Please explain the code with necessary comments.
class MyIndexReader:

    def __init__(self, type):
        print("finish reading the index")

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        return -1

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        return -1

    # Return DF.
    def DocFreq(self, token):
        return 0

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        return 0

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        return
