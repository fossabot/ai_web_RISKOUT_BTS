#!/bin/bash

sudo docker-compose -f analyzer-docker-compose.yml build --no-cache
sudo docker-compose -f analyzer-docker-compose.yml up --force-recreate
