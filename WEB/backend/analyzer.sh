#!/bin/bash

sudo docker-compose -f analyzer-docker-compose.yml --env-file analyzer-docker-env build --no-cache
sudo docker-compose -f analyzer-docker-compose.yml --env-file analyzer-docker-env up