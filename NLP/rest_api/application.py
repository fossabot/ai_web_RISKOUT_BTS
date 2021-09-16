import logging
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import List, Dict, Optional
from rest_api.config import ROOT_PATH, MODEL_PATH

from riskout.summarization import KorbartSummarizer
from riskout.textrank import KeysentenceSummarizer
from riskout.textrank import KeywordSummarizer
from riskout.utils import get_tokenizer, tokenize

logging.basicConfig(format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)

app = FastAPI(title="Riskout-API", debug=True, version="0.1")
kobartsum = KorbartSummarizer(model_path=MODEL_PATH)
tokenizer = get_tokenizer("mecab")

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

class Docs(BaseModel):
    document: Optional[str]


@app.post("/summarize")
async def summarize(docs: Docs):
    results = {"summairzed": ""}
    if docs:
        start_time = time.time()
        summarized = kobartsum.predict(docs.document)
        results["summairzed"] = summarized
        results.update({"time": time.time() - start_time})
    else:
        return {"detail": "Need docs"}

    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)