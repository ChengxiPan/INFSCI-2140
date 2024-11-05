class Query:
    def __init__(self, queryContent="", topicId=""):
        self.queryContent = queryContent
        self.topicId = topicId

    # def __init__(self):
    #     self.queryContent = ""
    #     self.topicId = ""

    def getQueryContent(self):
        return self.queryContent

    def getTopicId(self):
        return self.topicId

    def setQueryContent(self, content):
        self.queryContent=content

    def setTopicId(self, id):
        self.topicId=id