# -*- coding: utf-8 -*-
# @Time    : 2021.6.9
# @Author  : Aman

from fastapi import FastAPI, Form
import uvicorn as u
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from ElasticSearch import *
import jieba.posseg as pseg
import re
import json
import time as t
import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

obj = ElasticObj(index_name="arxiv", index_type="papers")
print(obj.es)


def query_title(text):
    _candidates = []

    _doc = {
        "query": {
            "match": {
                # "default_field": "abstract",
                "title": ""
            }
        }
    }
    _doc['query']['match']['title'] = text
    _doc['size'] = 100 # 最多返回100条
    hits = obj.Get_Data_By_Body(_doc)
    for hit in hits:
        candidate = {}
        candidate["title"] = hit["_source"]["title"]
        candidate["authors"] = hit["_source"]["authors"]
        candidate["submitted_date"] = hit["_source"]["submitted_date"]
        candidate["abstract"] = hit["_source"]["abstract"]
        candidate["pdf_link"] = hit["_source"]["pdf_link"]
        candidate["score"] = hit["_score"]
        _candidates.append(candidate)

    return _candidates

def query_abstract(text):
    _candidates = []

    _doc = {
        "query": {
            "match": {
                # "default_field": "abstract",
                "abstract": ""
            }
        }
    }
    _doc['query']['match']['abstract'] = text
    _doc['size'] = 100 # 最多返回100条
    hits = obj.Get_Data_By_Body(_doc)
    for hit in hits:
        candidate = {}
        candidate["title"] = hit["_source"]["title"]
        candidate["authors"] = hit["_source"]["authors"]
        candidate["submitted_date"] = hit["_source"]["submitted_date"]
        candidate["abstract"] = hit["_source"]["abstract"]
        candidate["pdf_link"] = hit["_source"]["pdf_link"]
        candidate["score"] = hit["_score"]
        _candidates.append(candidate)

    return _candidates


def query_author(text):
    _candidates = []

    _doc = {
        "query": {
            "match": {
                # "default_field": "abstract",
                "authors": ""
            }
        }
    }
    _doc['query']['match']['authors'] = text
    _doc['size'] = 100 # 最多返回100条
    hits = obj.Get_Data_By_Body(_doc)
    for hit in hits:
        candidate = {}
        candidate["title"] = hit["_source"]["title"]
        candidate["authors"] = hit["_source"]["authors"]
        candidate["submitted_date"] = hit["_source"]["submitted_date"]
        candidate["abstract"] = hit["_source"]["abstract"]
        candidate["pdf_link"] = hit["_source"]["pdf_link"]
        candidate["score"] = hit["_score"]
        _candidates.append(candidate)

    return _candidates


def query_arxiv(text):
    _candidates = []

    _doc = {
        "query": {
            "multi_match": {
                # "default_field": "abstract",
                "query": "",
                "fields": ["title", "abstract", "authors"]
            }
        }
    }
    _doc['query']['multi_match']['query'] = text
    _doc['size'] = 50 # 最多返回50条
    hits = obj.Get_Data_By_Body(_doc)
    for hit in hits:
        candidate = {}
        candidate["title"] = hit["_source"]["title"]
        candidate["authors"] = hit["_source"]["authors"]
        candidate["submitted_date"] = hit["_source"]["submitted_date"]
        candidate["abstract"] = hit["_source"]["abstract"]
        candidate["pdf_link"] = hit["_source"]["pdf_link"]
        candidate["score"] = hit["_score"]
        _candidates.append(candidate)

    return _candidates

@app.post("/arxiv_search_tit/")
async def read_text(
                    request:       Request,
                    text: str    = Form(...),
                    ):
    t1 = t.time()
    res = query_title(text)
    time_cost = round(t.time() - t1, 3)
    n = len(res)
    print("Q_title: ", text)
    for item in res:
        item['title'] = item['title'].replace('Title:', '')
        item['authors'] = item['authors'].replace('Authors:', '')
        item['abstract'] = item['abstract'].replace('Abstract: ', '').replace('\n', ' ')
        item['score'] = round(item['score'], 3)
    if not n:
        return templates.TemplateResponse("no_results.html", {"request": request})
    else:
        return templates.TemplateResponse("results.html", {"request": request,
                                            "text": text,
                                            "N": n,
                                            "cost_time": time_cost,
                                            "res": res
                                        })


@app.post("/arxiv_search_abs/")
async def read_text(
                    request:       Request,
                    text: str    = Form(...),
                    ):
    t1 = t.time()
    res = query_abstract(text)
    time_cost = round(t.time() - t1, 3)
    n = len(res)
    print("Q_abstract: ", text)
    for item in res:
        item['title'] = item['title'].replace('Title:', '')
        item['authors'] = item['authors'].replace('Authors:', '')
        item['abstract'] = item['abstract'].replace('Abstract: ', '').replace('\n', ' ')
        item['score'] = round(item['score'], 3)
    if not n:
        return templates.TemplateResponse("no_results.html", {"request": request})
    else:
        return templates.TemplateResponse("results.html", {"request": request,
                                            "text": text,
                                            "N": n,
                                            "cost_time": time_cost,
                                            "res": res
                                        })


@app.post("/arxiv_search_aut/")
async def read_text(
                    request:       Request,
                    text: str    = Form(...),
                    ):
    t1 = t.time()
    res = query_author(text)
    time_cost = round(t.time() - t1, 3)
    n = len(res)
    print("Q_author: ", text)
    for item in res:
        item['title'] = item['title'].replace('Title:', '')
        item['authors'] = item['authors'].replace('Authors:', '')
        item['abstract'] = item['abstract'].replace('Abstract: ', '').replace('\n', ' ')
        item['score'] = round(item['score'], 3)
    if not n:
        return templates.TemplateResponse("no_results.html", {"request": request})
    else:
        return templates.TemplateResponse("results.html", {"request": request,
                                            "text": text,
                                            "N": n,
                                            "cost_time": time_cost,
                                            "res": res
                                        })

@app.post("/arxiv_search/")
async def read_text(
                    request:       Request,
                    text: str    = Form(...),
                    ):
    t1 = t.time()
    res = query_arxiv(text)
    time_cost = round(t.time() - t1, 3)
    n = len(res)
    # 打印当前时间的query
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now_time + " _Query_: " + text)

    for item in res:
        item['title'] = item['title'].replace('Title:', '')
        item['authors'] = item['authors'].replace('Authors:', '')
        item['abstract'] = item['abstract'].replace('Abstract: ', '').replace('\n', ' ')
        item['score'] = round(item['score'], 3)
    if not n:
        return templates.TemplateResponse("no_results.html", {"request": request})
    else:
        return templates.TemplateResponse("results.html", {"request": request,
                                            "text": text,
                                            "N": n,
                                            "cost_time": time_cost,
                                            "res": res
                                        })


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    u.run(app, host="0.0.0.0", port=9001)

# uvicorn 1sthelloworld.py:app --reload
