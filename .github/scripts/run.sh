#!/bin/bash
sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install wget
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
google-chrome --version
