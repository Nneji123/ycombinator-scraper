sudo apt update
# Download and install chrome

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# If you get 'wget' command not found, that means you do not have wget installed on your machine. Simply install it by running:

sudo apt install wget
# Then you can install chrome from the downloaded file.

sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
# Check Chrome is installed correctly.

google-chrome --version
