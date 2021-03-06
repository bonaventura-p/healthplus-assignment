#!/bin/bash
#this is a shell file to build and run the containers. first it installs the required dependencies and then it executes the docker-compose command.

#apt to use a repository over HTTPS:
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

#the one below is Docker’s official GPG key:
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

#verify key with fingerprint
sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

#get docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

#give permissions
sudo chmod +x /usr/local/bin/docker-compose

#get docker and the cli
sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io


cd healthplus-assignment
sudo docker-compose up




