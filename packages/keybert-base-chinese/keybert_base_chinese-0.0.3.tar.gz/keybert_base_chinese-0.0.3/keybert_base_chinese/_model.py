# https://blog.csdn.net/whatwho_518/article/details/124481742
# https://blog.csdn.net/chenhepg/article/details/118571671
# https://zhuanlan.zhihu.com/p/462294183
# https://zhuanlan.zhihu.com/p/568271135

from sklearn.feature_extraction.text import CountVectorizer
import jieba
import keybert

class KeyBERT(keybert.KeyBERT):
    def __init__(self,
                 model="paraphrase-multilingual-MiniLM-L12-v2",
                 **kwargs):
        super().__init__(model=model, **kwargs)

    def extract_keywords(self,
                         docs,
                         vectorizer=CountVectorizer(tokenizer=jieba.lcut),
                         **kwargs):
        return super().extract_keywords(docs, vectorizer=vectorizer, **kwargs)

    def extract_embeddings(self,
                           docs,
                           vectorizer=CountVectorizer(tokenizer=jieba.lcut),
                           **kwargs):
        return super().extract_embeddings(docs, vectorizer=vectorizer, **kwargs)
