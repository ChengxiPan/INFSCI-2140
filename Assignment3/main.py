import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery
import datetime

# This is for INFSCI 2140 in Fall 2023

if __name__ == "__main__":
    startTime = datetime.datetime.now()

    index = MyIndexReader.MyIndexReader("trectext")
    search = QueryRetreivalModel.QueryRetrievalModel(index)
    extractor = ExtractQuery.ExtractQuery()
    queries= extractor.getQueries()
    for query in queries:
        print(query.topicId,"\t",query.queryContent)
        break
        results = search.retrieveQuery(query, 20)
        rank = 1
        for result in results:
            print(query.getTopicId()," Q0 ",result.getDocNo(),' ',rank," ",result.getScore()," MYRUN",)
            rank += 1

    endTime = datetime.datetime.now()
    print("time to load index & retrieve the token: ", endTime - startTime)
