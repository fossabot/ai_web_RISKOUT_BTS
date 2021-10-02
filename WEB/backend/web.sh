#!/bin/bash

cd ../frontend

npm i
npm run build

rm -rf ../backend/drf/build/*
cp -r ./build ../backend/drf/

cd ../backend

sudo docker-compose -f web-docker-compose.yml --env-file web-docker-env up --force-recreate