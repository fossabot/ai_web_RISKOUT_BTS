#!/bin/bash
echo "MongoDB install script By. dev-taewon-kim('https://github.com/dev-taewon-kim')"
echo "This script was written based on Ubuntu 20.04"
echo "This script will install MongoDB 4.4"

# Get MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

# Create sources.list
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Install mongoDB
sudo apt update
sudo apt install mongodb-org -y

# Make workspace dir for mongodb
sudo mkdir /data
sudo mkdir /data/db
sudo chown -R $(id -u -n):$(id -g -n)

# Echo guide
echo "Start mongoDB server daemon : mongod"
echo "Start mongoDB clinet : mongo"