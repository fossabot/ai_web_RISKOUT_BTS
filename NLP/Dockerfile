FROM python:3.7.4-stretch

WORKDIR /home/user

RUN apt-get update && apt-get install -y curl git pkg-config cmake
RUN apt-get install -y wget build-essential autotools-dev automake libmecab2 libmecab-dev


# copy code
COPY riskout /home/user/riskout

# install as a package
COPY setup.py requirements.txt /home/user/
RUN pip install -r requirements.txt

# install mecab
COPY mecab.sh /home/user/
RUN apt-get install -y g++ openjdk-8-jdk python3-dev python3-pip curl
RUN bash mecab.sh

# copy saved models
COPY models* /home/user/models/

# Copy REST API code
COPY rest_api /home/user/rest_api

# optional: copy data directory containing docs for ingestion
#COPY data /home/user/data

EXPOSE 8000

# cmd for running the API
# gunicorn application:app -k uvicorn.workers.UvicornWorker --workers 1
CMD ["gunicorn", "rest_api.application:app",  "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "180"]
