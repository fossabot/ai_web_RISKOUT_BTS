import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

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
    Or just try it out directly: curl --request POST --url 'http://127.0.0.1:8000/query' -H "Content-Type: application/json"  --data '{"query": "Did Albus Dumbledore die?"}'
    """
)


@app.post("/summarize/")
async def summarize(docs: Optional[str] = None):
    results = {"summairzed": ""}
    if docs:
        summarized = kobartsum.predict(docs)

    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
