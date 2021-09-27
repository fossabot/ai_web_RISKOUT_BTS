import logging
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import List, Dict, Optional, Union
from rest_api.config import KOBARTSUM_MODEL_PATH, SENTIMENT_MODEL_PATH, NER_MODEL_PATH

from riskout.ner import NER
from riskout.sentiment import SentimentClassifier
from riskout.summarization import KorbartSummarizer
from riskout.textrank import KeysentenceSummarizer
from riskout.textrank import KeywordSummarizer
from riskout.utils import get_tokenizer, tokenize

logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)

""" Initialization """
app = FastAPI(title="Riskout-API", debug=True, version="0.1")

tokenizer = get_tokenizer("mecab")
tokenize = lambda x: tokenizer.nouns(x)

kobart_summarizer = KorbartSummarizer(model_path=KOBARTSUM_MODEL_PATH)
sentiment_classifier = SentimentClassifier(model_path=SENTIMENT_MODEL_PATH)
named_entity_recognition = NER(model_path=NER_MODEL_PATH, split_by=tokenize)



app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")
logger.info(
    """
    Or just try it out directly
    curl --request POST \
        --url 'http://127.0.0.1:8000/summarize' \
        -H "Content-Type: application/json"  \
        --data '{"document": "SK이노베이션이 임시 주주총회을 열고 배터리 사업 분사를 결의했다. SK이노베이션은 16일 오전 10시 서울 종로구 SK서린빌딩에서 임시 주주총회를 열고 ‘SK배터리 주식회사(가칭)’와 ‘SK E&P 주식회사(가칭)’의 물적분할안을 의결했다. 전체 주주의 74.57%(6233만1624주)가 주총에 참석했으며, 이 가운데 80.2%(4998만1081주)가 찬성했다. 분할 조건인 주총 참석 주식의 3분의 2 이상, 전체 주식의 3분의 1이상 찬성을 확보했다. 2대 주주인 국민연금이 분사안에 반대한다는 의사를 밝혔지만 글로벌 의결권 자문기구 등이 찬성 의사를 밝혔다. SK이노베이션의 지분율은 올해 반기 기준 ㈜SK 등 특수관계인 33.4%, SK이노베이션 자기주식 10.8%, 국민연금 8.1%, 기타(외국인 및 국내 기관, 개인주주) 47.7% 등이다. 기타 지분 중 외국인ㆍ국내 기관이 약 26%, 개인주주가 22% 수준이다."}'
    """
)



class DocumentRequest(BaseModel):
    document: Optional[Union[List[str],str]] = None


@app.post("/ner")
async def ner(doc: DocumentRequest):
    if not doc:
        return {"detail": "Need doe"}

    results = {}
    if isinstance(doc.document, str):
        doc.document = [doc.document]
    start_time = time.time()
    entity = [named_entity_recognition.predict(d) for d in doc.document]
    try:
        results["ner"] = [{k: list(set(v)) for k, v in d.items()} for d in entity] # remove duplicated
    except:
        results["detail"] = "[Error with document] {}".format(doc.document[:100])
    results["time"] = time.time() - start_time

    return results
    

@app.post("/sentiment")
async def sentiment(doc: DocumentRequest):
    if not doc:
        return {"detail": "Need doc"}  

    results = {"score": []}
    if isinstance(doc.document, str):
        doc.document = [doc.document]
    start_time = time.time()
    try:
        scores = [sentiment_classifier.predict(d)[1] for d in doc.document] # [1] stand for positive score
        results["score"] = scores
    except:
        results["detail"] = "[Error with document] {}".format(doc.document[:100])
   
    results.update({"time": time.time() - start_time})

    return results


@app.post("/summarize")
async def summarize(doc: DocumentRequest):
    if not doc:
        return {"detail": "Need doc"}    

    results = {}
    if isinstance(doc.document, str):
        doc.document = [doc.document]
    start_time = time.time()
    try:
        results["summairzed"] = [kobart_summarizer.predict(d) for d in doc.document]
    except Exception as e:
        results["detail"] = "[Error] {}".format(e)

    results["time"] = time.time() - start_time
    return results


@app.post("/keywords")
async def keywords(doc: DocumentRequest):
    if not doc:
        return {"detail": "Need docs"}
    elif len(doc.document) <= 1:
        return {"detail": "Need more docs"}

    results = {}
    if isinstance(doc.document, str):
        doc.document = [doc.document]
    start_time = time.time()
    keyword_extractor = KeywordSummarizer(
        tokenize=tokenize,
        window=-1,
        verbose=False
    )
    try:
        results["keywords"] =  keyword_extractor.summarize(doc.document, topk=10)
    except:
        results["detail"] = "[Error with document] {}".format(doc.document[:100])
    results.update({"time": time.time() - start_time})
    return results


@app.post("/keysentences")
async def keysentences(doc: DocumentRequest):
    if not doc:
        return {"detail": "Need docs"}
    elif len(doc.document) <= 1:
        return {"detail": "Need more docs"}

    results = {}
    if isinstance(doc.document, str):
        doc.document = [doc.document]
    start_time = time.time()
    summarizer = KeysentenceSummarizer(
        tokenize=tokenize,
        min_sim=0.3,
        verbose=False
    )
    try:
        _keysentences = [{ "id": int(idx), "score": float(r), "sentence": str(sents)}
                         for idx, r, sents in summarizer.summarize(doc.document, topk=10)]
        results.update({"keysentences": _keysentences})
    except:
        results["detail"] = "[Error with document] {}".format(doc.document[:100])
    results.update({"time": time.time() - start_time})
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")