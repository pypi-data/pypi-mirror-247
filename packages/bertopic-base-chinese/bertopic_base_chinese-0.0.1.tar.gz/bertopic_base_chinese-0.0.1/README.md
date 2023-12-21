# About
一个基于bertopic对中文文档进行主题建模的包。

# Install
`$ pip3 install -U bertopic_base_chinese`

# Director 
+ bertopic\_base\_chinese
    + \_model.py

## \_model.py
- BERTopic类
  重写了__init__()，设置embedding\_model为"paraphrase-multilingual-MiniLM-L12-v2"，以及选取tokenizer为jieba.lcut，初始化类参数。 

# Usage
```Python3
from bertopic_base_chinese import BERTopic

docs = ["我爱北京天安门", "我家大门常打开，开放怀抱等你"]
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(docs)
```

# Contact us
<may.xiaoya.zhang@gmail.com>
