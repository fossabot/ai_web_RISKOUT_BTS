import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from fastapi import APIRouter
from pydantic import BaseModel

from riskout.summarization import KorbartSummarizer
from rest_api.config import LOG_LEVEL, CONCURRENT_REQUEST_PER_WORKER
# from rest_api.controller.utils import RequestLi
