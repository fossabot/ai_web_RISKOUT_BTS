FROM python:3.7.4-stretch

WORKDIR /home/user

RUN apt-get update -y
RUN apt-get install -y wget build-essential autotools-dev automake libmecab2 libmecab-dev

# install mecab
RUN wget -O - https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz | tar zxfv -
RUN cd mecab-0.996-ko-0.9.2; ./configure; make; make install; ldconfig

# install mecab python
RUN wget -O - https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.0.1-20150920.tar.gz | tar zxfv -
RUN cd mecab-ko-dic-2.0.1-20150920; sh ./autogen.sh
RUN cd mecab-ko-dic-2.0.1-20150920; ./configure; make; make install; ldconfig

# copy code
COPY riskout /home/user/riskout

# install as a package
COPY setup.py requirements.txt /home/user/
RUN pip install -r requirements.txt
RUN pip install -e .

# copy saved models
# COPY README.md models* /home/user/models/

# Copy REST API code
COPY rest_api /home/user/rest_api

# optional: copy data directory containing docs for ingestion
#COPY data /home/user/data

EXPOSE 8000

# cmd for running the API
CMD ["gunicorn", "rest_api.application:app",  "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "180"]
