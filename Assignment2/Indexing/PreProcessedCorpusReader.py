import Classes.Path as Path

# Please explain the code with necessary comments.
class PreprocessedCorpusReader:

    def __init__(self, type):
        self.file_path = Path.ResultHM1 + type
        self.file = open(self.file_path, 'r', encoding='utf-8')
        return

    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
        # Read docNo and content from self.file
        docNo = self.file.readline().strip()
        content = self.file.readline().strip()
        # break when the end of the file is reached
        if not docNo:
            self.file.close()
            return None
        # print(f"docNo: {docNo}, content: {content}\n")
        return  [docNo, content]