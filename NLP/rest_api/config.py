import os

FILE_UPLOAD_PATH = os.getenv("FILE_UPLOAD_PATH", "./file_upload")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ROOT_PATH = os.getenv("ROOT_PATH", "/")
MODEL_PATH = os.getenv("MODEL_PATH", "/home/user/models")

CONCURRENT_REQUEST_PER_WORKER = int(os.getenv("CONCURRENT_REQUEST_PER_WORKER", 4))
