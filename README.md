# arXiv-Search
An arXiv paper search engine based on Elasticsearch and fastapi.

- [arXiv-Search](#arXiv-Search)
  - [Description](#description)
  - [Modules](#modules)
  - [Results](#results)


## Description
基于 [arXiv](https://arxiv.org/) 上的数据的一个论文检索系统，可以通过输入标题、作者、摘要中的关键字进行检索，方便研究人员高效地搜索相关论文。

爬虫部分代码略去。爬取论文标题、作者、摘要、提交日期和 pdf 链接共 5 个字段，数据格式如下 ([data_format](https://github.com/Aman-4-Real/arXiv-Search/blob/main/data/data_0.json))：
```
"0": {
  "abstract": "",
  "authors": "",
  "pdf_link": "",
  "submitted_data": "",
  "title": ""
}
```

系统分为后端 Elasticsearch 部分进行检索支持，在标题、作者、摘要三个字段上采用 BM25 计算查询与文档的相似度，并通过 fastapi 框架返回到前端进行搜索结果的展示。


## Modules
- [```main.py```](https://github.com/Aman-4-Real/arXiv-Search/tree/main/src/main.py): 

作为程序入口，包含了 fastapi 部分，执行 `python main.py` 即可 serve 在本地 9001 端口。

- [```ElasticSearch.py```](https://github.com/Aman-4-Real/arXiv-Search/tree/main/src/ElasticSearch.py): 

ES 的部分，进行数据预处理，索引创建、数据插入和删除、查询等操作，需要在 `__main__` 函数中注释对应部分操作。执行 `python Elasticsearch.py`。


## Results

![1](https://github.com/Aman-4-Real/arXiv-Search/blob/main/results/result1.jpg)
![2](https://github.com/Aman-4-Real/arXiv-Search/blob/main/results/result2.jpg)




