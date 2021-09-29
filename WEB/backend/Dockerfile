FROM ubuntu:20.04

# install python3.8-venv
RUN : \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.8-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

# set python3.8-venv as default python interpreter
RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH

# copy files
WORKDIR /home/user
COPY ../analyzer /home/user/analyzer
COPY ../crawler /home/user/crawler
COPY ./requirements.txt /home/user/requirements.txt

# install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN bash ./analyzer/mongo-test/mongo_install.sh

# run mongo server daemon and mongo client
RUN mongod
RUN mongo

# import riskout mongoDB init collection
RUN mongoimport --db=riskout --collection=counter --jsonArray --file=riskout_db.json

# Run crawler
CMD ["python", "./crawler/main.py"]
