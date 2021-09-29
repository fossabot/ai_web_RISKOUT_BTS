#!/bin/bash

# run mongo server daemon in background
mongod --fork --logpath=/home/user/mongo.log

# import riskout mongoDB init collection
mongoimport --db=riskout --collection=counter --jsonArray --file=/home/user/analyzer/mongo-test/riskout_db.json

# Run crawler
python ./crawler/main.py

# Run analyzer
python ./analyzer/analyzer.py
