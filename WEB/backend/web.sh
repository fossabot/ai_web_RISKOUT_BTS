#!/bin/bash

sudo docker-compose -f web-docker-compose.yml --env-file web-docker-env build --no-cache
sudo docker-compose -f web-docker-compose.yml --env-file web-docker-env up