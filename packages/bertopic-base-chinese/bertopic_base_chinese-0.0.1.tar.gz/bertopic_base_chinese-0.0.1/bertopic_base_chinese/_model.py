# https://zhuanlan.zhihu.com/p/587025298
# https://zhuanlan.zhihu.com/p/349781103
# https://zhuanlan.zhihu.com/p/643902193
# https://zhuanlan.zhihu.com/p/588248281
# https://zhuanlan.zhihu.com/p/587096188
# https://hidadeng.gitee.io/blog/bertopic主题建模/
# https://maartengr.github.io/BERTopic/getting_started/quickstart/quickstart.html
# https://maartengr.github.io/BERTopic/getting_started/embeddings/embeddings.html
# https://maartengr.github.io/BERTopic/faq.html#how-can-i-use-bertopic-with-chinese-documents
# https://maartengr.github.io/BERTopic/api/bertopic.html
# https://blog.csdn.net/qq_51116518/article/details/131199393

from sklearn.feature_extraction.text import CountVectorizer
import jieba
import bertopic

class BERTopic(bertopic.BERTopic):
    def __init__(self,
                 embedding_model="paraphrase-multilingual-MiniLM-L12-v2",
                 vectorizer_model=CountVectorizer(tokenizer=jieba.lcut),
                 **kwargs):
        super().__init__(embedding_model=embedding_model,
                         vectorizer_model=vectorizer_model,
                         **kwargs)
