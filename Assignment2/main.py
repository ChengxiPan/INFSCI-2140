import Indexing.PreProcessedCorpusReader as PreprocessedCorpusReader
import Indexing.MyIndexWriter as MyIndexWriter
import Indexing.MyIndexReader as MyIndexReader
import datetime


# This is for INFSCI 2140 in Fall 2023

def WriteIndex(type):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus =PreprocessedCorpusReader.PreprocessedCorpusReader(type)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter(type)
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1])
        count+=1
        if count%30000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return

def ReadIndex(type, token):
    # Initiate the index file reader.
    idx =MyIndexReader.MyIndexReader(type)
    # retrieve the token.
    df = idx.DocFreq(token)
    ctf = idx.CollectionFreq(token)
    print(" >> the token \""+token+"\" appeared in "+ str(df) +" documents and "+ str(ctf) +" times in total")
    if df>0:
        posting = idx.getPostingList(token)
        for docId in posting:
            docNo = idx.getDocNo(docId)
            print(docNo+"\t"+str(docId)+"\t"+str(posting[docId]))

startTime = datetime.datetime.now()
WriteIndex("trecweb")
endTime = datetime.datetime.now()
print ("time to index web corpus: ", endTime - startTime)
startTime = datetime.datetime.now()
ReadIndex("trecweb", "acow")
endTime = datetime.datetime.now()
print ("time to load index & retrieve the token: ", endTime - startTime)

startTime = datetime.datetime.now()
WriteIndex("trectext")
endTime = datetime.datetime.now()
print ("time to index web corpus: ", endTime - startTime)
startTime = datetime.datetime.now()
ReadIndex("trecweb", "yhoo")
endTime = datetime.datetime.now()
print ("time to load index & retrieve the token: ", endTime - startTime)