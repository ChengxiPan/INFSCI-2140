import Classes.Path as Path  # 假设 Path 类中已经定义了存放索引文件的位置

# 需要特别关注效率和内存成本
class MyIndexReader:

    def __init__(self, type):
        """
        初始化索引读取器。
        `type` 用于指定文档的类型（如文本、网页等），可能会影响读取的方式。
        在此方法中，我们可以从磁盘读取并加载倒排索引等相关数据结构。
        """
        self.type = type
        self.docid_map = {}  # 用于存放 docNo 到 docid 的映射
        self.docno_map = {}  # 用于存放 docid 到 docNo 的映射
        self.inverted_index = {}  # 用于存放词项到文档ID列表的倒排索引
        self.doc_freq = {}  # 存放词项的文档频率
        self.collection_freq = {}  # 存放词项在整个集合中的词频
        self.load_index()  # 调用自定义方法加载索引
        print("finish reading the index")

    def load_index(self):
        """
        从磁盘读取索引文件并加载到内存中。
        假设索引文件包含倒排索引和文档 ID 映射信息。
        """
        # 假设索引文件已经按照特定格式存储在 Path.index_dir 中
        index_file = f"{Path.index_dir}/index_{self.type}.txt"
        docid_map_file = f"{Path.index_dir}/docid_map_{self.type}.txt"

        # 加载 docNo 到 docid 的映射文件
        with open(docid_map_file, 'r') as f:
            for line in f:
                docNo, docid = line.strip().split()
                docid = int(docid)
                self.docid_map[docNo] = docid
                self.docno_map[docid] = docNo
        
        # 加载倒排索引
        with open(index_file, 'r') as f:
            for line in f:
                term, postings = line.strip().split(':')
                postings_list = postings.split(',')
                postings_dict = {}
                for posting in postings_list:
                    docid, freq = map(int, posting.split('-'))
                    postings_dict[docid] = freq
                self.inverted_index[term] = postings_dict
                self.doc_freq[term] = len(postings_dict)
                self.collection_freq[term] = sum(postings_dict.values())

    # 返回输入的字符串形式的文档编号对应的整数形式的文档ID
    def getDocId(self, docNo):
        """
        返回与输入的 `docNo` 对应的整数 `docId`。
        如果找不到，返回 -1。
        """
        return self.docid_map.get(docNo, -1)

    # 返回输入的整数形式的文档ID对应的字符串形式的文档编号
    def getDocNo(self, docId):
        """
        返回与输入的 `docId` 对应的字符串 `docNo`。
        如果找不到，返回 -1。
        """
        return self.docno_map.get(docId, -1)

    # 返回文档频率（DF）
    def DocFreq(self, token):
        """
        返回某个词项的文档频率（即包含该词项的文档数量）。
        """
        return self.doc_freq.get(token, 0)

    # 返回整个集合中该词项的频率
    def CollectionFreq(self, token):
        """
        返回某个词项在整个集合中的出现频率。
        """
        return self.collection_freq.get(token, 0)

    # 返回该词项的倒排表，以 {documentID: frequency} 的形式
    def getPostingList(self, token):
        """
        返回该词项的倒排表，形式为 {docid: frequency}。
        """
        return self.inverted_index.get(token, {})
